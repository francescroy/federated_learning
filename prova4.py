

import numpy as np

exemple_1 = [1,2,3,4,5]
exemple_2 = [1,2,3,4,5]

exemple_1 = np.array(exemple_1[-3::])
exemple_2 = np.array(exemple_2[-3::])

exemple_3 = exemple_1 + exemple_2

print(exemple_3)