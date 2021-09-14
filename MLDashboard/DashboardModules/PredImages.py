from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.CommunicationBackend import Message, MessageMode

class PredImages(ImageModule):
    def __init__(self, ax, config):
        """
        Shows a set of sample predictions from the prediction set.

        :param ax: matplotlib ax
        :param config: Config info with the keys width and height for the image and rows and cols for the plot
        """
        super().__init__(ax, config, "Sample Predictions")

    def update(self, data):
        if data.mode == MessageMode.Pred_Sample:
            images = self.createImages(data.body['x'])
            text = data.body['y']
            self.updateImageGrid(images, text)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return [Message(MessageMode.Pred_Sample, {"num": self.config['rows'] * self.config['cols']})]