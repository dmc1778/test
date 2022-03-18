    def tensor1d(min_len=1, max_len=64, dtype=np.float32, elements=None, nonzero=False):
        return HypothesisUtil.tensor(1, 1, dtype, elements, nonzero, min_value=min_len, max_value=max_len)