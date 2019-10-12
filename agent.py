
import random


class Agent(object):
    def __init__(self, richLevel, lostSteal, isProtect, isInsurance, probabilitySteal, expectUtility, isSteal, levelRichFinal):
        self.richLevel = richLevel
        self.lostSteal = lostSteal
        self.isProtect = isProtect
        self.isInsurance =isInsurance
        self.probabilitySteal = probabilitySteal
        self.expectUtility = expectUtility
        self.isSteal = isSteal
        self.levelRichFinal = levelRichFinal
        self.friend = None
        strategy = 1
        if strategy == 0:
            self.strategy = StrategyMax(self)
        elif strategy == 1:
            self.strategy = StrategyImitation(self)
        else:
            self.strategy = StrategyCorrect(self)

    def updateUtility(self, cr, cs, au):
        #self.richLevel - self.probabilitySteal * self.lostSteal * (1 - int(self.isInsurance)) - int(self.isProtect) * cr - int(self.isInsurance) * cs
        self.expectUtility = self.strategy.usefulPercent(cr, cs, au)
    def updateStealing(self,pa0):
        value = random.uniform(100,0)
        if value < pa0 and not self.isProtect:
            self.isSteal = True
        else:
            self.isSteal = False
    def updateLevelRichness(self,cr,cs):
        self.richLevel = self.richLevel - self.lostSteal - self.isSteal * ( 1 - self.isInsurance) - self.isProtect * cr - self.isInsurance * cs

class Strategy(object):
    def __init__(self,parent):
        self.parent = parent
        pass
    def updateUsefulPercent(self,cr,cs,au):
        pass

class StrategyMax(Strategy):
    def __init__(self, parent):
        super(StrategyMax, self).__init__(parent)

    def usefulPercent(self,cr,cs,au):

        ucase0 = self.parent.richLevel - self.parent.probabilitySteal * self.parent.lostSteal * (1 - 0) - (0 * cr) - (0 * cs)
        ucase1 = self.parent.richLevel - self.parent.probabilitySteal * self.parent.lostSteal * (1 - 1) - (0 * cr) - (1 * cs)
        ucase2 = self.parent.richLevel - self.parent.probabilitySteal * self.parent.lostSteal * (1 - 0) - (1 * cr) - (0 * cs)
        return max(ucase0, ucase1, ucase2)

class StrategyImitation(Strategy):
    def __init__(self, parent: Agent):
        super(StrategyImitation, self).__init__(parent)

    def usefulPercent(self, cr, cs,au):
        if (self.parent.friend.richLevel > self.parent.richLevel):
            self.parent.isProtect = self.parent.friend.isProtect
            self.parent.isInsurance = self.parent.friend.isInsurance
        self.parent.richLevel - self.parent.probabilitySteal * self.parent.lostSteal * (1 - self.parent.isInsurance) - self.parent.isProtect * cr - self.parent.isInsurance * cs


class StrategyCorrect(Strategy):
    def __init__(self, parent: Agent):
        super(StrategyCorrect, self).__init__(parent)

    def usefulPercent(self, cr, cs, au):
        if (self.parent.expectUtility < au):
            if self.parent.isInsurance and not self.parent.isProtect:
                self.parent.isInsurance = False
                self.parent.isProtect = True
            elif not self.parent.isInsurance and self.parent.isProtect:
                self.parent.isInsurance = True
                self.parent.isProtect = False
            elif not self.parent.isInsurance and not self.parent.isProtect:
                coin = random.randint(0, 1)
                if coin == 0:
                    self.parent.isInsurance = False
                    self.parent.isProtect = True
                else:
                    self.parent.isInsurance = True
                    self.parent.isProtect = False
        return self.parent.richLevel - self.parent.probabilitySteal * self.parent.lostSteal * (1 - self.parent.isInsurance) - self.parent.isProtect * cr - self.parent.isInsurance * cs


