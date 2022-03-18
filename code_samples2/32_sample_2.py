if sys.version_info.major == 2:
    from keras.backend import theano_backend as KTH
    from keras.backend import tensorflow_backend as KTF