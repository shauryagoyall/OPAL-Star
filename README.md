# A2C

## To run:

    python main.py --algo "opal" --env-name "ALE/Breakout-v5" --num-processes 1
    
Changes from main (my reference mainly):

vanilla a2c code:

    from envs.py removed atari_env in \
    is_atari = hasattr(gym.envs, 'atari') and isinstance( \
                env.unwrapped, gym.envs.atari.atari_env.AtariEnv) 

sb3 package:

    File "C:\Users\91845\anaconda3\lib\site-packages\stable_baselines3\common\atari_wrappers.py", line 36, in reset 
        noops = self.unwrapped.np_random.randint(1, self.noop_max + 1) 
    AttributeError: 'numpy.random._generator.Generator' object has no attribute 'randint' 

    #make np_random.randint(1, self.noop_max + 1) to np_random.integers(1, self.noop_max + 1)

## To Edit:

Major: CNNBase from model.py in a2c...   folder \
Minor: pytorch.save(...       from main.py




## Incomplete Requirements 

* Python 3 
* [PyTorch](http://pytorch.org/)
* [Stable baselines3](https://github.com/DLR-RM/stable-baselines3)
* OpenCV

In order to install requirements, follow:

```bash
# PyTorch
from the pytorch website

# Other requirements
pip install -r requirements.txt

# Gym Atari
conda install -c conda-forge gym-atari
```

