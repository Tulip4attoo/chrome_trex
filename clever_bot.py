import numpy as np
import time

import capturing_objects


URL = "http://www.trex-game.skipser.com/"

clever_params = {'b2': np.array([[ 0.27304736]]), 'W2': np.array([[ 0.91572382, -0.29862268,  0.30955728]]), 'W1': np.array([[-0.02062025,  0.00016742,  0.00381535],
       [ 0.00226537,  0.01325698,  0.02389935],
       [ 0.02300561,  0.01351209,  0.00588823]]), 'b1': np.array([[-0.73119972],
       [-0.05157346],
       [-0.00290758]])}

capturing_objects.chrome_setup(URL)
time.sleep(3)
capturing_objects.play_game(clever_params)
