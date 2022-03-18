        v = tf.eye(n, m, dtype=dtype, name=name)
        if py_all(v.shape.as_list()):
            return variable(v, dtype=dtype, name=name)
        return v