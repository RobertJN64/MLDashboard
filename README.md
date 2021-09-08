# Getting Started

This guide assumes you already understand python and tensorflow.

## Installation
```commandline
pip install git+https://github.com/RobertJN64/MLDashboard
```

## Integration
The dashboard can easily by added to an existing machine learning project.
Import the dashboard as shown.
```python
from MLDashboard.MLDashboardBackend import createDashboard, DashboardCallbacks, HandleRemaingCommands
from MLDashboard.CommunicationBackend import Message, MessageMode
```

Before training starts, create the dashboard.
```python
dashboardProcess, updatelist, returnlist = createDashboard()
```

Connect the callbacks to your training.
```python
model.fit(x_train, y_train, epochs=10,
        callbacks=[DashboardCallbacks(updatelist, returnlist, model, x_train, y_train, x_test, y_test)]
    )
```

After training ends, you can send evaluation stats to the dashboard.
```python
res = model.evaluate(x_test, y_test, batch_size=128)
updatelist.append(Message(MessageMode.Evaluation, dict(zip(model.metrics_names, res))))
```

To exit the dashboard cleanly, use the following code:
```python
updatelist.append(Message(MessageMode.End, {}))
print("Exiting cleanly...")
dashboardProcess.join()
print("Dashboard exited.")
HandleRemaingCommands(returnlist, model)
```

InteractiveDashboardDemo shows a full example.

## Customization
The modules shown in the dashboard can be changed in the dashboard.json file, or by specifying a new config file
in createDashboard().

A properly formatted dashboard.json file should look like this.
```json
{
  "modules": [
    [
       ["LossMetricsGraph", {}],
       ["LossMetricsNumerical", {}],
       ["TrainingSetSampleImages",
          {"width": 28,
           "height": 28,
           "rows": 2,
           "cols": 4}]
    ],
    [
       ["StatusModule", {}],
       ["ControlButtons", {}],
       ["EmptyModule", {}]
    ]
  ]
}
```
This creates a dashboard with 2 rows of 3 cols. The dict after the module name contains config info.

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
from MLDashboard.CommunicationBackend import Message, MessageMode
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
from MLDashboard.CommunicationBackend import Message, MessageMode

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
## Creating a Custom Module
All modules must inherit from the base class module. This can be directly or indirectly through sub classes such as ImageModule.
A module must provide an init function and an update function. If necessary, initialRequest can be used as well.
More information on these functions can be found in the Module info under Classes.

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

More examples can be found by looking in DashboardModules.

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