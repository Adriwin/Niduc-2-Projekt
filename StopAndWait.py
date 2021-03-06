#Stop And Wait Protocol

from Channel import *
from TMR import *

class StopAndWait:
    sourcePackages = [] #pakiety ze zrodla
    destPackages = [] #gotowe "przemielone" pakiety
    ###########################################################
    protocol = None #protocol z funkcja sprawdzajaca poprawnosc IsValid !!!
    ###########################################################
    channelModel = None #model channelu
    errorCounter = 0 #ogolna ilosc NAKów

    def __init__(self, src, chan, prot, isBSC):
        self.sourcePackages = src
        self.channelModel = chan
        self.protocol = prot
        self.isBSC = isBSC
        self.errorCounter = 0
        self.countOfRelay = 0

    def getDestinationPackets(self): #zwraca "przerobiony" plik
        return self.destPackages

    def getErrors(self):
        return self.errorCounter

    def transmit(self):   #TRANSMITUJE PAKIETY Z sourcePackages do destPackages
        # print("Rozpoczynam transmisje danych")
        packetsize = len(self.sourcePackages[0])

        tempDest = []
        for i in range(0,len(self.sourcePackages)):
            temp = []
            for j in range(0,packetsize):
                temp.append('0')
            tempDest.append(temp)

        self.destPackages = tempDest

        sended = 0 # ilosc wyslanych pakietow
        packets = len(self.sourcePackages) #ilosc pakietow

        while(sended < packets):  # ! U W A G A JEZELI JEST ZBYT DUZO BLEDOW TO PLIK NIE PRZEJDZIE BO SENDED DOJDZIE DO KONCA A ERRORBUF NIE BEDZIE PUSTY
            # print("petla nr {}".format(sended))
            if(self.isBSC):
                packet = self.channelModel.addBSCNoise(self.sourcePackages[sended])
            else:
                packet = self.channelModel.addGilbertNoise(self.sourcePackages[sended]) # ZAKLOCANIE

            #ODBIERANIE PAKIETOW
            while (self.protocol.isValid(packet) == False): # Sprawdzenie odkodowanego tymczasowo pakietu z TMR
                #TUTAJ BEDZIEMY SPRAWDZAC ACK == TRUE, NAK == FALSE
                self.errorCounter += 1
                # print("\twysylanie pakietu {}".format(sended))
                if (self.isBSC):
                    packet = self.channelModel.addBSCNoise(self.sourcePackages[sended])
                else:
                    packet = self.channelModel.addGilbertNoise(self.sourcePackages[sended])

                self.countOfRelay += 1

            self.destPackages[sended] = packet  # paczka zapisana
            sended += 1

        print("Ilosc retranmisji: " + str(self.countOfRelay))