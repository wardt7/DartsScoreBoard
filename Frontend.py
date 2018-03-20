from tkinter import *
from tkinter import ttk
from tkinter import font
import Backend

class interfaceScoreboard:
	def __init__(self, start, legs_to_win, player_to_start):
		self.scorer = Backend.Score(start, legs_to_win, player_to_start)
		self.inter = Tk()
		self.player_one_score = StringVar()
		self.player_one_score.set(start)
		self.player_two_score = IntVar()
		self.player_two_score.set(start)
		self.player_one_legs= IntVar()
		self.player_one_legs.set(0)
		self.player_two_legs = IntVar()
		self.player_two_legs.set(0)
		self.calculation_input_display = StringVar()
		self.calculation_input_actual = ""
		self.font_small = font.Font(family="Helvetica", size=14, weight="bold")
		self.font_large = font.Font(family="Helvetica", size=32, weight="bold")
		ttk.Style().theme_use("clam")
		ttk.Style().configure(style="TButton", font=self.font_small, bordercolor="Black")
		ttk.Style().configure(style="TFrame", background="White", bordercolor="White", foreground="White", borderwidth=10)
		ttk.Style().configure(style="Black.TFrame", background="Black", foreground="Black", borderwidth=10, relief="groove")
		ttk.Style().configure(style="TLabel", background="White", bordercolor="Black", justify="center", borderwidth=5, relief="groove")
		ttk.Style().configure(style="Red.TButton", font=self.font_small, background="#ff4242", foreground="Black")
		ttk.Style().configure(style="Green.TButton", font=self.font_small, background="#59b754", foreground="Black")
		ttk.Style().configure(style="PlayerOne.TLabel", font=self.font_small, background="#ffb838")
		ttk.Style().configure(style="PlayerOneLight.TLabel", font=self.font_small, background="#ffce75")
		ttk.Style().configure(style="PlayerOne.TButton", font=self.font_small, background="#ffb838")
		ttk.Style().configure(style="PlayerTwo.TLabel", font=self.font_small, background="#77d4ff")
		ttk.Style().configure(style="PlayerTwoLight.TLabel", font=self.font_small, background="#ccefff")
		ttk.Style().configure(style="PlayerTwo.TButton", font=self.font_small, background="#77d4ff")
		ttk.Style().configure(style="CurrentPlayerLight.TLabel", font=self.font_small, background="#ffce75")
		ttk.Style().configure(style="CurrentPlayer.TButton", font=self.font_small, background="#ffb838")
		self.inter.title("Darts Scoreboard")
		self.inter.resizable(False, False)
		self.inter.columnconfigure(0, weight=1)
		self.inter.rowconfigure(0, weight=1)
		self.inter["background"] = "Black"
		self.player_one_frame = ttk.Frame(self.inter, style="TFrame")
		self.player_one_frame.grid(column=0, row=0, sticky=(W))
		self.player_one_name = ttk.Label(self.player_one_frame, text="Player 1", font=self.font_small, style="PlayerOne.TLabel",
									anchor=CENTER)
		self.player_one_name.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))
		self.player_one_legs_label = ttk.Label(self.player_one_frame, text="Legs", font=self.font_small, anchor=CENTER)
		self.player_one_legs_label.grid(column=0, row=1, columnspan=3, sticky=(N, W, E, S))
		self.player_one_remove_leg = ttk.Button(self.player_one_frame, command=lambda player=1: self.remove_leg(player), text="-",
										   padding=3, width=5, style="Red.TButton")
		self.player_one_remove_leg.grid(column=0, row=2, sticky=(N, W, E, S))
		self.player_one_current_legs = ttk.Label(self.player_one_frame, textvariable=self.player_one_legs, font=self.font_small,
											padding=3, width=4, anchor=CENTER, style="PlayerOne.TLabel")
		self.player_one_current_legs.grid(column=1, row=2, sticky=(N, W, E, S))
		self.player_one_add_leg = ttk.Button(self.player_one_frame, command=lambda player=1: self.add_leg(player), text="+",
										width=5, style="Green.TButton")
		self.player_one_add_leg.grid(column=2, row=2)
		self.player_one_score_label = ttk.Label(self.player_one_frame, textvariable=self.player_one_score, font=self.font_large,
										   anchor=CENTER, style="PlayerOne.TLabel")
		self.player_one_score_label.grid(column=0, row=3, columnspan=3, sticky=(N, W, E, S))
		self.undo_button = ttk.Button(self.player_one_frame, command=self.undo, text="Undo", style="Red.TButton")
		self.undo_button.grid(column=0, row=4, columnspan=3, sticky=(N,W,E,S))
		self.player_two_frame = ttk.Frame(self.inter, style="TFrame")
		self.player_two_frame.grid(column=1, row=0, sticky=(N, W, E, S))
		self.player_two_name = ttk.Label(self.player_two_frame, text="Player 2", font=self.font_small, style="PlayerTwo.TLabel",
									anchor=CENTER)
		self.player_two_name.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))
		self.player_two_legs_label = ttk.Label(self.player_two_frame, text="Legs", font=self.font_small, anchor=CENTER)
		self.player_two_legs_label.grid(column=0, row=1, columnspan=3, sticky=(N, W, E, S))
		self.player_two_remove_leg = ttk.Button(self.player_two_frame, command=lambda player=2: self.remove_leg(player), text="-",
										   padding=3, width=5, style="Red.TButton")
		self.player_two_remove_leg.grid(column=0, row=2, sticky=(N, W, E, S))
		self.player_two_current_legs = ttk.Label(self.player_two_frame, textvariable=self.player_two_legs, font=self.font_small,
											padding=3, width=4, anchor=CENTER, style="PlayerTwo.TLabel")
		self.player_two_current_legs.grid(column=1, row=2, sticky=(N, W, E, S))
		self.player_two_add_leg = ttk.Button(self.player_two_frame, command=lambda player=2: self.add_leg(player), text="+",
										width=5, style="Green.TButton")
		self.player_two_add_leg.grid(column=2, row=2, sticky=(N, W, E, S))
		self.player_two_score_label = ttk.Label(self.player_two_frame, textvariable=self.player_two_score, font=self.font_large,
										   anchor=CENTER, style="PlayerTwo.TLabel")
		self.player_two_score_label.grid(column=0, row=3, columnspan=3, sticky=(N, W, E, S))
		self.redo_button = ttk.Button(self.player_two_frame, command=self.redo, text="Redo",
									 style="Green.TButton")
		self.redo_button.grid(column=0, row=4, columnspan=3, sticky=(N,W,E,S))
		self.keypad_frame = ttk.Frame(self.inter, style="TFrame")
		self.keypad_frame.grid(column=0, row=1, columnspan=2, sticky=(N, W, E, S))
		self.keypad_calculation_display = ttk.Label(self.keypad_frame, textvariable=self.calculation_input_display,
											   font=self.font_small, style="CurrentPlayerLight.TLabel", padding=5)
		self.keypad_calculation_display.grid(column=0, row=0, columnspan=5, sticky=(N, W, E, S))
		for x, y, number in zip([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3], [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
								[1, 2, 3, 4, 5, 6, 7, 8, 9, 0, "+", "X"]):
			btn = ttk.Button(self.keypad_frame, text=number, command=lambda number=number: self.keypad(number),
						   style="CurrentPlayer.TButton", padding=3, width=8).grid(column=y, row=x + 1)
		self.keypad_delete = ttk.Button(self.keypad_frame, text="DEL", command=lambda: self.delete(), style="Red.TButton",
								   width=8)
		self.keypad_delete.grid(column=4, row=1, rowspan=2, sticky=(N, W, E, S))
		self.keypad_enter = ttk.Button(self.keypad_frame, text="ENT", command=lambda: self.enter(), style="Green.TButton",
								  width=8)
		self.keypad_enter.grid(column=4, row=3, rowspan=2, sticky=(N, W, E, S))
		self.inter.mainloop()

	def remove_leg(self, player):
		if player == 1:
			update = self.scorer.remove_leg(1)
		else:
			update = self.scorer.remove_leg(2)
		if "error" in update:
			return self.error(update["error"])
		else:
			self.player_one_legs.set(self.scorer.player_one.get_legs())
			self.player_two_legs.set(self.scorer.player_two.get_legs())

	def add_leg(self, player):
		if player == 1:
			update = self.scorer.add_leg(1)
		else:
			update = self.scorer.add_leg(2)
		self.player_one_legs.set(self.scorer.player_one.get_legs())
		self.player_two_legs.set(self.scorer.player_two.get_legs())
		if update["winner"] is not None:
			return self.winner(player)

	def keypad(self, value):
		if type(value) == int:
			self.calculation_input_display.set(self.calculation_input_display.get()+str(value))
			self.calculation_input_actual = self.calculation_input_actual + str(value)
		else:
			try:
				if self.calculation_input_actual[-1] == "+" or self.calculation_input_actual[-1] == "*":
					return self.error("Can't have two + or two X operators in a row")
				else:
					if value == "+":
						self.calculation_input_display.set(self.calculation_input_display.get() + value)
						self.calculation_input_actual = self.calculation_input_actual + value
					else:
						self.calculation_input_display.set(self.calculation_input_display.get() + value)
						self.calculation_input_actual = self.calculation_input_actual + "*"
			except IndexError:
				return self.error("Can't start input with + or X")

	def delete(self):
		if len(self.calculation_input_actual) == 0:
			return self.error("Can't delete when input is empty")
		else:
			self.calculation_input_display.set(self.calculation_input_display.get()[:-1])
			self.calculation_input_actual = self.calculation_input_actual[:-1]

	def enter(self):
		current_score = self.scorer.parse_string_input(self.calculation_input_actual)
		if self.scorer.turn % 2 == 1:
			update = self.scorer.add_turn(1, current_score)
		else:
			update = self.scorer.add_turn(2, current_score)
		if "error" in update:
			return self.error(update["error"])
		else:
			self.calculation_input_actual = ""
			self.calculation_input_display.set("")
			self.player_one_legs.set(self.scorer.player_one.get_legs())
			self.player_two_legs.set(self.scorer.player_two.get_legs())
			self.player_one_score.set(self.scorer.player_one.get_score())
			self.player_two_score.set(self.scorer.player_two.get_score())
			if update["winner"] is None:
				if update["leg_start"] == 1 or self.scorer.turn % 2 == 1:
					self.change_style(1)
				elif update["leg_start"] == 2 or self.scorer.turn % 2 == 0:
					self.change_style(2)
			else:
				self.winner(update["winner"])

	def change_style(self, player):
		if player == 1:
			ttk.Style().configure(style="CurrentPlayerLight.TLabel", font=self.font_small, background="#ffce75")
			ttk.Style().configure(style="CurrentPlayer.TButton", font=self.font_small, background="#ffb838")
		else:
			ttk.Style().configure(style="CurrentPlayerLight.TLabel", font=self.font_small, background="#ccefff")
			ttk.Style().configure(style="CurrentPlayer.TButton", font=self.font_small, background="#77d4ff")

	def error(self, message):
		error_window = Toplevel()
		error_window.resizable(False,False)
		error_window.title("ERROR")
		error_window.columnconfigure(0, weight=1)
		error_window.rowconfigure(0, weight=1)
		error_window["background"] = "White"
		error_message = ttk.Label(error_window, text=message, font=self.font_small, style="TLabel", padding=5)
		error_message.grid(column=0, row=0)
		error_button = ttk.Button(error_window, command=error_window.destroy, text="Ok", padding=3, width=5, style="TButton")
		error_button.grid(column=0,row=1, sticky=(N,W,E,S))
		error_window.mainloop()

	def winner(self, player):
		winner_window = Toplevel()
		winner_window.resizable(False, False)
		winner_window.title("ERROR")
		winner_window.columnconfigure(0, weight=1)
		winner_window.rowconfigure(0, weight=1)
		winner_window["background"] = "White"
		winner_message = ttk.Label(winner_window, text="Player {} wins!".format(player), font=self.font_small, style="TLabel", padding=5)
		winner_message.grid(column=0, row=0, columnspan=2)
		winner_ok_button = ttk.Button(winner_window, command=lambda: self.inter.destroy(), text="Ok", padding=3, width=5,
								  style="Green.TButton")
		winner_ok_button.grid(column=1, row=1, sticky=(N, W, E, S))
		winner_undo_button = ttk.Button(winner_window, command=lambda: self.undo_win(winner_window), text="Undo", padding=3, width=5, style="Red.TButton")
		winner_undo_button.grid(column=0, row=1, sticky=(N,W,E,S))
		winner_window.mainloop()

	def undo(self):
		try:
			update = self.scorer.undo_turn()
		except ValueError:
			return self.error("Can't undo past first turn")
		self.calculation_input_actual = ""
		self.calculation_input_display.set("")
		self.player_one_legs.set(self.scorer.player_one.get_legs())
		self.player_two_legs.set(self.scorer.player_two.get_legs())
		self.player_one_score.set(self.scorer.player_one.get_score())
		self.player_two_score.set(self.scorer.player_two.get_score())
		if update["leg_start"] == 1 or self.scorer.turn % 2 == 1:
			self.change_style(1)
		elif update["leg_start"] == 2 or self.scorer.turn % 2 == 0:
			self.change_style(2)

	def undo_win(self, window):
		self.undo()
		window.destroy()

	def redo(self):
		try:
			update = self.scorer.redo_turn()
		except ValueError:
			return self.error("Can't redo past last turn")
		self.calculation_input_actual = ""
		self.calculation_input_display.set("")
		self.player_one_legs.set(self.scorer.player_one.get_legs())
		self.player_two_legs.set(self.scorer.player_two.get_legs())
		self.player_one_score.set(self.scorer.player_one.get_score())
		self.player_two_score.set(self.scorer.player_two.get_score())
		if update["winner"] is None:
			if update["leg_start"] == 1 or self.scorer.turn % 2 == 1:
				self.change_style(1)
			elif update["leg_start"] == 2 or self.scorer.turn % 2 == 0:
				self.change_style(2)
		else:
			self.winner(update["winner"])




handle = interfaceScoreboard(170,2,1)