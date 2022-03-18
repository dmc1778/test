        processed = tf.reshape(processed, (B, T, H, W, C))
        if self.build_cell is None:
            return processed