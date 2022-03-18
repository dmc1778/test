    # 增加av。分母boxes2[..., 3]可能为0，所以加上除0保护防止nan。
    atan1 = tf.atan(boxes1[..., 2] / boxes1[..., 3])
    temp_a = K.switch(boxes2[..., 3] > 0.0, boxes2[..., 3], boxes2[..., 3] + 1.0)
    atan2 = tf.atan(boxes2[..., 2] / temp_a)