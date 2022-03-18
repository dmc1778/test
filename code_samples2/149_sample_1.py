    old_layer = keras.layers.MaxPool1D(pool_length=2, border_mode='valid', name='maxpool1d')
    new_layer = keras.layers.MaxPool1D(pool_size=2, padding='valid', name='maxpool1d')
    new_layer = keras.layers.MaxPool1D(pool_size=2, padding='valid', name='maxpool1d')
    old_layer = keras.layers.AvgPool1D(pool_length=2, border_mode='valid', name='d')