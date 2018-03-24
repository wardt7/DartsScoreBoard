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
		self.turn = 1
		if player_to_start == 1:
			self.leg_start = 1
		else:
			self.leg_start = 2
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
		self.c.execute("""INSERT OR REPLACE INTO Games VALUES (?,?,?,?,?,?,?)""", (self.game_id,
																				   self.turn,
																				   self.player_one.get_score(),
																				   self.player_two.get_score(),
																				   self.player_one.get_legs(),
																				   self.player_two.get_legs(),
																				   self.leg_start))

	def create_table(self):
		self.c.execute("""CREATE TABLE IF NOT EXISTS Games(
		                game_ID INTEGER NOT NULL,
		                turn_no INTEGER NOT NULL,
		                player_one_score INTEGER NOT NULL,
		                player_two_score INTEGER NOT NULL,
		                player_one_legs INTEGER NOT NULL,
		                player_two_legs INTEGER NOT NULL,
		                player_leg_start INTEGER NOT NULL,
		                PRIMARY KEY (game_ID, turn_no))""")

	def check_game_existence(self, game_id):
		value = self.c.execute("""SELECT game_ID FROM Games WHERE game_ID = ?""", (game_id,))
		value = value.fetchall()
		if not value:
			return False
		else:
			return True

	def add_leg(self, player):
		if player == 1:
			self.player_one.set_legs(self.player_one.get_legs()+1)
		else:
			self.player_two.set_legs(self.player_two.get_legs()+1)
		self.turn += 1
		self.c.execute("""INSERT OR REPLACE INTO Games VALUES (?,?,?,?,?,?,?)""", (self.game_id,
																				   self.turn,
																				   self.player_one.get_score(),
																				   self.player_two.get_score(),
																				   self.player_one.get_legs(),
																				   self.player_two.get_legs(),
																				   self.leg_start))
		if self.player_one.get_legs() == self.legs_to_win:
			return {"winner": self.player_one.name}
		elif self.player_two.get_legs() == self.legs_to_win:
			return {"winner": self.player_two.name}
		else:
			return {"winner": None}

	def remove_leg(self, player):
		if player == 1:
			legs = self.player_one.get_legs()
			if legs == 0:
				return {"error":"Can't have negative legs"}
			else:
				self.player_one.set_legs(legs-1)
		else:
			legs = self.player_two.get_legs()
			if legs == 0:
				return {"error":"Can't have negative legs"}
			else:
				self.player_two.set_legs(legs-1)
		self.c.execute("""INSERT OR REPLACE INTO Games VALUES (?,?,?,?,?,?,?)""", (self.game_id,
																				   self.turn,
																				   self.player_one.get_score(),
																				   self.player_two.get_score(),
																				   self.player_one.get_legs(),
																				   self.player_two.get_legs(),
																				   self.leg_start))
		return {}

	def add_turn(self, player, score=0):
		new_leg_flag = False
		return_dict = {}
		if player == 1:
			if score > self.player_one.get_score():
				return {"error": "Score entered was larger than {}'s current score".format(self.player_one.name)}
			self.player_one.set_score(self.player_one.get_score() - score)
			if self.player_one.get_score() == 0:
				self.player_one.set_legs(self.player_one.get_legs() + 1)
				new_leg_flag = True
		else:
			if score > self.player_two.get_score():
				return {"error": "Score entered was larger than {}'s current score".format(self.player_two.name)}
			self.player_two.set_score(self.player_two.get_score() - score)
			if self.player_two.get_score() == 0:
				self.player_two.set_legs(self.player_two.get_legs() + 1)
				new_leg_flag = True
		self.turn += 1
		if new_leg_flag:
			self.player_one.set_score(self.start_score)
			self.player_two.set_score(self.start_score)
			if self.leg_start == 1:
				self.leg_start = 2
				if self.turn % 2 == 1:
					self.turn += 1
			else:
				self.leg_start = 1
				if self.turn % 2 == 0:
					self.turn += 1
			return_dict["leg_start"] = self.leg_start
		self.c.execute("""INSERT OR REPLACE INTO Games VALUES (?,?,?,?,?,?,?)""", (self.game_id,
																				   self.turn,
																				   self.player_one.get_score(),
																				   self.player_two.get_score(),
																				   self.player_one.get_legs(),
																				   self.player_two.get_legs(),
																				   self.leg_start))
		if self.player_one.get_legs() == self.legs_to_win:
			return {"winner": self.player_one.name}
		elif self.player_two.get_legs() == self.legs_to_win:
			return {"winner": self.player_two.name}
		else:
			if "leg_start" not in return_dict:
				return_dict["leg_start"] = None
			return_dict["winner"] = None
			return return_dict

	def undo_turn(self):
		undoing = True
		current_turn = self.turn
		return_dict = {}
		while undoing:
			self.turn -= 1
			if self.turn < 1:
				self.turn = current_turn
				raise ValueError("Cannot undo past first turn")
			self.c.execute("SELECT * FROM Games WHERE game_ID = ? AND turn_no = ?", (self.game_id, self.turn))
			values = self.c.fetchone()
			if values:
				undoing = False
		self.player_one.set_score(values[2])
		self.player_two.set_score(values[3])
		self.player_one.set_legs(values[4])
		self.player_two.set_legs(values[5])
		self.leg_start = values[6]
		if values[2] == self.start_score and values[3] == self.start_score:
			return_dict["leg_start"] = self.leg_start
		else:
			return_dict["leg_start"] = None
		return return_dict



	def redo_turn(self):
		redoing = True
		current_turn = self.turn
		return_dict = {}
		while redoing:
			self.turn += 1
			self.c.execute("SELECT * FROM Games WHERE game_ID = ? AND turn_no = ?", (self.game_id, self.turn))
			values = self.c.fetchone()
			if values:
				redoing = False
			else:
				if current_turn+2 == self.turn:
					self.turn = current_turn
					raise ValueError("Cannot redo past last turn")
		self.player_one.set_score(values[2])
		self.player_two.set_score(values[3])
		self.player_one.set_legs(values[4])
		self.player_two.set_legs(values[5])
		self.leg_start = values[6]
		if values[2] == self.start_score and values[3] == self.start_score:
			return_dict["leg_start"] = self.leg_start
		else:
			return_dict["leg_start"] = None
		if self.player_one.get_legs() == self.legs_to_win:
			return {"winner": self.player_one.name}
		elif self.player_two.get_legs() == self.legs_to_win:
			return {"winner": self.player_two.name}
		else:
			if "leg_start" not in return_dict:
				return_dict["leg_start"] = None
			return_dict["winner"] = None
			return return_dict


	def parse_string_input(self, calculation):
		if calculation == "":
			return 0
		return eval(parser.expr(calculation).compile())
