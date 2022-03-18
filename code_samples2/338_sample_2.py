model_path = os.path.join(PATH, model_path)
weights_path = os.path.join(PATH, weights_path)
labels_file_path = os.path.join(PATH, 'labels.txt')
labels = np.loadtxt(labels_file_path, delimiter='
', dtype=str)