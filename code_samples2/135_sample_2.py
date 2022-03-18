    exp2phidelta = np.exp(1j * (2 * phi + delta))
    eiphi = np.exp(1j * phi)
    cgamma = np.conj(gamma)
        -0.5 * np.abs(gamma) ** 2 - 0.5 * cgamma ** 2 * exp2phidelta * tanhr
            cgamma * exp2phidelta * tanhr + gamma,
            -cgamma * eiphi / coshr,
            [exp2phidelta * tanhr, -eiphi / coshr],
            [-eiphi / coshr, -np.exp(-1j * delta) * tanhr],