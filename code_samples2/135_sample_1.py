    cgamma = np.conj(gamma)
    e2phidelta = np.exp(1j * (2 * phi + delta))
    eiphi = np.exp(1j * phi)
    eidelta = np.exp(-1j * delta)
        -0.5 * np.abs(gamma) ** 2 - 0.5 * cgamma ** 2 * e2phidelta * tanhr
            cgamma * e2phidelta * tanhr + gamma,
            -cgamma * eiphi/ coshr,
            [e2phidelta * tanhr, -eiphi / coshr],
            [-eiphi / coshr, -eidelta * tanhr],