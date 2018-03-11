import sqlite3, random, parser


class Player:
	def __init__(self, player):
		self.__score = 0
		self.__legs = 0
		self.name = player

	def set_score(self, score):
		self.__score = score
		return True

	def set_legs(self, legs):
		self.__legs = legs

	def get_score(self):
		return self.__score

	def get_legs(self):
		return self.__legs


class Score:
	def __init__(self, start, legs_to_win, player_to_start, player_one="Player 1", player_two="Player 2"):
		self.player_one = Player(player_one)
		self.player_two = Player(player_two)
		if player_to_start == 1:
			self.turn = 1
		else:
			self.turn = 2
		self.legs_to_win = legs_to_win
		self.start_score = start
		self.player_one.set_score(self.start_score)
		self.player_two.set_score(self.start_score)
		self.db = sqlite3.connect("Darts")
		self.c = self.db.cursor()
		self.create_table()
		creating_game_id = True
		while creating_game_id:
			self.game_id = random.randrange(0, 100000)
			if not self.check_game_existence(self.game_id):
				creating_game_id = False

	def create_table(self):
		self.c.execute("""CREATE TABLE IF NOT EXISTS Games(
		                game_ID INTEGER NOT NULL,
		                turn_no INTEGER NOT NULL,
		                player_one_score INTEGER NOT NULL,
		                player_two_score INTEGER NOT NULL,
		                player_one_legs INTEGER NOT NULL,
		                player_two_legs INTEGER NOT NULL,
		                PRIMARY KEY (game_ID, turn_no))""")

	def check_game_existence(self, game_id):
		value = self.c.execute("""SELECT game_ID FROM Games WHERE game_ID = ?""", (game_id,))
		value = value.fetchall()
		if not value:
			return False
		else:
			return True

	def add_turn(self, player, score=0):
		new_leg_flag = False
		if player == 1:
			if score > self.player_one.get_score():
				raise ValueError("Score entered was larger than player's current score")
			self.player_one.set_score(self.player_one.get_score() - score)
			if self.player_one.get_score() == 0:
				self.player_one.set_legs(self.player_one.get_legs() + 1)
				new_leg_flag = True
		else:
			if score > self.player_two.get_score():
				raise ValueError("Score entered was larger than player's current score")
			self.player_two.set_score(self.player_two.get_score() - score)
			if self.player_two.get_score() == 0:
				self.player_two.set_legs(self.player_two.get_legs() + 1)
				new_leg_flag = True
		self.c.execute("""INSERT OR REPLACE INTO Games VALUES (?,?,?,?,?,?)""", (self.game_id,
																	  self.turn,
																	  self.player_one.get_score(),
																	  self.player_two.get_score(),
																	  self.player_one.get_legs(),
																	  self.player_two.get_legs()))
		if new_leg_flag:
			self.player_one.set_score(self.start_score)
			self.player_two.set_score(self.start_score)
		if self.player_one.get_legs() == self.legs_to_win:
			return {"winner":self.player_one.name}
		elif self.player_two.get_legs() == self.legs_to_win:
			return {"winner":self.player_two.name}
		else:
			self.turn += 1
			return {"winner":None}

	def undo_turn(self):
		self.turn -= 1
		self.c.execute("SELECT * FROM Games WHERE game_ID = ? AND turn_no = ?",(self.game_id,self.turn))
		values = self.c.fetchone()
		if not values:
			self.turn += 1
			raise ValueError("Cannot undo past first turn")
		self.player_one.set_score(values[2])
		self.player_two.set_score(values[3])
		self.player_one.set_legs(values[4])
		self.player_two.set_legs(values[5])
		return True

	def redo_turn(self):
		self.turn += 1
		self.c.execute("SELECT * FROM Games WHERE game_ID = ? AND turn_no = ?",(self.game_id,self.turn))
		values = self.c.fetchone()
		try:
			self.player_one.set_score(values[2])
			self.player_two.set_score(values[3])
			self.player_one.set_legs(values[4])
			self.player_two.set_legs(values[5])
			return True
		except IndexError:
			self.turn -= 1
			raise ValueError("Cannot redo as there is no data to return")

	def parse_string_input(self, calculation):
		return eval(parser.expr(calculation).compile())
