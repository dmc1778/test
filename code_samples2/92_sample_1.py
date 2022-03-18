        X = np.random.normal(loc=center, scale=noise, size=(n_samples, 2))
        y = np.repeat(lbl, n_samples).tolist()