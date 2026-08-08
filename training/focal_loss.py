import tensorflow as tf


class SparseCategoricalFocalLoss(tf.keras.losses.Loss):

    def __init__(self, gamma=2.0, alpha=0.25, **kwargs):
        super().__init__(**kwargs)
        self.gamma = gamma
        self.alpha = alpha

    def call(self, y_true, y_pred):

        y_true = tf.cast(y_true, tf.int32)

        if len(y_true.shape) > 1:
            y_true = tf.squeeze(y_true, axis=-1)

        y_true_one_hot = tf.one_hot(
            y_true,
            depth=tf.shape(y_pred)[-1]
        )

        epsilon = tf.keras.backend.epsilon()

        y_pred = tf.clip_by_value(
            y_pred,
            epsilon,
            1.0 - epsilon
        )

        cross_entropy = -tf.reduce_sum(
            y_true_one_hot * tf.math.log(y_pred),
            axis=-1
        )

        p_t = tf.reduce_sum(
            y_true_one_hot * y_pred,
            axis=-1
        )

        focal_loss = (
            self.alpha
            * tf.pow(1.0 - p_t, self.gamma)
            * cross_entropy
        )

        return tf.reduce_mean(focal_loss)

    def get_config(self):

        return {
            "gamma": self.gamma,
            "alpha": self.alpha
        }