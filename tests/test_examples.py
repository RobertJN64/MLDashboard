# Tests are hard because of multiprocessing and whatnot

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #stops agressive error message printing
import tensorflow as tf
from tensorflow import keras

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

def test_train_model():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    x_train = x_train.reshape(-1, 784).astype("float32") / 255.0
    x_test = x_test.reshape(-1, 784).astype("float32") / 255.0

    # Limit the train data to 10000 samples
    x_train = x_train[:10000]
    y_train = y_train[:10000]
    # Limit test data to 1000 samples
    x_test = x_test[:1000]
    y_test = y_test[:1000]

    model = get_model()

    model.fit(x_train, y_train, epochs=50)

    _, accuracy = model.evaluate(x_test, y_test, batch_size=128)
    assert accuracy > 0.75

# def test_main_demo():
#     import MLDashboard.Examples.InteractiveDashboardDemo as IDD
#     IDD.run(testmode=True)
#
# def test_custom_callbacks():
#     import MLDashboard.Examples.CustomCallbacksDemo as CCD
#     CCD.run(testmode=True)
#
# def test_every_module():
#     with open("MLDashboard/Examples/allmodules.json") as f:
#         with open("MLDashboard/Examples/dashboarddemo.json", 'w+') as g:
#             g.write(f.read())
#     import MLDashboard.Examples.InteractiveDashboardDemo as IDD
#     import MLDashboard.Examples.CustomCallbacksDemo as CCD
#     IDD.run(testmode=True)
#     CCD.run(testmode=True)