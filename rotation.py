from scipy.spatial.transform import Rotation as R
import numpy as np


r = R.from_rotvec(np.deg2rad(0.1) * np.array([1, -1, 0]))
print(r.as_euler("zxz",degrees=True))

#test1