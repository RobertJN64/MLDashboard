import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
import tensorflow as tf
from tensorflow import keras
from MLDashboard.MLDashboardBackend import createDashboard
from MLDashboard.MLCallbacksBackend import DashboardCallbacks, CallbackConfig
from MLDashboard.MLCommunicationBackend import Message, MessageMode
import time

def get_model():
    model = keras.Sequential(
        [keras.layers.Dense(128, activation='relu'),
         keras.layers.Dense(10)]
    )

    model.compile(
        optimizer='adam',
        loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"],
    )

    return model

def run(testmode=False):
    print("Starting interactive dashboard demo...")
    print("Setting up dashboard...")

    #Create dashboard and return communication tools (this starts the process)
    dashboardjsonfile = os.path.dirname(__file__) + '/dashboarddemo.json'
    dashboardProcess, updatelist, returnlist = createDashboard(dashboardjsonfile, openatend=not testmode)

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
    model = get_model()


    print("Creating callbacks...")
    #Callbacks require update and return list for communicating with dashboard
    #Model and datasets are useful for sending that data to certain modules
    config = CallbackConfig()
    labels = list(range(0,10))
    #labels = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    callback = DashboardCallbacks(updatelist, returnlist, model, x_train, y_train, x_test, y_test, labels, config)

    print("Starting training...")
    trainingstarttime = time.time()
    model.fit(x_train, y_train, epochs=50, callbacks=[callback])
    print("Training finished in: ", round(time.time() - trainingstarttime, 3), " seconds.")

    print("Evaluating model...")
    model.evaluate(x_test, y_test, batch_size=128, callbacks=[callback])

    updatelist.append(Message(MessageMode.End, {}))
    print("Exiting cleanly...")
    dashboardProcess.join()
    print("Dashboard exited.")
    #This handles any extra data that the dashboard sent, such as save commands
    callback.HandleRemaingCommands()

if __name__ == '__main__':
    run()