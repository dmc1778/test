        y = np.reshape(y, (-1, yshape[-1]))  # for time-distributed data, collapse time and sample
        return np.reshape(class_weights, yshape[:-1] + (1,))  # uncollapse initial dimensions