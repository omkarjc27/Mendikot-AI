class HumanPlayer:
	def __init__(self,game,player_no,cards,model):
		self.player_no = player_no
		self.game = game
		self.cards = cards

	def print_card(self,card):
		# 0-12 Club
		# 13-25 Diamond 
		# 26-38 Heart
		# 39-52 Spades
	
		sym = ['Club', 'Diamond', 'Heart', 'Spades']
		number = (card%13)+2
		symbol = sym[int(card/13)]
		
		if number>10:
			if number == 11: 
				number = "Jack"
			elif number == 12: 
				number = "Queen"
			elif number == 13: 
				number = "King"
			elif number == 14: 
				number = "Ace"
	
			return "%5s of %s"%(number,symbol)


		return "%5d of %s"%(number,symbol)

	def display(self,playables):
		# print cards played in that hand
		print("Player No:",self.player_no+1,"|",self.game.turn_no+1,"-",self.game.round_no+1)
		if self.game.trump!=None:
			sym = ['Club', 'Diamond', 'Heart', 'Spades']
			print("Trump is",sym[self.game.trump])
		if len(self.game.current_hand)!=0:
			print("------------\n","Haat","\n------------")
			for card in self.game.current_hand:
				if card != -1:
					print(self.print_card(card))
		# print all cards that player has
		print("------------\n","Your Cards","\n------------")
		for i in range(len(self.cards)):
			print(self.print_card(self.cards[i]))
		# print all cards that can be played
		print("------------\n","Your Options","\n------------")
		for i in range(len(playables)):
			print("%2d. %s"%(i+1,self.print_card(playables[i])))


	def play(self):
		playables = self.game.find_playables(self.player_no)
		self.display(playables)
		# Ask for new card and check if card can be played or not
		while True:
			try:
				currentcard = playables[int(input(">>"))-1]
				#currentcard = playables[0]
			except:
				print("Input Number Invalid. Try Again.")
			else:
				break

		return self.game.score(currentcard,self.player_no)
	