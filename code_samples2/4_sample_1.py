        assert memoryview(c).strides == (800, 80, 8)
        assert memoryview(fortran).strides == (8, 80, 800)