def setup_sgpr():
    X = np.random.randn(1000, 3)
    Y = np.random.randn(1000, 3)
    Z = np.random.randn(100, 3)
    return gpflow.models.SGPR(X, Y, Z=Z, kern=gpflow.kernels.RBF(3))
            m = setup_sgpr()