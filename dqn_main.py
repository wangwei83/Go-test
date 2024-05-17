
from tkinter import *
from tkinter.ttk import *
import copy
import tkinter.messagebox

class Application(Tk):
    def __init__(self, my_mode_num=9):
        Tk.__init__(self)
        self.mode_num = my_mode_num
        self.size = 1.8
        self.dd = 360 * self.size / (self.mode_num - 1)
        self.p = 1 if self.mode_num == 9 else (2/3 if self.mode_num == 13 else 4/9)
        self.positions = [[0 for i in range(self.mode_num + 2)] for i in range(self.mode_num + 2)]
        for m in range(self.mode_num + 2):
            for n in range(self.mode_num + 2):
                if (m * n == 0 or m == self.mode_num + 1 or n == self.mode_num + 1):
                    self.positions[m][n] = -1
        self.last_3_positions = copy.deepcopy(self.positions)
        self.last_2_positions = copy.deepcopy(self.positions)
        self.last_1_positions = copy.deepcopy(self.positions)
        self.cross_last = None
        self.present = 0
        self.stop = True
        self.regretchance = 0
        self.photoW = PhotoImage(file = "./Pictures/W.png")
        self.photoB = PhotoImage(file = "./Pictures/B.png")
        self.photoBD = PhotoImage(file = "./Pictures/BD-" + str(self.mode_num) + ".png")
        self.photoWD = PhotoImage(file = "./Pictures/WD-" + str(self.mode_num) + ".png")
        self.photoBU = PhotoImage(file = "./Pictures/BU-" + str(self.mode_num) + ".png")
        self.photoWU = PhotoImage(file = "./Pictures/WU-" + str(self.mode_num) + ".png")
        self.photoWBU_list = [self.photoBU, self.photoWU]
        self.photoWBD_list = [self.photoBD, self.photoWD]
        self.geometry(str(int(600 * self.size)) + 'x' + str(int(400 * self.size)))
        self.canvas_bottom = Canvas(self, bg='#369', bd=0, width=600 * self.size, height=400 * self.size)
        self.canvas_bottom.place(x=0, y=0)
        self.startButton = Button(self, text='开始游戏', command=self.start)
        self.startButton.place(x=480 * self.size, y=200 * self.size)
        self.passmeButton = Button(self, text='弃一手', command=self.passme)
        self.passmeButton.place(x=480 * self.size, y=225 * self.size)
        self.regretButton = Button(self, text='悔棋', command=self.regret)
        self.regretButton.place(x=480 * self.size, y=250 * self.size)
        self.regretButton['state'] = DISABLED
        self.replayButton = Button(self, text='重新开始', command=self.reload)
        self.replayButton.place(x=480 * self.size, y=275 * self.size)
        self.newGameButton1 = Button(self, text=('十三' if self.mode_num == 9 else '九') + '路棋', command=self.newGame1)
        self.newGameButton1.place(x=480 * self.size, y=300 * self.size)
        self.newGameButton2 = Button(self, text=('十三' if self.mode_num == 19 else '十九') + '路棋', command=self.newGame2)
        self.newGameButton2.place(x=480 * self.size, y=325 * self.size)
        self.quitButton = Button(self, text='退出游戏', command=self.quit)
        self.quitButton.place(x=480 * self.size, y=350 * self.size)
        self.canvas_bottom.create_rectangle(0 * self.size, 0 * self.size, 400 * self.size, 400 * self.size, fill='#c51')
        self.canvas_bottom.create_rectangle(20 * self.size, 20 * self.size, 380 * self.size, 380 * self.size, width=3)
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                self.oringinal = self.canvas_bottom.create_oval(200 * self.size - self.size * 2, 200 * self.size - self.size * 2,
                200 * self.size + self.size * 2, 200 * self.size + self.size * 2, fill='#000')
                self.canvas_bottom.move(self.oringinal, m * self.dd * (2 if self.mode_num == 9 else (3 if self.mode_num == 13 else 6)),
                n * self.dd * (2 if self.mode_num == 9 else (3 if self.mode_num == 13 else 6)))
        for i in range(1, self.mode_num - 1):
            self.canvas_bottom.create_line(20 * self.size, 20 * self.size + i * self.dd, 380 * self.size, 20 * self.size + i * self.dd, width=2)
            self.canvas_bottom.create_line(20 * self.size + i * self.dd, 20 * self.size, 20 * self.size + i * self.dd, 380 * self.size, width=2)
        self.pW = self.canvas_bottom.create_image(500 * self.size + 11, 65 * self.size, image=self.photoW)
        self.pB = self.canvas_bottom.create_image(500 * self.size - 11, 65 * self.size, image=self.photoB)
        self.canvas_bottom.addtag_withtag('image', self.pW)
        self.canvas_bottom.addtag_withtag('image', self.pB)
        self.canvas_bottom.create_text(500 * self.size + 11, 90 * self.size, text='后手棋', fill='#FFF')
        self.canvas_bottom.create_text(500 * self.size - 11, 90 * self.size, text='先手棋', fill='#FFF')
        self.able = [[1 for i in range(self.mode_num)] for j in range(self.mode_num)]
        self.cross = []
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.bind('<Button-1>', self.getDown)

        # Initialize the agent
        self.env = GoEnvWrapper(board_size=self.mode_num)
        state_size = self.env.observation_space.shape[0] * self.env.observation_space.shape[1] * self.env.observation_space.shape[2]
        action_size = self.env.action_space.n
        self.agent = DQNAgent(state_size, action_size)
        self.agent.model.load_state_dict(torch.load('dqn_model.pth'))  # Load the trained model

    def getDown(self, event):
        if self.stop:
            return
        self.last_3_positions = copy.deepcopy(self.last_2_positions)
        self.last_2_positions = copy.deepcopy(self.last_1_positions)
        self.last_1_positions = copy.deepcopy(self.positions)
        p = round((event.x - 20 * self.size) / (360 * self.size) * (self.mode_num - 1)) + 1
        q = round((event.y - 20 * self.size) / (360 * self.size) * (self.mode_num - 1)) + 1
        if (p * q == 0 or p == self.mode_num + 1 or q == self.mode_num + 1 or self.positions[p][q] != 0):
            return
        self.positions[p][q] = self.present + 1
        self.cross.append(self.canvas_bottom.create_image(p * self.dd + 20 * self.size, q * self.dd + 20 * self.size,
        image=self.photoWBU_list[self.present]))
        self.canvas_bottom.addtag_withtag('image', self.cross[-1])
        self.regretchance += 1
        self.regretButton['state'] = NORMAL
        if self.regretchance > 5:
            self.regretchance = 5
        self.cross_last = self.cross[-1]
        self.present = 1 - self.present
        self.able[p - 1][q - 1] = 0

        # Use the agent to predict the next move
        state = np.reshape(self.positions, [1, state_size])
        action = self.agent.act(state)
        p = action // self.mode_num + 1
        q = action % self.mode_num + 1
        if self.positions[p][q] == 0:
            self.positions[p][q] = self.present + 1
            self.cross.append(self.canvas_bottom.create_image(p * self.dd + 20 * self.size, q * self.dd + 20 * self.size,
            image=self.photoWBU_list[self.present]))
            self.canvas_bottom.addtag_withtag('image', self.cross[-1])
            self.cross_last = self.cross[-1]
            self.present = 1 - self.present
            self.able[p - 1][q - 1] = 0

    def start(self):
        self.stop = False

    def passme(self):
        self.present = 1 - self.present

    def regret(self):
        if self.regretchance > 0 and self.cross != []:
            self.canvas_bottom.delete(self.cross[-1])
            self.cross.pop()
            self.positions = copy.deepcopy(self.last_1_positions)
            self.last_1_positions = copy.deepcopy(self.last_2_positions)
            self.last_2_positions = copy.deepcopy(self.last_3_positions)
            self.present = 1 - self.present
            self.regretchance -= 1

    def reload(self):
        self.stop = True
        self.positions = [[0 for i in range(self.mode_num + 2)] for i in range(self.mode_num + 2)]
        for m in range(self.mode_num + 2):
            for n in range(self.mode_num + 2):
                if (m * n == 0 or m == self.mode_num + 1 or n == self.mode_num + 1):
                    self.positions[m][n] = -1
        self.last_3_positions = copy.deepcopy(self.positions)
        self.last_2_positions = copy.deepcopy(self.positions)
        self.last_1_positions = copy.deepcopy(self.positions)
        self.cross = []
        self.cross_last = None
        self.present = 0
        self.stop = True
        self.regretchance = 0
        self.canvas_bottom.delete('image')
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def newGame1(self):
        self.quit()
        self.__init__(my_mode_num=(13 if self.mode_num == 9 else 9))
        self.mainloop()

    def newGame2(self):
        self.quit()
        self.__init__(my_mode_num=(19 if self.mode_num == 13 else 13))
        self.mainloop()

    def quit(self):
        self.stop = True
        if tkinter.messagebox.askokcancel('Quit', 'Do you really want to quit?'):
            self.destroy()


import gym
import gym_go
import numpy as np

class GoEnvWrapper(gym.Env):
    def __init__(self, board_size=9):
        self.env = gym.make('gym_go:go-v0', size=board_size, komi=0)
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def reset(self):
        return self.env.reset()

    def step(self, action):
        state, reward, done, info = self.env.step(action)
        return state, reward, done, info

    def render(self):
        self.env.render()

import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque

class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state)
        act_values = self.model(state)
        return torch.argmax(act_values[0]).item()

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = torch.FloatTensor(next_state)
                target = reward + self.gamma * torch.max(self.model(next_state)[0]).item()
            target_f = self.model(torch.FloatTensor(state))
            target_f[0][action] = target
            self.optimizer.zero_grad()
            loss = self.criterion(self.model(torch.FloatTensor(state)), target_f)
            loss.backward()
            self.optimizer.step()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# 声明全局变量，用于新建Application对象时切换成不同模式的游戏
global mode_num,newApp
mode_num=9
newApp=False	
if __name__=='__main__':
	# 循环，直到不切换游戏模式
	while True:
		newApp=False
		app=Application(mode_num)
		app.title('围棋')
		app.mainloop()
		if newApp:
			app.destroy()
		else:
			break