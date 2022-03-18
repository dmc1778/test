            m = setup_sgpr()
        m.clear()
            m.kern.variance.prior = gpflow.priors.Gamma(1.4, 1.6)