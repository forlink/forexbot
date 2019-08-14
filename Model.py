import tensorflow as tf
class Model:
    def __init__(self, train_dataset, test_dataset):
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Flatten())
        self.model.add(tf.keras.layers.Dense(200, activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dropout(0.2))
        self.model.add(tf.keras.layers.Dense(50, activation=tf.nn.softmax))
        self.model.add(tf.keras.layers.Dropout(0.2))
        self.model.add(tf.keras.layers.Dense(2, activation=tf.nn.softmax))
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(train_dataset.x, train_dataset.y, epochs=3, validation_data=(test_dataset.x, test_dataset.y))