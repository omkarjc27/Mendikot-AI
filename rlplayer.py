import torch
class RLPlayer:
	def __init__(self,game,player_no,cards,model):
		self.player_no = player_no
		self.game = game
		self.cards = cards
		
		self.model = model['model']
		self.optimizer = model['optimizer']
		self.criterion = model['criterion']
		self.learning = model['learning']

		self.state = model['state']
		self.actual = model['actual']

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
		print("------------\n","Player No:",self.player_no+1,"|",self.game.turn_no+1,"-",self.game.round_no+1,"\n------------")
		if self.game.trump:
			print("Trump",self.print_card(self.game.trump))
		if len(self.game.current_hand)!=0:
			print("\nHaat\n")
			for card in self.game.current_hand:
				if card != -1:
					print(self.print_card(card))
		# print all cards that can be played
		print("\nOptions\n")
		for i in range(len(playables)):
			print("%2d. %s"%(i+1,self.print_card(playables[i])))




	def play(self):

		playables = self.game.find_playables(self.player_no)
		if not self.learning:
			#self.display(playables)
			pass
		# Binarized form of playables
		p = [0]*52
		for card in playables:
			p[card] = 1

		inp = [0]*2704
		for i in range(len(self.game.history)):
			inp[self.game.history[i]+(52*i)] = 1
		#print(self.game.history)
		#print(inp)
		self.state.append(inp) # Save states input for training
		# Convert to torch tensor
		inp = torch.squeeze(torch.FloatTensor(inp))
		
		p = torch.squeeze(torch.FloatTensor(p))
		# Mean Normalization
		#inp = torch.add(inp, -25.5)
		#inp = torch.div(inp, 53)
		y_pred = self.model(inp) # Predict Q-Score of each card
		y_pred = torch.mul(y_pred, p) # Filter out cards that can only be played
		val = torch.max(y_pred).item()
		currentcard = torch.argmax(y_pred).item()
		if val == 0:
			currentcard = playables[0]
		if not self.learning:
			print("Player No",self.player_no)
			print([self.print_card(i) for i in playables])
			print("Played",self.print_card(currentcard))
		ret = self.game.score(currentcard,self.player_no)
		
		y = y_pred.tolist()
		y[currentcard] = ret[self.player_no]
		self.actual.append(y) # Save y for training
		
		return ret
	