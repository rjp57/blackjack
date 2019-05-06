'''Simple 1 deck Blackjack game with just hit/stand/double down. no Splitting or Insurance.

Features: . Dynamic hand values (aces can be either 1 or 11)
		  . Actual deck tracking, meaning the deck does not shuffle between hands and the cards dealt are removed from it. Deck will shuffle when there are no more cards in it.
		  . Keeps track of the "count" (how many more high cards are in the deck compared to low cards) if you want to practice counting cards
		  . Keeps track of how many cards are left in the deck
		  . Dealer will Hit when his hand is less than 17. Stands on "soft 17"
'''
from random import shuffle

class deck:
	cards = ['A','A','A','A', 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']
	count = 0
	
	def total_cards(self):
		return len(self.cards)
	
	def shuffle_deck(self):
		self.cards = ['A','A','A','A', 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']
		count = 0
		print("Shuffling Deck...")
		shuffle(self.cards)

	def take_top_card(self):
		if (self.total_cards() == 0):
			self.shuffle_deck()
			
		card = self.cards.pop(-1)
		
		if (card == 'A' or card == 'J' or card == 'Q' or card == 'K' or card == 10):
			self.count -= 1
		elif (card == 2 or card == 3 or card == 4 or card == 5 or card == 6):
			self.count += 1
		return card
	
	def current_count(self):
		return self.count

def calculate_hard_total(hand):
	total = 0
	for card in hand:
		if (card == 'J' or card == 'Q' or card == 'K'):
			total += 10
		elif (card == 'A'):
			total += 11
		else:
			total += card
			
	if (total > 21 and 'A' in hand):
		for card in hand:
			if (card == 'A'):
				total -= 10
				if (total <= 21):
					return total
		
	return total

chipTotal = 1000
d = deck()
d.shuffle_deck()
keepPlaying = 1
while (keepPlaying == 1):

	playerTotal = 0
	dealerTotal = 0
	playerCards = []
	dealerCards = []
	currentBet = 0
	dealerNatural = 0

	print("Your current Chip total is: " + str(chipTotal))
	print ("Enter the amount you want to bet")
	
	while (1):
		try:
			userInput = int(input())
		except ValueError:
			print("Enter a valid bet")
			continue
		if (isinstance(userInput, int) is False or userInput <= 0):
			print("Enter a valid bet")
		elif (chipTotal - userInput < 0):
			print("You do not have enough chips to make that bet")
		else:
			currentBet = userInput
			break

	dealerCards.append(d.take_top_card())
	playerCards.append(d.take_top_card())
	dealerCards.append(d.take_top_card())
	playerCards.append(d.take_top_card())

	print ("Dealer's Up Card: " + str(dealerCards[1]))
	print ("Your Cards: " + str(playerCards[0]) + ", " + str(playerCards[1]))

	playerTotal = calculate_hard_total(playerCards)
	dealerTotal = calculate_hard_total(dealerCards)

	if (playerTotal == 21):
		print("Natural Blackjack! Checking if Dealer also has a natural...")
		if (dealerTotal == 21):
			print("Dealer also had a natural, so it is a Push")
		else:
			print("Dealer does not have a natural, you win! Payout is 3:2")
			chipTotal += int(currentBet * 1.5)
	else:
		cont = 1
		while (cont == 1):
			if (playerTotal == 21):
				decision = 's'
			else:
				print("Hit, Stand or Double Down? (type h for hit, s for stand, d for double down)")
				while(1):
					decision = input()
					if (decision != 'h' and decision != 's' and decision != 'd'):
						print("Please enter h or s or d")
					elif (chipTotal - (currentBet * 2) < 0 and decision == 'd'):
						print("You do not have enough chips to double down")
					else:
						break
			if (decision == 'h'):
				playerCards.append(d.take_top_card())
				print ("Your Cards: " + str(playerCards))
				playerTotal = calculate_hard_total(playerCards)
				if (playerTotal > 21):
					cont = 0
			elif (decision == 'd'):
				print("Doubling Down...")
				currentBet = currentBet * 2
				playerCards.append(d.take_top_card())
				print ("Your Cards: " + str(playerCards))
				playerTotal = calculate_hard_total(playerCards)
				cont = 0
			elif (decision == 's'):	
				cont = 0
				dealercont = 1
				print("Dealer flips: has hand:" + str(dealerCards))
				if (dealerTotal == 21):
					print ("Dealer has a natural and you don't, so he wins")
					chipTotal -= currentBet
					dealerNatural = 1
					dealercont = 0
				while(dealercont == 1):
					if (dealerTotal < 17):
						print("Dealer has less than 17, so he hits")
						dealerCards.append(d.take_top_card())
						dealerTotal = calculate_hard_total(dealerCards)
						print("Dealer's hand:" + str(dealerCards))
					else:
						dealercont = 0
		print("")
		print("Your Score: " + str(playerTotal))
		print("Dealer's Score: " + str(dealerTotal))
	
		if (playerTotal > 21):
			print("You Busted!")
			chipTotal -= currentBet
		elif (dealerTotal > 21):
			print("Dealer Busted, You win!")
			chipTotal += currentBet
		elif (playerTotal == dealerTotal and dealerNatural == 0):
			print("Push")
		elif (playerTotal < dealerTotal and dealerNatural == 0):
			print("Dealer Wins")
			chipTotal -= currentBet
		else:
			print("You win!")
			chipTotal += currentBet
	if (chipTotal == 0):
		print("Looks like you ran out of chips. Oops")
		exit
	print ("Cards left in deck: " + str(d.total_cards()))
	print ("Chip Total: " + str(chipTotal))
	print ("Current 'count': " + str(d.current_count()))
	print ("Keep playing? (y or n)")
	
	while(1):
		yesOrNo = input()
		if (yesOrNo == 'n'):
			keepPlaying = 0
			break
		elif (yesOrNo == 'y'):
			keepPlaying = 1
			dealerNatural = 0
			break
		else:
			print("Please enter y/n")
		