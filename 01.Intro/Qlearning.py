import numpy as np

BOARD_ROWS = 3 
BOARD_COLS = 4 
WIN_STATE = (0, 3)      # +1의 보상을 가지는 종단 상태 위치
LOSE_STATE = (1, 3)     # -1의 보상을 가지는 종단 상태 위치
BLOCKED_STATE = (1, 1)  # 이동할 수 없는 영역
START = (2, 0)          # 시작 상태 위치
DETERMINISTIC = False   # 상태 전이 함수의 확률을 적용하기 위한 플래그. False일 경우에 적용.

class State:
    def __init__(self, state=START):
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def giveReward(self):
        if self.state == WIN_STATE:
            return 1
        if self.state == LOSE_STATE:
            return -1
        return 0

    def isEndFunc(self):
        if self.state==WIN_STATE or self.state==LOSE_STATE:
            self.isEnd = True

    def _chooseActionProb(self, action):
        if action == "U":
            return np.random.choice(["U", "L", "R"], p = [0.8, 0.1, 0.1])
        if action == "D":
            return np.random.choice(["D", "L", "R"], p = [0.8, 0.1, 0.1])
        if action == "L":
            return np.random.choice(["L", "U", "D"], p = [0.8, 0.1, 0.1])
        if action == "R":
            return np.random.choice(["R", "U", "D"], p = [0.8, 0.1, 0.1])

    # 격자 공간 내에서의 다음 상태를 반환
    def nextPosition(self, action):
        if self.determine:
            if action == "U":
                nextState = (self.state[0]-1, self.state[1])
            elif action == "D":
                nextState = (self.state[0]+1, self.state[1])
            elif action == "L":
                nextState = (self.state[0], self.state[1]-1)
            else:
                nextState = (self.state[0], self.state[1]+1)
            self.determine = False
        else:
            # 상태 전이 함수를 적용
            action = self._chooseActionProb(action)
            self.determine = True
            nextState = self.nextPosition(action)

        # 벽을 뚫거나, 이동할 수 없는 영역으로 상태를 바꿀 수 없음
        if nextState[0]>=0 and nextState[0]<=2:
            if nextState[1]>=0 and nextState[1]<=3:
                if nextState != BLOCKED_STATE:
                    return nextState
        return self.state

class Agent:
    def __init__(self):
        self.states = []    # 위치와 행동을 기록
        self.actions = ['U','D','L','R']
        self.state = State()
        self.isEnd = self.state.isEnd
        self.lr = 0.2
        self.decayGamma = 0.9   # 할인율

        # 전체 상태에 대해 Q함수(행동 가치 함수) 값 초기화
        self.Q_values = {}
        for i in range(BOARD_ROWS):
            for k in range(BOARD_COLS):
                self.Q_values[(i,k)] = {}
                for a in self.actions:
                    self.Q_values[(i,k)][a] = 0

    # Q값을 가장 극대화시키는 방향으로 다음 행동을 선택
    def chooseAction(self):
        maxNextReward = 0
        action = ''

        for a in self.actions:
            currentPosition = self.state.state
            nextReward = self.Q_values[currentPosition][a]
            if nextReward >= maxNextReward:
                action = a
                maxNextReward = nextReward
            #print(f'current pos: {self.state.state}, greedy action: {action}')
        return action

    # 행동 후 상태 업데이트
    def takeAction(self, action):
        position = self.state.nextPosition(action)
        return State(state=position)

    # 종단 상태 도달후 에피소드 초기화
    def reset(self):
        self.states = []
        self.state = State()
        self.isEnd = self.state.isEnd

    # 에피소드 갯수만큼 반복
    def play(self, episodes = 10):
        i = 0
        print('Sample 출력(에피소드 10까지)')
        while i < episodes:
            if i <= 10:
                print(i, end=' ')
            if self.state.isEnd:
                reward = self.state.giveReward()
                for a in self.actions:
                    self.Q_values[self.state.state][a] = reward
                for s in reversed(self.states):
                    currentQ_value = self.Q_values[s[0]][s[1]]
                    reward = currentQ_value + self.lr * (self.decayGamma*reward - currentQ_value)
                    self.Q_values[s[0]][s[1]] = round(reward, 3)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                self.states.append([(self.state.state), action])
                self.state = self.takeAction(action)
                self.state.isEndFunc()
                self.isEnd = self.state.isEnd
