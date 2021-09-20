# Functions

This guide contains info on the main functions that the user should
interact with.

## MLDashboardBackend

### createDashboard()

Loads a dashboard in a seperate process. Returns process, updatelist, and return list.

Params:
 - config: Path to config file (default: dashboard.json)
 - waitforstart: Pauses main process until dashboard is ready (default: True)


## MLCallbacksBackend

### DashboardCallbacks

Inherits from keras.Callbacks.Callback. This contains all communication between
model training and the dashboard.

Params:
- updatelist: List from dashboard creation
- returnlist: List from dashboard creation
- model: Tensorflow model
- x_train: Training set features 
- y_train: Training set output
- x_test: Test set features
- y_test: Test set output
- prediction_labels: Allows images to be labeled with friendly text
- config: Customize when data is sent

#### Example: model.fit() with callbacks
```python
from MLDashboard.MLCallbacksBackend import DashboardCallbacks, CallbackConfig
config = CallbackConfig()
labels = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
callback = DashboardCallbacks(updatelist, returnlist, model, x_train, y_train, x_test, y_test, labels, config)
model.fit()
```

## MLCommunicationBackend

### MessageMode

Message mode is an enum with different types of messages that the dashboard should receieve
or send.

### Message

Message is a class that contains a mode and a data payload. All data going to and from
the dashboard is a Message.

#### Example: Send the dashboard the end message
```python
from MLDashboard.MLCallbacksBackend import Message, MessageMode
updatelist.append(Message(MessageMode.End, {})) #message does not need a payload
```