#Module imports
from MLDashboard.DashboardModules.LossMetricsGraph import LossMetricsGraph
from MLDashboard.DashboardModules.LossMetricsNumerical import LossMetricsNumerical
from MLDashboard.DashboardModules.StatusModule import StatusModule
from MLDashboard.DashboardModules.ControlButtons import ControlButtons
from MLDashboard.DashboardModules.TrainingSetSampleImages import TrainingSetSampleImages
from MLDashboard.DashboardModules.PredImages import PredImages
from MLDashboard.DashboardModules.EmptyModule import EmptyModule
from MLDashboard.DashboardModules.Module import Module

from MLDashboard.CommunicationBackend import Message, MessageMode
import matplotlib.pyplot as pyplot
from tensorflow.keras.callbacks import Callback
import multiprocessing
import warnings
import json
import time

#region Dashboard
allModules = {'LossMetricsGraph': LossMetricsGraph,
              'LossMetricsNumerical': LossMetricsNumerical,
              'StatusModule': StatusModule,
              'ControlButtons': ControlButtons,
              'TrainingSetSampleImages': TrainingSetSampleImages,
              'PredImages': PredImages,
              'EmptyModule': EmptyModule}

def dashboardProcess(configjson: dict, updatelist: list, returnlist: list):
    """Wrapper function to run dashboard in a seperate process. This should not be called manually."""
    print("Loading dashboard...")
    dashboard = Dashboard(configjson, updatelist, returnlist)
    print("Starting dashboard...")
    dashboard.runDashboardLoop()

def createDashboard(config='dashboard.json',
                    waitforstart=True) -> tuple[multiprocessing.Process, list[Message], list[Message]]:
    """
    Creates a dashboard running in a seperate thread.
    Returns the process, updatelist, and return list for communication
    :param config: The file to load the dashboard config from
    :param waitforstart: Should the main process halt while the dashboard starts
    """
    syncmanager = multiprocessing.Manager()
    updatelist: list[Message] = syncmanager.list()
    returnlist: list[Message] = syncmanager.list()

    with open(config) as f:
        configjson = json.load(f)
    process = multiprocessing.Process(target=dashboardProcess, args=(configjson, updatelist, returnlist,))
    process.start()

    if waitforstart:
        done = False
        rmindex = -1
        while not done:
            time.sleep(0.05)
            for index, item in enumerate(returnlist):
                if item.mode == MessageMode.Start:
                    rmindex = index
                    done = True
                    break

        returnlist.pop(rmindex)

    return process, updatelist, returnlist

def getModules(configjson):
    """Returns a list of module classes"""

    if "modules" not in configjson:
        raise Exception("Modules tag missing in config json.")
    modulelist = configjson["modules"]
    if len(modulelist) == 0:
        raise Exception("No modules found in config json.")

    sublistlen = len(modulelist[0])
    modules = []
    configs = []
    for sublist in modulelist:
        if len(sublist) != sublistlen:
            raise Exception("Modules do not form a grid.")
        for module, config in sublist:
            if module not in allModules:
                raise Exception("Module: " + str(module) + " not valid.")
            modules.append(allModules[module])
            configs.append(config)

    return modules, configs, sublistlen, len(modulelist)

def addRequests(reqs, outputlist):
    """Adds requests to output list if reqs is not none"""
    if reqs is not None:
        for item in reqs:
            outputlist.append(item)

class Dashboard:
    """
    Dashboard is a class that handles high level matplotlib interaction and sends data to sub modules.
    Dashbaords should be created with the createDashboard function.
    """
    def __init__(self, configjson: dict, updatelist: list[Message], returnlist:  list[Message]):
        self.configjson = configjson
        self.updatelist = updatelist
        self.returnlist = returnlist
        moduleclasslist, moduleconfiglist, self.width, self.height = getModules(configjson)
        self.modulelist: list[Module] = []


        self.fig = pyplot.figure()
        figManager = pyplot.get_current_fig_manager()
        figManager.window.state('zoomed')
        self.fig.suptitle("Tensorflow Dashboard")
        self.fig.canvas.manager.set_window_title("Tensorflow Dashboard")
        self.fig.set_tight_layout(True)
        for i, module in enumerate(moduleclasslist):
            ax = self.fig.add_subplot(self.height, self.width, i+1)
            m = module(ax, moduleconfiglist[i])
            addRequests(m.initialRequests(), self.returnlist)
            self.modulelist.append(m)

        # status metrics
        self.currentmode = "Live Render"  # are we rendering during training
        self.timer = 0  # time to do a full update loop
        self.modulestimer = [0.0] * len(self.modulelist) #how long does it take to render each module

    def runDashboardLoop(self): #this function is designed to be run in a separate process
        """Continually updates modules"""
        done = False
        self.returnlist.append(Message(MessageMode.Start, {}))
        while not done:
            while len(self.updatelist) == 0:
                pyplot.draw()
                pyplot.pause(0.001) #only update when resting

            mostrecentupdate = self.updatelist.pop(0)
            if mostrecentupdate.mode == MessageMode.ForceUpdate:
                pyplot.draw()
                pyplot.pause(0.001)

            else:
                starttime = time.time()
                for i, module in enumerate(self.modulelist):
                    sTime = time.time()
                    self.updateModule(module, mostrecentupdate)
                    self.modulestimer[i] = round(time.time() - sTime, 3)
                self.timer = round(time.time() - starttime, 3)


            if mostrecentupdate.mode == MessageMode.End:
                done = True

        print("Dashboard exiting cleanly...")
        self.currentmode = 'Post Training View'
        for module in self.modulelist:
            self.updateModule(module, Message(MessageMode.End, {}))

        pyplot.show()
        for module in self.modulelist:
            req = module.update(Message(MessageMode.End, {}))
            if req is not None:
                for item in req:
                    self.returnlist.append(item)

    def updateModule(self, module, mostrecentupdate: Message):
        if type(module) == StatusModule:
            reqs = module.update(Message(MessageMode.CustomData, {'autorendering': len(self.updatelist) <= 1,
                                                                  'currentmode': self.currentmode,
                                                                  'timer': self.timer,
                                                                  'modulestimer': self.modulestimer,
                                                                  'width': self.width,
                                                                  'height': self.height}))
        else:
            reqs = module.update(mostrecentupdate)

        addRequests(reqs, self.returnlist)

#endregion
#region Command Handling
def handleCommands(returnlist: list[Message], model, allowstop=True):
    """
    Handles return list commands, such as stop and save.
    :param returnlist: returnlist from dashboard creation
    :param model: Tensorflow / keras model
    :param allowstop: Should we warn if a stop command is triggered.
    """
    rmlist: list[int] = []
    for index, item in enumerate(returnlist):
        if item.mode == MessageMode.Command:
            rmlist.append(index)
            if item.body['command'] == 'stop':
                if allowstop:
                    print("Training manually stopped.")
                    model.stop_training = True
                else:
                    warnings.warn("Stop was triggered but training has already exited.")
            elif item.body['command'] == 'save':
                print("Model manually saved.")
                model.save(input("File name: "))


    rmlist.reverse()
    for index in rmlist:
        returnlist.pop(index)


def HandleRemaingCommands(returnlist: list[Message], model): #TODO - handle remaining data requests
    """
    This should be called after the dashboard exits.
    :param returnlist: returnlist from dashboard creation
    :param model: Tensorflow / keras model
    """
    handleCommands(returnlist, model, allowstop=False)
    if len(returnlist) > 0:
        warnings.warn("We couldn't handle these remaining requests: ")
        print(returnlist)

#endregion
#region Callbacks
class DashboardCallbacks(Callback):
    def __init__(self, updatelist: list[Message], returnlist: list[Message], model, x_train, y_train,
                 x_test, y_test, send_on_batch_end = False):
        """
        This inherits from Tensorflow callbacks and connects the model training to the dashboard.

        :param updatelist: List from dashboard creation
        :param returnlist: List from dashboard creation
        :param model: Tensorflow model
        :param x_train: Training set features
        :param y_train: Training set output
        :param x_test: Test set features
        :param y_test: Test set output
        :param send_on_batch_end: Should we send data on batch end, default to False to not overwhelm dashboard
        """

        super().__init__()
        self.updatelist = updatelist
        self.returnlist = returnlist
        self.model = model
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.send_on_batch_end = send_on_batch_end

        self.handleDataRequest()

    def handleDataRequest(self):
        rmlist = []
        for index, item in enumerate(self.returnlist):
            if item.mode == MessageMode.Train_Set_Sample:
                rmlist.append(index)
                num = item.body["num"]
                x = self.x_train[0:num]
                y = self.y_train[0:num]
                self.updatelist.append(Message(MessageMode.Train_Set_Sample, {"x": x, "y": y}))

            elif item.mode == MessageMode.Test_Set_Sample:
                rmlist.append(index)
                num = item.body["num"]
                x = self.x_test[0:num]
                y = self.y_test[0:num]
                self.updatelist.append(Message(MessageMode.Test_Set_Sample, {"x": x, "y": y}))

            elif item.mode == MessageMode.Pred_Sample:
                rmlist.append(index)
                num = item.body["num"]
                self.updatelist.append(Message(MessageMode.Pred_Sample,
                                               {"x": self.x_test[0:num],
                                                "y": self.y_test[0:num],
                                                "pred": self.model.predict(self.x_test[0:num])}))

            elif item.mode == MessageMode.Pred_Sample_Train:
                rmlist.append(index)
                num = item.body["num"]
                self.updatelist.append(Message(MessageMode.Pred_Sample_Train,
                                               {"x": self.x_train[0:num],
                                                "y": self.y_train[0:num],
                                                "pred": self.model.predict(self.x_train[0:num])}))

            elif item.mode == MessageMode.Wrong_Pred_Sample:
                rmlist.append(index)
                maxnum = item.body["maxnum"]
                attempts = item.body["attempts"]

                preds = self.model.predict(self.x_test[0:attempts])
                features = []
                wrongpreds = []
                correctresult = []
                for i in range(0, len(attempts)):
                    if preds[i] != self.y_test[i]:
                        features.append(self.x_test[i])
                        wrongpreds.append(preds[i])
                        correctresult.append(self.y_test[i])

                    if len(features) >= maxnum:
                        break

                self.updatelist.append(Message(MessageMode.Wrong_Pred_Sample,
                                               {"x": features,
                                                "y": correctresult,
                                                "pred": wrongpreds}))

            elif item.mode == MessageMode.Wrong_Pred_Sample_Train:
                rmlist.append(index)
                maxnum = item.body["maxnum"]
                attempts = item.body["attempts"]

                preds = self.model.predict(self.x_train[0:attempts])
                features = []
                wrongpreds = []
                correctresult = []
                for i in range(0, len(attempts)):
                    if preds[i] != self.y_train[i]:
                        features.append(self.x_train[i])
                        wrongpreds.append(preds[i])
                        correctresult.append(self.y_train[i])

                    if len(features) >= maxnum:
                        break

                self.updatelist.append(Message(MessageMode.Wrong_Pred_Sample_Train,
                                               {"x": features,
                                                "y": correctresult,
                                                "pred": wrongpreds}))

        rmlist.reverse()
        for index in rmlist:
            self.returnlist.pop(index)

    def on_train_batch_end(self, batch, logs=None): #this can overwhelm the dashboard, so its off by default
        if self.send_on_batch_end:
            self.updatelist.append(Message(MessageMode.Train_Batch_End, logs))

    def on_epoch_end(self, epoch, logs=None):
        logs['epoch'] = epoch
        self.updatelist.append(Message(MessageMode.Epoch_End, logs))
        self.updatelist.append(Message(MessageMode.ForceUpdate, {}))
        handleCommands(self.returnlist, self.model)

    def on_epoch_begin(self, epoch, logs=None):
        self.handleDataRequest()

#endregion Callbacks
