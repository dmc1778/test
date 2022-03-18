      # Use conv2d instead of fully_connected layers.
      fc6 = slim.conv2d(pool5, 4096, [7, 7], padding='VALID', scope='fc6')
      fc7 = slim.conv2d(fc6, 4096, [1, 1], scope='fc7')