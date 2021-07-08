class Player(object):
    def __init__(self, currentSum, usableAce, dealerCard):
        self.currentSum = currentSum
        self.usableAce = usableAce
        self.dealerCard = dealerCard
        self.usingAce = self.usableAce

    def receiveCard(self, card):
        if self.usingAce and self.currentSum + card > 21:
            self.usingAce = False
            self.currentSum += card - 10
        else:
            self.currentSum += card

    def getState(self):
        return self.currentSum, self.usableAce, self.dealerCard

    def getValue(self):
        return self.currentSum

    def shouldHit(self, policy):
        return policy[self.getState()]

    def bust(self):
        return self.getValue() > 21

class Dealer(object):
    def __init__(self, cards):
        self.cards = cards

    def receiveCard(self, card):
        self.cards.append(card)

    def getValue(self):
        sum, aceCount = 0, 0
        for card in self.cards:
            if card == 1:
                aceCount += 1
            else:
                sum += card
        while aceCount > 0:
            aceCount -= 1
            sum += 11
            if sum > 21:
                aceCount += 1
                sum -= 11
                sum += aceCount
                break
        return sum

    def shouldHit(self):
        if self.getValue() < 17:
            return True
        else:
            return False

    def bust(self):
        return self.getValue() > 21
        