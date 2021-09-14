from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.CommunicationBackend import MessageMode

class PredImages(ImageModule):
    def __init__(self, ax, config):
        """
        Shows a set of sample predictions from the prediction set.

        :param ax: matplotlib ax
        :param config: Config info with the keys width and height for the image and rows and cols for the plot
        """
        super().__init__(ax, config, "Sample Predictions", MessageMode.Pred_Sample)

    def update(self, data):
        if data.mode == MessageMode.Pred_Sample:
            images = self.createImages(data.body['x'])
            text = []
            color = []
            print(data.body['pred'][0])
            for i in range(0, len(images)):
                #text.append(str(data.body['pred'][i]) + " : " + str(data.body['y'][i]))
                color.append('green')
                text.append('text')

            self.updateImageGrid(images, text, color)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return self.generateRequest()