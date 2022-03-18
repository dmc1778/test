    return tf.select(tf.random_uniform(shape, dtype=dtype, seed=seed) <= p,
                     tf.ones(shape, dtype=dtype),
                     tf.zeros(shape, dtype=dtype))