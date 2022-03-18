        z = np.correlate(self.x, self.y, 'full', old_behavior=self.old_behavior)
        z = np.correlate(self.y, self.x, 'full', old_behavior=self.old_behavior)
        assert_array_almost_equal(z, self.z2)
        z = np.correlate(self.x, self.y, 'full', old_behavior=self.old_behavior)
        z = np.correlate(self.y, self.x, 'full', old_behavior=self.old_behavior)
        assert_array_almost_equal(z, self.z2)
    old_behavior = True