        assert_(memoryview(c).strides == (800, 80, 8))
        assert_(memoryview(fortran).strides == (8, 80, 800))