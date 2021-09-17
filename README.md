# Getting Started

This guide assumes you already understand python and tensorflow.

## Installation
```
pip install git+https://github.com/RobertJN64/MLDashboard
```

## Quick Start
To start, you need a dashboard.json config file. This should be in the same directory as your script.
Here is an example:
```python
{
    "modules":[
        [
            ["LossMetricsGraph", {}],
            ["LossMetricsNumerical", {}]
        ],
        [
            ["StatusModule",{}],
            ["EmptyModule", {}]
        ]
    ]
}
```


NOTE: All code in this demo should be protected by
```python
if __name__ == '__main__':
```
to prevent multiprocessing conflicts.

The dashboard can easily by added to an existing machine learning project.
Import the dashboard as shown.

```python
from MLDashboard.MLDashboardBackend import createDashboard
from MLDashboard.MLCallbacksBackend import DashboardCallbacks, CallbackConfig
from MLDashboard.MLCommunicationBackend import Message, MessageMode
```

Before training starts, create the dashboard.
```python
#MAKE SURE YOU HAVE A DASHBOARD.JSON FILE IN THE SAME DIRECTORY AS YOUR SCRIPT
dashboardProcess, updatelist, returnlist = createDashboard(config='dashboard.json')
```

Connect the callbacks to your training.
```python
config = CallbackConfig()
labels = list(range(0,10)) #labels should be customized for the data. This is for mnist number recognition
callback = DashboardCallbacks(updatelist, returnlist, model, x_train, y_train, x_test, y_test, labels, config)

model.fit(x_train, y_train, epochs=10, callbacks=[callback])
```

After training ends, you can send evaluation stats to the dashboard.
```python
model.evaluate(x_test, y_test, batch_size=128, callbacks=[callback])
```

To exit the dashboard cleanly, use the following code:
```python
updatelist.append(Message(MessageMode.End, {}))
print("Exiting cleanly...")
dashboardProcess.join()
print("Dashboard exited.")
#This handles any extra data that the dashboard sent, such as save commands
callback.HandleRemaingCommands()
```

Here is a full example with python code:
```python
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2' #stops agressive error message printing
import tensorflow as tf
from tensorflow import keras
from MLDashboard.MLDashboardBackend import createDashboard
from MLDashboard.MLCallbacksBackend import DashboardCallbacks, CallbackConfig
from MLDashboard.MLCommunicationBackend import Message, MessageMode

def run():
    print("Starting interactive dashboard demo...")
    print("Setting up dashboard...")

    #Create dashboard and return communication tools (this starts the process)
    #MAKE SURE YOU HAVE A DASHBOARD.JSON FILE IN THE SAME DIRECTORY AS YOUR SCRIPT
    dashboardProcess, updatelist, returnlist = createDashboard(config='dashboard.json')

    print("Loading data...")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    print("Formatting data...")
    x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

    print("Sampling data...")
    # Limit the train data to 10000 samples
    x_train = x_train[:10000]
    y_train = y_train[:10000]
    # Limit test data to 1000 samples
    x_test = x_test[:1000]
    y_test = y_test[:1000]

    print("Creating model...")
    model = keras.Sequential([keras.layers.Dense(128, activation='relu'), keras.layers.Dense(10)])

    model.compile(optimizer='adam', metrics=["accuracy"], 
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True))


    print("Creating callbacks...")
    #Callbacks require update and return list for communicating with dashboard
    #Model and datasets are useful for sending that data to certain modules
    config = CallbackConfig()
    labels = list(range(0,10))
    callback = DashboardCallbacks(updatelist, returnlist, model, x_train, y_train, x_test, y_test, labels, config)

    model.fit(x_train, y_train, epochs=50, callbacks=[callback])

    print("Evaluating model...")
    #This is connected to the callback so the data is sent to the dashboard
    model.evaluate(x_test, y_test, batch_size=128, callbacks=[callback])

    updatelist.append(Message(MessageMode.End, {}))
    print("Exiting cleanly...")
    dashboardProcess.join()
    print("Dashboard exited.")
    #This handles any extra data that the dashboard sent, such as save commands
    callback.HandleRemaingCommands()

if __name__ == '__main__':
    run()
```

## Other guides:
 - [Customizing the Dashboard](Guides/Customization.md)
 - [Creating a Custom Module](Guides/CustomModule.md)
 - [Creating Custom Callbacks (advanced)](Guides/CustomCallbacks.md)
 - [Module Documentation]
 - [Data Structure Documentation]
 - [Primary Functions Documentation]
 
# Data Structure Info
All data is sent in packets containing a data type (int) and data body (dict).

All data going to the modules is appended to update list. This occurs in the DashboadCallbacks class.
Modules are countinually sent the updates through their update function. The dashboard will 
automatically remove packets once all modules have recieved them.

All data coming from the modules is appended to the return list. This can occur
at the end of the update function or from the initialRequest function. This data is handled inside DashbaordCallbacks
and is only removed once it has been processed.

#### Examples:
Sending data from updates:

```python
from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message, MessageMode
import copy


class ControlButtons(Module):
    def __init__(self, ax, config):
        """Contains buttons to stop training and save model"""
        super().__init__(ax, config, "Control Buttons", noticks=True)
        self.stopbutton = createButtonWithingAxes(self.ax, 0.2, 0.2, 0.2, 0.1, "Stop Training")
        self.savebutton = createButtonWithingAxes(self.ax, 0.5, 0.2, 0.2, 0.1, "Save Model")
        self.stopbutton.on_clicked(self.stopFunc)
        self.savebutton.on_clicked(self.saveFunc)

        self.internalreturnlist: list[Message] = []

    def update(self, data: Message):
        out = copy.deepcopy(self.internalreturnlist)
        self.internalreturnlist = []
        return out

    def stopFunc(self, event):
        if event == event:
            pass
        self.internalreturnlist.append(Message(MessageMode.Command, {'command': 'stop'}))

    def saveFunc(self, event):
        if event == event:
            pass
        self.internalreturnlist.append(Message(MessageMode.Command, {'command': 'save'}))
```

Sending data from initialRequest:

```python
from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.MLCommunicationBackend import Message, MessageMode


class TrainingSetSampleImages(ImageModule):
    def __init__(self, ax, config):
        super().__init__(ax, config, "Training Set Sample Images")

    def initialRequests(self):
        return [Message(MessageMode.Train_Set_Sample, {"num": self.config['rows'] * self.config['cols']})]

    def update(self, data):
        if data.body == MessageMode.Train_Set_Sample:
            print(data)
```

# Tutorials


# Classes:
## Dashboard
Dashboard is a class that handles high level matplotlib interaction and sends data to sub modules.
A dashboard is created in a seperate process and communicates using updatelist
and returnlist. The createDashboard function makes this easier.

## Module
Module is the base class for graphical modules that can be added to the dashboard.
Modules are created automatically when the dashboard loads.

Parameters:
- ax: matplotlib axes for the module to render in
- config: dict containing config info, can be {}
- title: title to appear above plot
- noticks (optional): remove tick marks from plot, default = False
- reqkeys (optional): required keys in config dict, default = None

Functions:
- \_\_init__(): creates module
- update(data): updates module with data
- initialRequest(): allows module to request data before dashboard loads

All functions are called automatically from dashboard.

## Image Module

ImageModule inherits from module and contains some functions to make handling
images easier.

# Module Info
TODO - all module info