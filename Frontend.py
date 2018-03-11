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
		self.calculation_input = StringVar()
		self.font_small = font.Font(family="Helvetica", size=14, weight="bold")
		self.font_large = font.Font(family="Helvetica", size=32, weight="bold")
		ttk.Style().theme_use("clam")
		ttk.Style().configure(style="TButton", font=self.font_small)
		ttk.Style().configure(style="TFrame", background="White", foreground="White", borderwidth=10, relief="groove")
		ttk.Style().configure(style="TLabel", background="White", justify="center", borderwidth=5, relief="groove")
		ttk.Style().configure(style="MinusLeg.TButton", font=self.font_small, background="#FC4E4E", foreground="Black")
		ttk.Style().configure(style="AddLeg.TButton", font=self.font_small, background="#C9F390", foreground="Black")
		ttk.Style().configure(style="PlayerOne.TLabel", font=self.font_small, background="#9C8AA5")
		ttk.Style().configure(style="PlayerOneLight.TLabel", font=self.font_small, background="#BDAEC6")
		ttk.Style().configure(style="PlayerTwo.TLabel", font=self.font_small, background="#5E9DC8")
		ttk.Style().configure(style="PlayerTwoLight.TLabel", font=self.font_small, background="#DCF0F7")

	def interface(self):
		self.inter.title("Darts Scoreboard")
		self.inter.columnconfigure(0, weight=1)
		self.inter.rowconfigure(0, weight=1)
		self.inter["background"] = "White"
		player_one_frame = ttk.Frame(self.inter, style="TFrame")
		player_one_frame.grid(column=0, row=0, sticky=(N,W,E,S))
		player_one_name = ttk.Label(player_one_frame, text="Player 1", font=self.font_small, style="PlayerOne.TLabel", anchor=CENTER)
		player_one_name.grid(column=0, row=0, columnspan=3, sticky=(N,W,E,S))
		player_one_legs_label = ttk.Label(player_one_frame, text="Legs", font=self.font_small, anchor=CENTER)
		player_one_legs_label.grid(column=0, row=1, columnspan=3, sticky=(N,W,E,S))
		player_one_remove_leg = ttk.Button(player_one_frame, command=lambda player=1: self.remove_leg(player), text="-", padding=3, width=5, style="MinusLeg.TButton")
		player_one_remove_leg.grid(column=0, row=2, sticky=(N,W,E,S))
		player_one_current_legs = ttk.Label(player_one_frame, textvariable=self.player_one_legs, font=self.font_small, padding=3, width=5, anchor=CENTER, style="PlayerOne.TLabel")
		player_one_current_legs.grid(column=1, row=2, sticky=(N,W,E,S))
		player_one_add_leg = ttk.Button(player_one_frame, command=lambda player=1: self.add_leg(player), text="+", width=5, style="AddLeg.TButton")
		player_one_add_leg.grid(column=2, row=2)
		player_one_score_label = ttk.Label(player_one_frame, textvariable=self.player_one_score, font=self.font_large, anchor=CENTER, style="PlayerOne.TLabel")
		player_one_score_label.grid(column=0, row=3, columnspan=3, sticky=(N,W,E,S))
		player_two_frame = ttk.Frame(self.inter, style="TFrame")
		player_two_frame.grid(column=1, row=0)
		player_two_name = ttk.Label(player_two_frame, text="Player 2", font=self.font_small, style="PlayerTwo.TLabel", anchor=CENTER)
		player_two_name.grid(column=0, row=0, columnspan=3, sticky=(N, W, E, S))
		player_two_legs_label = ttk.Label(player_two_frame, text="Legs", font=self.font_small, anchor=CENTER)
		player_two_legs_label.grid(column=0, row=1, columnspan=3, sticky=(N, W, E, S))
		player_two_remove_leg = ttk.Button(player_two_frame, command=lambda player=2: self.remove_leg(player), text="-", padding=3, width=5, style="MinusLeg.TButton")
		player_two_remove_leg.grid(column=0, row=2, sticky=(N, W, E, S))
		player_two_current_legs = ttk.Label(player_two_frame, textvariable=self.player_two_legs, font=self.font_small, padding=3, width=5, anchor=CENTER, style="PlayerTwo.TLabel")
		player_two_current_legs.grid(column=1, row=2, sticky=(N, W, E, S))
		player_two_add_leg = ttk.Button(player_two_frame, command=lambda player=2: self.add_leg(player), text="+", width=5, style="AddLeg.TButton")
		player_two_add_leg.grid(column=2, row=2, sticky=(N, W, E, S))
		player_two_score_label = ttk.Label(player_two_frame, textvariable=self.player_two_score, font=self.font_large, anchor=CENTER, style="PlayerTwo.TLabel")
		player_two_score_label.grid(column=0, row=3, columnspan=3, sticky=(N, W, E, S))
		self.inter.mainloop()

	def remove_leg(self, player):
		if player == 1:
			if self.scorer.player_one.get_legs() > 0:
				self.scorer.player_one.set_legs(self.scorer.player_one.get_legs()-1)
				self.player_one_legs.set(self.scorer.player_one.get_legs())
		else:
			if self.scorer.player_one.get_legs() > 0:
				self.scorer.player_one.set_legs(self.scorer.player_one.get_legs()-1)
				self.player_one_legs.set(self.scorer.player_one.get_legs())

	def add_leg(self, player):
		if player == 1:
			self.scorer.player_one.set_legs(self.scorer.player_one.get_legs()+1)
			self.player_one_legs.set(self.scorer.player_one.get_legs())
		else:
			self.scorer.player_two.set_legs(self.scorer.player_two.get_legs()+1)
			self.player_one_legs.set(self.scorer.player_two.get_legs())


handle = interfaceScoreboard(170,2,1)
handle.interface()