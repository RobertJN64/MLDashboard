# Creating a Custom Module
Modules are designed to be easy for the user to create.
Although many modules are included already, sometimes a specific use case
needs a custom module to be created.

All modules must inherit from the base class module.
This can be directly or indirectly through sub classes such as ImageModule.
A module must provide an init function and an update function. If necessary, initialRequest can be used as well.
More information on these functions can be found in the Module info under Classes.

Modules should interact with matplotlib using their ax class.

#### Example:
```python
from MLDashboard.DashboardModules.Module import Module

class MyModule(Module):
    def __init__(self, ax, config):
        super().__init__(ax, config, "My Module", noticks=True)
        #Add more init code here

    def update(self, data):
        pass
        #Code to run on update here
```

To register your module, add this code in your main script.
```python
import MyModule
from MLDashboard.MLDashboardBackend import allModules

allModules["MyModule"] = MyModule
```

When a module is created these options can be configured:
 - ax: The ax that the dashboard passes in (stored in self.ax)
 - config: The config that the dashboard passes in (stored in self.config)
 - title: The title that will appear on the dasboard
 - noticks: Removes tick marks from plot (default: False)
 - reqkeys: Keys that must be in config (default: None)

## Image Modules
If a module deals with images, it should inherit from ImageModule.

Image modules contain predefined functions for making image handling easier.
These include:
 - generateRequest(): returns a Message object if the module should request more images
 - createImages(): turns arrays into PIL images
 - updateImageGrid(): shows images in a grid and updates images and text if needed
 
Backend functions:
 - compareImages(): returns True if 2 images are the same
 - shouldRequest(): returns True if a request is needed
 - displayImage(): creates an image axes

To support these functions, image modules have different inital config:
 - ax: The ax that the dashboard passes in (stored in self.ax)
 - config: The config that the dashboard passes in (stored in self.config)
 - title: The title that will appear on the dasboard
 - __datarequesttype: Message object that labels data requests__
 - __reqkeys: Keys that must be in config in addition to:
["width", "height", "rows", "cols", "refreshrate"] (default: None)__

Config explanation:
 - width: width of image in pixels
 - height: height of image in pixels
 - rows: number of image rows
 - cols: number of image cols
 - refreshrate: how often to request more images
 - conversion (default: 'L'): PIL conversion for images (defaults to greyscale)
 - cmap (default: 'gray'): Matplotlib color mapping

## Example
```python
from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.MLCommunicationBackend import MessageMode

class TrainingSetSampleImages(ImageModule):
    def __init__(self, ax, config):
        super().__init__(ax, config, "Training Set Sample Images", MessageMode.Train_Set_Sample)

    def initialRequests(self):
        return self.generateRequest()

    def update(self, data):
        if data.mode == MessageMode.Train_Set_Sample:
            images = self.createImages(data.body['x'])
            text = data.body['y']
            self.updateImageGrid(images, text)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return self.generateRequest()
```

More examples of how modules are structured can be found by looking in DashboardModules.