# 격자 공간 클래스
class Grid: 
	def __init__(self, rows, cols, start):
		self.rows = rows
		self.cols = cols
		self.i = start[0]
		self.j = start[1]

	# 각 상태의 보상과 선택 가능한 행동을 설정
	def set(self, rewards, actions):
		self.rewards = rewards
		self.actions = actions

	def set_state(self, s):
		self.i = s[0]
		self.j = s[1]

	def current_state(self):
		return (self.i, self.j)

	def is_terminal(self, s):
		return s not in self.actions

	def move(self, action):
		if action in self.actions[(self.i, self.j)]:
			if action == 'U':
				self.i -= 1
			elif action == 'D':
				self.i += 1
			elif action == 'R':
				self.j += 1
			elif action == 'L':
				self.j -= 1
	    # 보상이 있을 경우 보상을 반환
		return self.rewards.get((self.i, self.j), 0)

	# 모든 상태를 반환
	def all_states(self):
		# possibly buggy but simple way to get all states
		# either a position that has possible next actions
		# or a position that yields a reward
		return set(self.actions.keys()) | set(self.rewards.keys())