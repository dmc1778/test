        part = np.rollaxis(part, axis, part.ndim)
        n = np.isnan(part[..., -1])
        if rout.ndim == 0:
            if n == True:
                warnings.warn("Invalid value encountered in median",
                              RuntimeWarning, stacklevel=3)
                if out is not None:
                    out[...] = a.dtype.type(np.nan)
                    rout = out
                else:
                    rout = a.dtype.type(np.nan)
        elif np.count_nonzero(n.ravel()) > 0:
            warnings.warn("Invalid value encountered in median for" +
                          " %d results" % np.count_nonzero(n.ravel()),
                          RuntimeWarning, stacklevel=3)
            rout[n] = np.nan
        return rout