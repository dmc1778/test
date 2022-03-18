    axes = [1, 0] + range(2, len(outputs.get_shape()))
    outputs = tf.transpose(outputs, axes)