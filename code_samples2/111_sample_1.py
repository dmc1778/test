#https://stackoverflow.com/questions/7821518/matplotlib-save-plot-to-numpy-array
import numpy as np
ax=plt.gca()
fig.canvas.draw()
# Now we can save it to a numpy array.
data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
writer.add_image('matplotlib', data)
writer.close()