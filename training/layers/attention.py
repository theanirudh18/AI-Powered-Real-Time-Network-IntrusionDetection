import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense


class BahdanauAttention(Layer):

    def __init__(self, units=128, **kwargs):
        super(BahdanauAttention, self).__init__(**kwargs)

        self.units = units

        self.W1 = Dense(units)

        self.W2 = Dense(units)

        self.V = Dense(1)

    def call(self, values):

        score = self.V(

            tf.nn.tanh(

                self.W1(values)

                +

                self.W2(values)

            )

        )

        attention_weights = tf.nn.softmax(

            score,

            axis=1

        )

        # Stored for explainability — read after predict() to see which
        # timesteps (features) the model focused on for the last prediction.
        self.last_attention_weights = attention_weights

        context_vector = attention_weights * values

        context_vector = tf.reduce_sum(

            context_vector,

            axis=1

        )

        return context_vector

    def get_config(self):

        config = super().get_config()

        config.update({

            "units": self.units

        })

        return config