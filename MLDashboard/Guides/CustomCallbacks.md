# Custom Callbacks

Note: this is an advanced guide. Most use of the dashboard should
not require creating custom callbacks.

A custom callback must inherit from the DashboardCallbacks class.

These callbacks have properties that can be accessed from self:
 - updatelist: send data to modules
 - self.returnlist: recieve data from modules
 - self.model = keras model
 - self.x_train: dataset
 - self.y_train: dataset
 - self.x_test: dataset
 - self.y_test: dataset
 - self.predictionlabels: labels for y in datasets
 - self.config: CallbackConfig class

To interact with the callbacks, you can override a 'custom_on' function.

For example:
```python
from MLDashboard.MLCallbacksBackend import DashboardCallbacks
class myCustomCallback(DashboardCallbacks):
    def __init__(self, updatelist, returnlist, model, x_train, y_train, x_test, y_test, labels, config):
        super().__init__(updatelist, returnlist, model, x_train, y_train, x_test, y_test, labels, config)

    def custom_on_test_begin(self, logs):
        print("We are beginning the evaluation step.")
```

These custom functions are called after main data handling.

Changing flags in CallbackConfig can also adjust callback behavior.
The defaults are recommended to avoid sending too much data, but they can be changed.