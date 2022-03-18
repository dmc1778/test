    base_anchor = keras.backend.cast([-base_size / 2, -base_size / 2, base_size / 2, base_size / 2], keras.backend.floatx())
    anchors = keras.backend.round(anchors)