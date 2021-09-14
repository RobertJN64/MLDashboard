import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
import tensorflow as tf
from tensorflow import keras
import MLDashboard.MLDashboardBackend as MLDashboardBackend
from MLDashboard.CommunicationBackend import Message, MessageMode
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

def run():
    print("Starting interactive dashboard demo...")
    print("Setting up dashboard...")

    #Create dashboard and return communication tools (this starts the process)
    dashboardProcess, updatelist, returnlist = MLDashboardBackend.createDashboard(config='dashboarddemo.json')

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
    callback = MLDashboardBackend.DashboardCallbacks(updatelist, returnlist, model, x_train, y_train, x_test, y_test)

    print("Starting training...")
    trainingstarttime = time.time()
    model.fit(x_train, y_train, epochs=50, callbacks=[callback])
    print("Training finished in: ", round(time.time() - trainingstarttime, 3), " seconds.")

    print("Evaluating model...")
    res = model.evaluate(x_test, y_test, batch_size=128)
    #This data is sent to the dashboard
    updatelist.append(Message(MessageMode.Evaluation, dict(zip(model.metrics_names, res))))

    updatelist.append(Message(MessageMode.End, {}))
    print("Exiting cleanly...")
    dashboardProcess.join()
    print("Dashboard exited.")
    #This handles any extra data that the dashboard sent, such as save commands
    MLDashboardBackend.HandleRemaingCommands(returnlist, model)

if __name__ == '__main__':
    run()