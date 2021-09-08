from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.CommunicationBackend import Message, MessageMode

class TrainingSetSampleImages(ImageModule):
    def __init__(self, ax, config):
        """
        Shows a set of sample images from the training set.

        :param ax: matplotlib ax
        :param config: Config info with the keys width and height for the image and rows and cols for the plot
        """
        super().__init__(ax, config, "Training Set Sample Images")

    def initialRequests(self):
        return [Message(MessageMode.Train_Set_Sample, {"num": self.config['rows'] * self.config['cols']})]

    def update(self, data):
        if data.body == MessageMode.Train_Set_Sample:
            print(data)
