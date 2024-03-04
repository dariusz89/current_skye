"""
Gymnasium custom environment
https://stable-baselines3.readthedocs.io/en/master/guide/custom_env.html
https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/#sphx-glr-tutorials-gymnasium-basics-environment-creation-py
"""
import gymnasium as gym
import numpy as np
from gymnasium import spaces

class SnakeEnv(gym.Env):
    """Custom Environment that follows gym interface."""
    metadata = {"render_modes": None}

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(5,),
            dtype=np.uint8,
            seed=1
        )

    def __get_obs(self):

        return {}

    def __get_info(self):

        return {}

    def reset(self, **kwargs):
        super().reset(**kwargs)
        observation = self.__get_obs()
        info = self.__get_info()
        return observation, info

    def step(self, action):
        observation = self.__get_obs()
        reward = action # just placeholder for now, implement later
        terminated = False
        truncated = False
        info = self.__get_info()

        return observation, reward, terminated, truncated, info

    def render(self):
        pass
