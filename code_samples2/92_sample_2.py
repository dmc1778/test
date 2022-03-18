        X = np.random.normal(loc=center, scale=noise, size=(samples, 2))
        y = np.repeat(lbl, samples).tolist()