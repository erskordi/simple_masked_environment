import numpy as np
import gym
from gym import spaces

class ToyEnv(gym.Env):

    def __init__(self, previous_state):
        
        """
        No-terminal states: 0 - 9
        Terminal states 10 - 13

        Possible transits:
        0: (0,10), (0,1)
        1: (1,2), (1,0)
        2: (2,1), (2,8), (2,3), (2,9)
        3: (3,2), (3,4)
        4: (4,3), (4,5)
        5: (5,4), (5,6)
        6: (6,5), (6,12)
        7: (7,13), (7,8)
        8: (8,7), (8,2)
        9: (9,2), (9,11)
        """

        self.transits = {
            0: [1,10],
            1: [0,2],
            2: [1,3,8,9],
            3: [2,4],
            4: [3,5],
            5: [4,6],
            6: [5,12],
            7: [8,13],
            8: [2,7],
            9: [2,11],
            10: [],
            11: [],
            12: [],
            13: [],
        }

        self.non_terminal_states = list(range(10))
        self.terminal_states = list(range(10,14))
        self.visited_states = []
        self.previous_state = previous_state
        self.next_obs = None
        self.potential_transits = None

        observation_space = {
            "action_mask": spaces.Box(0,1,shape=(10,)),
            "obs": spaces.Discrete(10)
        }

        self.observation_space = spaces.Dict(observation_space)
        self.action_space = spaces.Discrete(14)

    def reset(self):
        self.visited_states = []
        init_obs = self.previous_state#np.random.randint(self.observation_space["obs"].n)
        self.potential_transits = self.transits[init_obs]
        init_action_mask = np.zeros(self.action_space.n, dtype=np.uint8)
        init_action_mask[self.potential_transits] = 1

        self.visited_states.append(init_obs)
        #self.previous_state = init_obs

        init_state = {
            "action_mask": init_action_mask,
            "obs": init_obs
        }

        self.next_obs = init_obs

        return init_state

    def step(self, action):
        obs = self._get_state(action)
        self.next_obs = obs["obs"]

        reward = self._get_reward(obs["obs"])
        done = self._is_terminal()

        return obs, reward, done, {}

    def _get_state(self, action):
        self.potential_transits = self.transits[action]
        action_mask = np.zeros(self.action_space.n, dtype=np.uint8)

        for i in self.potential_transits:
            if i not in self.visited_states:
                action_mask[i] = 1
        
        self.visited_states.append(action)
        #self.previous_state = action

        state = {
            "action_mask": action_mask,
            "obs": action
        }

        return state
    
    def _get_reward(self, state):

        if state in self.terminal_states:
            reward = 100
        else:
            reward = -1
        
        return reward
    
    def _is_terminal(self):

        if self.next_obs in self.terminal_states:
            done = True
        else:
            done = False

        return done

if __name__ == "__main__":

    num_episodes = 10
    previous_state = np.random.randint(10)
    print("first:{}".format(previous_state))
    env = ToyEnv(previous_state=previous_state)

    for _ in range(num_episodes):
        obs = env.reset()
        done = False
        step = 0

        avail_actions = np.where(obs["action_mask"] > 0)[0]
        
        while not done:
            action = np.random.choice(avail_actions)
            obs, rew, done, _ = env.step(action)
            avail_actions = np.where(obs["action_mask"] > 0)[0]
            print("obs:{}, reward:{}, done:{}".format(obs,rew,done))
            step += 1
   
