# Getting Started

This guide assumes you already understand python and tensorflow.

## Installation
```
pip install MLDashboard
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
 - [Customizing the Dashboard](MLDashboard/Guides/Customization.md)
 - [Creating a Custom Module](MLDashboard/Guides/CustomModules.md)
 - [Creating Custom Callbacks (advanced)](MLDashboard/Guides/CustomCallbacks.md)
 - [Module Documentation](MLDashboard/Guides/Modules.md) Coming soon!
 - [Data Structure Documentation](MLDashboard/Guides/DataStructures.md)
 - [Primary Functions Documentation](MLDashboard/Guides/Functions.md)