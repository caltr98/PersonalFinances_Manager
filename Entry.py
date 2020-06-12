import random
import datetime

class entry:

    def __init__(self, desc, amount, per):
        self.id = random.randint(0,100000)
        self.date = datetime.date.today()
        self.descript = desc
        self.amount = amount
        self.period = per

    def getId(self):
        return self.id

    def getDate(self):
        return self.date

    def getDesc(self):
        return self.descript

    def getAmo(self):
        return self.amount

    def getPeriod(self):
        return self.period

    def toStringDate(self):
        return str(self.date)

    def setDesc(self,dsc):
        self.descript = dsc

    def setAmount(self, amt):
        self.amount = amt

    def setPeriod(self, per):
        self.period = per

    def display(self):
        print('ID: ', self.id, 'DATA: ', self.toStringDate(), 'NOTE: ', self.descript, 'IMPORTO: ', self.amount, 'PERIODO: ', self.period)


