                next_max_action = tf.one_hot(tf.squeeze(next_max_action), self.a_counts, 1., 0., dtype=tf.float32)  # [B, A]
                _next_max_action = tf.reshape(tf.tile(next_max_action, [self.target_quantiles, 1]), [self.target_quantiles, -1, self.a_counts])  # [B, A] => [N'*B, A] => [N', B, A]