import tensorflow as tf
import time


class Model:
    BATCH_SIZE = 64
    EPOCHS = 10
    NAME = "{}".format(int(time.time()))
    def __init__(self, train_dataset, test_dataset):

        self.model = tf.keras.models.Sequential()

        self.model.add(tf.keras.layers.CuDNNLSTM(128, input_shape = (train_dataset.x.shape[1:]), return_sequences = True))
        self.model.add(tf.keras.layers.Dropout(0.2))
        self.model.add(tf.keras.layers.BatchNormalization())

        self.model.add(tf.keras.layers.CuDNNLSTM(128, input_shape=(train_dataset.x.shape[1:]), return_sequences=True))
        self.model.add(tf.keras.layers.Dropout(0.1))
        self.model.add(tf.keras.layers.BatchNormalization())

        self.model.add(tf.keras.layers.CuDNNLSTM(128, input_shape=(train_dataset.x.shape[1:])))
        self.model.add(tf.keras.layers.Dropout(0.2))
        self.model.add(tf.keras.layers.BatchNormalization())

        self.model.add(tf.keras.layers.Dense(32, activation="relu"))
        self.model.add(tf.keras.layers.Dropout(0.2))

        self.model.add(tf.keras.layers.Dense(2, activation="softmax"))

        opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

        self.model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        tensorboard = tf.keras.callbacks.TensorBoard(log_dir='logs/{}'.format(self.NAME))
        filepath = "RNN_Final-{epoch:02d}-{val_acc:.3f}"
        checkpoint = tf.keras.callbacks.ModelCheckpoint("models/{}.model".format(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max'))

        histroy = self.model.fit(
            train_dataset.x, train_dataset.y,
            epochs=self.EPOCHS,
            batch_size=self.BATCH_SIZE,
            validation_data=(test_dataset.x, test_dataset.y),
            callbacks=[tensorboard, checkpoint]
        )