    try:
        return tf.stack(x)
    except AttributeError:
        return tf.pack(x)