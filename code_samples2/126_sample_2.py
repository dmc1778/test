        timesteps = np.array([date], dtype='datetime64[s]')[0].astype(np.int64)
        assert_equal(x[0].astype(np.int64), 322689600000000000)