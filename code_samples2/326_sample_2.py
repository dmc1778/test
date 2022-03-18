        for n in [x.size, 2*x.size]:
            for norm in [None, 'ortho']:
                assert_array_almost_equal(
                    np.fft.fft(x, n=n, norm=norm)[:(n//2 + 1)],
                    np.fft.rfft(x, n=n, norm=norm))
            assert_array_almost_equal(np.fft.rfft(x, n=n) / np.sqrt(n),
                                      np.fft.rfft(x, n=n, norm="ortho"))