    def setUp(self):
        X = np.random.randn(1000, 3)
        Y = np.random.randn(1000, 3)
        Z = np.random.randn(100, 3)
        self.m = gpflow.models.SGPR(X, Y, Z=Z, kern=gpflow.kernels.RBF(3))
            m = self.m
            m.compile()