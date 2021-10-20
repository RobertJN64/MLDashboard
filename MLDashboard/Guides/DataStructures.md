# Data Structures

!["ALT TEXT"](DataStructuresDiagram.png)

## Config

Dashboard config is loaded in the `createDashboard()` function.
Global config is combined with each module config and sent to the module
as a param in the `__init__()` function. Required keys can be specified
in the module code.

Callback config is sent to the dashboard callbacks in the `__init__()`
function. It controls when data is sent.

## Training

Data is sent from the training to the dashboard callbacks by tensorflow.
`model.fit(callbacks=[dashboardCallback])`

## Callbacks

Data is sent between the callbacks and the dashboard using multiprocessing
lists: `updateList` and `returnList`

## Dashboard

The dashboard sends all updates in `updateList` to each module. It recieves
data from each module and sends it back to the callbacks in `returnList`.

## Modules

Each module recieves data in the `update()` function. It can return data
from the `update()` function or the `initialRequest()` function.

### Example:
```python
from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.MLCommunicationBackend import MessageMode

class TrainingSetSampleImages(ImageModule):
    def __init__(self, ax, config):
        super().__init__(ax, config, str("Training Set Sample Images"), MessageMode.Train_Set_Sample)

    def initialRequests(self):
        return self.generateRequest() #built in from ImageModule

    def update(self, data):
        if data.mode == MessageMode.Train_Set_Sample:
            images = self.createImages(data.body['x'])
            text = data.body['y']
            self.updateImageGrid(images, text)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return self.generateRequest()
```