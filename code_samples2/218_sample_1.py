    def tensor1d(min_len=1, max_len=64, dtype=np.float32, elements=None):
        return HypothesisUtil.tensor(1, 1, dtype, elements, min_value=min_len, max_value=max_len)