        totlist = np.logical_or.reduce(condlist, axis=0)
        # Only able to stack vertically if the array is 1d or less
        if x.ndim <= 1:
            condlist = np.vstack([condlist, ~totlist])
        else:
            condlist = [asarray(c, dtype=bool) for c in condlist]
            totlist = condlist[0]
            for k in range(1, n):
                totlist |= condlist[k]
            condlist.append(~totlist)