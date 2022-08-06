# Opal Star

## To run/train:

    python main.py --algo "opal" --env-name "Breakout-v0" --num-processes 16
    
    change "opal" to "a2c" to use vanilla a2c algorithm 
    it would be useful to use the --log-dir argument to set a custom directory for the log file
    
## Requirements 

* Python 3 
* [PyTorch](http://pytorch.org/)
* [Stable baselines3](https://github.com/DLR-RM/stable-baselines3)
* OpenCV
* h5py
* gym
* pybullet (for physics based and robotics simulations only, not needed here)

In order to install requirements, follow:

```bash
# PyTorch
from the pytorch website

# h5py
conda install h5py

# All other requirements
pip install stable-baselines3[extra]

```

## Visualization of training:
use visualize.ipynb file. It uses the .csv file saved in the log directory. For now, you will have to manually remove the 1st line from the .csv file before this code works

## Changes from main (my reference mainly):

vanilla a2c code:

    from envs.py removed atari_env in \
    is_atari = hasattr(gym.envs, 'atari') and isinstance( \
                env.unwrapped, gym.envs.atari.atari_env.AtariEnv) 

sb3 package:

    File "C:\Users\91845\anaconda3\lib\site-packages\stable_baselines3\common\atari_wrappers.py", line 36, in reset 
        noops = self.unwrapped.np_random.randint(1, self.noop_max + 1) 
    AttributeError: 'numpy.random._generator.Generator' object has no attribute 'randint' 

    #make np_random.randint(1, self.noop_max + 1) to np_random.integers(1, self.noop_max + 1)
