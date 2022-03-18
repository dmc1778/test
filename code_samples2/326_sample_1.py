        assert_array_almost_equal(np.fft.fft(x)[:16], np.fft.rfft(x))
        assert_array_almost_equal(np.fft.rfft(x) / np.sqrt(30),
                                  np.fft.rfft(x, norm="ortho"))