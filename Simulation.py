import random
import agent
import matplotlib.pyplot as plt

class Simulation(object):

    def __init__(self, priceProtection, priceInsurance, initialProtabilitySteal, averageUtility, numberAgents ):
        self.agents = []
        self.priceProtection = priceProtection
        self.priceInsurance = priceInsurance
        self.initialProbabilitySteal = initialProtabilitySteal
        self.averageUtility = averageUtility

        self.totalCountInsurance = []
        self.totalCountProtected = []
        self.totalPriceInsurenace = []
        for i in range(numberAgents):
            initialRich = float(random.uniform(0, 100) / 100)
            initialLost = initialRich * 0.75
            initialProtect = random.randint(0,1)
            initialInsurance = random.randint(0,1)
            initailProbabilitySteal = 0.2,
            initialExpectUtility = random.uniform(0,1)
            initialSteal = random.randint(0,1)
            initialRichFinal = 0.6
            self.agents.append(agent.Agent(initialRich , initialLost,initialProtect , initialInsurance,  initailProbabilitySteal, initialExpectUtility, initialRichFinal))

    def simulation (self,numberPeriods):
        for i in range(numberPeriods):
            self.period()
        self.showChart(numberPeriods)
    def period(self):

        self.globalUpdate()
        self.agentUpdate()
        self.calculateAgents()


    def globalUpdate(self):
        if self.initialProbabilitySteal < 0.5:
            self.initialProbabilitySteal = random.uniform(0, self.initialProbabilitySteal * 0.2)
        else:
            self.initialProbabilitySteal = random.uniform(self.initialProbabilitySteal * 2, 1.1)

    def agentUpdate(self):

        for i in self.agents:
            self.selectFriend(i)
        for i in self.agents:
            i.updateUtility(self.priceProtection, self.priceInsurance, self.averageUtility)
        for i in self.agents:
            i.updateStealing(self.initialProbabilitySteal)
        for i in self.agents:
            i.updateLevelRichness(self.priceProtection, self.priceInsurance)

        counterAgentsInsurance = 0
        counterAgentsInsuranceAndSteal = 0
        for i in self.agents:
            counterAgentsInsurance = counterAgentsInsurance + i.isInsurance
            counterAgentsInsuranceAndSteal = counterAgentsInsuranceAndSteal + i.isInsurance * i.isSteal
        self.priceInsurance = self.agents[0].lostSteal * (counterAgentsInsuranceAndSteal/counterAgentsInsurance)

        totalRich = 0
        for i in self.agents:
            totalRich = totalRich + i.richLevel
        self.averageUtility = totalRich / len (self.agents)

    def selectFriend(self, agent):
        isSelectedAFriend = True
        while isSelectedAFriend:
            friend = random.randint(0, len(self.agents) - 1)
            if self.agents[friend] != agent:
                agent.friend = self.agents[friend]
                isSelectedAFriend = False

    def calculateAgents(self):
        auxTotalCountInsurance = 0
        auxTotalCountProtected = 0
        priceInsurance = 0
        for i in self.agents:
            auxTotalCountInsurance = auxTotalCountInsurance + i.isInsurance
            auxTotalCountProtected = auxTotalCountProtected + i.isProtect
        self.totalCountProtected.append( auxTotalCountProtected / len(self.agents))
        self.totalCountInsurance.append( auxTotalCountInsurance / len(self.agents))
        self.totalPriceInsurenace.append(self.priceInsurance)
    def showChart(self,numberSimulation):
        plt.plot(range(numberSimulation), self.totalPriceInsurenace, color='g')
        plt.plot(range(numberSimulation), self.totalCountInsurance, color='red')
        plt.plot(range(numberSimulation), self.totalCountProtected, color='blue')


        plt.xlabel('Number simulation')
        plt.ylabel('price')
        plt.title('Insurance simulation')
        plt.show()

        csv = open('insurance.csv', 'w')
        csv.write("totalcountprotected,totalCountInsurance,totalPriceInsurance\n")
        for row in range(len(self.totalCountProtected)):
            csv.write(str(self.totalCountProtected[row]) + "," + str(self.totalCountInsurance[row]) + "," + str(self.totalPriceInsurenace[row]) + "\n")
        csv.close()
if __name__ == '__main__':
    priceProtection = 0.05
    priceInsurance = 0.90
    initialProtabilitySteal = 1
    averageUtility = 0.80
    numberAgents = 500
    s = Simulation(priceProtection, priceInsurance, initialProtabilitySteal, averageUtility, numberAgents)
    s.simulation(2000)

