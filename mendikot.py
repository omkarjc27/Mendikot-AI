from random import shuffle
from player import HumanPlayer
class Mendikot():
	def __init__(self):
		self.cards = [[],[],[],[]]
		self.deal()
		self.players = [HumanPlayer(self,0,self.cards[0]),\
						HumanPlayer(self,1,self.cards[1]),\
						HumanPlayer(self,2,self.cards[2]),\
						HumanPlayer(self,3,self.cards[3])]
		self.history = []
		self.trump = None
		self.current_hand = []
		self.round_no = 0
		self.turn_no = 0
		self.trump_set = False


	def deal(self):
		l = list(range(52))
		shuffle(l)
		for i in range(len(l)):
			p = i%4
			self.cards[p].append(l[i])

	def find_playables(self,player):
		playables = []
		# If it is not the first card of that round then find all possible cards that can be played
		if len(self.current_hand)!=0:
			for card in self.cards[player]:
				if int(card/13) == int(self.current_hand[0]/13):
					playables.append(card)

		# If No card is available to play with initial symbol of that round
		# or It is first card of that round
		if len(playables)==0:
			playables = self.cards[player]			
			# Check if It is not first card of that round then it is a trump
			if self.trump == None and len(self.current_hand)!=0 :
				self.trump_set = True
		return playables

	def eval(self,current_hand):
		val = [0,0,0,0]
		sym = [0,0,0,0]
		res = [0,0,0,0]
		same_symbol = True
		winner = None

		for i in range(len(current_hand)):
			card = current_hand[i]
			val[i] = (card%13)
			sym[i] = int(card/13)
			# Check if all cards have same symbol
			if int(current_hand[0]/13) != int(card/13):
				same_symbol = False

		if same_symbol:
			winner = val.index(max(val))
		else:
			# Check if Trump exists 
			if self.trump:
				print("Trump",self.trump)
				trumps = [i for i, j in enumerate(current_hand) if int(j/13) == int(self.trump/13)]
				print(trumps)
				# Check for Trumps in current hand
				if len(trumps)>0:				
					# Assign winner to first element of trumps 
					# and check if there is any greater trump and then declare greatest as the winner
					winner = trumps[0]
					for t in trumps:
						if val[t] > val[winner]:
							winner = t

			# If trumps do not exist
			if winner == None:
				valid_cards = [i for i, j in enumerate(current_hand) if int(j/13) == int(current_hand[0]/13)]
				winner = valid_cards[0]
				for t in valid_cards:
					if val[t] > val[winner]:
						winner = t
		# If even team wins both players get equal points
		next_p = winner
		if winner%2 == 0:
			winner = 0
			winner2 = 2
		else:
			winner = 1
			winner2 = 3

		# If Mendi (10) Exists winner gets 1 point else winner gets 0.8 point
		if 8 in val:
			res[winner] = 1
			res[winner2] = 1
		else:
			res[winner2] = 0.25
			res[winner] = 0.25


		return next_p,res

	def score(self,currentcard,player_no):
		order = [0,1,2,3,0]
		# Find player that will be playing next move
		next_player = order[order.index(player_no)+1]
		# Append card to current hand and remove from cards
		if len(self.current_hand) == 0:
			self.current_hand = [-1]*4
		self.current_hand[player_no] = currentcard
		# Remove currentcard from cards
		del self.cards[player_no][self.cards[player_no].index(currentcard)]
		# If This is a trump card set it
		if self.trump_set and self.trump == None:
			self.trump = int(currentcard/13)
			self.trump_set = False
		# Check if it's the last turn of the round 
		self.turn_no+=1
		if self.turn_no > 3:
			self.round_no += 1
			self.turn_no = 0
			self.history.append(self.current_hand)
			next_player,res = self.eval(self.current_hand)
			print(self.current_hand)
			print(res)
			self.current_hand = []
			# Check if it is the last turn of the game
			if self.round_no > 12:
				return res
			else:
				rec = self.players[next_player].play()
				return [ rec[0]+res[0], rec[1]+res[1], rec[2]+res[2], rec[3]+res[3]]

		rec = self.players[next_player].play()
		return rec

M = Mendikot()
print(M.players[0].play())