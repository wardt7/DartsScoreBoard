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
		self.calucation_input = StringVar()
		# Sets some default fonts for use in the program's theme
		self.font_headings = font.Font(family="Helvetica", size=14)
		self.font_title = font.Font(family="Helvetica", size=32, weight="bold")
		self.font_text = font.Font(family="Helvetica", size=12)
		ttk.Style().configure(style="TButton", font=self.font_text)
		ttk.Style().configure(style="TFrame", background="White")
		ttk.Style().configure(style="TLabel", background="White", borderwidth=10, relief="solid", highlightbackground="Black")
		#ttk.Style().configure(style="MinusLeg.TButton", font=self.font_text, background="Red", foreground="Red")
		#ttk.Style().configure(style="AddLeg.TButton", font=self.font_text, background="Green", foreground="Green", activeforeground="Green")

	def interface(self):
		self.inter.title("BlackButler - Main Menu")
		self.inter.columnconfigure(0, weight=1)
		self.inter.rowconfigure(0, weight=1)
		self.inter["background"] = "White"
		player_one_frame = ttk.Frame(self.inter)
		player_one_frame.grid(column=0, row=0)
		player_one_frame = ttk.Frame(self.inter)
		player_one_frame.grid(column=0, row=0)
		player_one_name = ttk.Label(player_one_frame, text="Player 1", font=self.font_text, padding=5)
		player_one_name.grid(column=0, row=0, columnspan=3, sticky=(N,W,E,S))
		player_one_legs_label = ttk.Label(player_one_frame, text="Legs", font=self.font_text)
		player_one_legs_label.grid(column=0, row=1, columnspan=3, sticky=(N,W,E,S))
		player_one_remove_leg = ttk.Button(player_one_frame, command=lambda player=1: self.remove_leg(player), text="-", padding=3, style="MinusLeg.TButton")
		player_one_remove_leg.grid(column=0, row=2, sticky=(N,W,E,S))
		player_one_current_legs = ttk.Label(player_one_frame, textvariable=self.player_one_legs, font=self.font_text, padding=3)
		player_one_current_legs.grid(column=1, row=2, sticky=(N,W,E,S))
		player_one_add_leg = ttk.Button(player_one_frame, command=lambda player=1: self.add_leg(player), text="+", padding=3, style="AddLeg.TButton")
		player_one_add_leg.grid(column=2, row=2, sticky=(N,W,E,S))
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
			self.scorer.player_one.set_legs(self.scorer.player_one.get_legs()+1)
			self.player_one_legs.set(self.scorer.player_one.get_legs())


handle = interfaceScoreboard(170,2,1)
handle.interface()