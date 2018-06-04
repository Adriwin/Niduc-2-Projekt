#Selective Repeat Protocol

from Channel import *
from TMR import *
from Hamming import *
from tkinter import *

class SelectiveRepeatGUI:
    sourcePackages = [] #pakiety ze zrodla
    destPackages = [] #gotowe "przemielone" pakiety
    ###########################################################
    protocol = None #protocol z funkcja sprawdzajaca poprawnosc IsValid !!!
    ###########################################################
    channelModel = None #model channelu
    window = 0 #ilosc pakietow w oknie tzn. ile na raz pakietow zostanie wyslanych
    errorCounter = 0 #ogolna ilosc NAKów

    def __init__(self, src, chan, prot, win, isBSC, tk):
        self.sourcePackages = src
        self.channelModel = chan
        self.protocol = prot
        self.window = win
        self.errorCounter = 0
        self.isBSC = isBSC
        self.countOfRelay = 0
        self.tk = tk
        self.waitForNextStep = True
        self.isWindowDestroyed = False

    def getDestinationPackets(self): #zwraca "przerobiony" plik
        return self.destPackages

    def getErrors(self):
        return self.errorCounter

    def _nextStep(self):
        self.waitForNextStep = False

    def _delete_window(self):
        self.root.destroy()
        self.isWindowDestroyed = True
        self.waitForNextStep = False

    def transmit(self):   #TRANSMITUJE PAKIETY Z sourcePackages do destPackages

        # Ustawienie GUI
        self.root = Toplevel(self.tk)
        self.root.protocol("WM_DELETE_WINDOW", self._delete_window)
        canvas = Canvas(self.root, width=300, height=300, bg="#e5b390")
        canvas.pack()
        self.root.title("Selective Repeat")

        strLab = "Count of package to send: " + str(len(self.sourcePackages))
        countPackage = Label(canvas, text=strLab)
        canvas.create_window(100, 20, window=countPackage)

        packetLabelText = StringVar()
        packetLabel = Label(canvas, textvariable=packetLabelText)
        canvas.create_window(70, 60, window=packetLabel)

        receiveLabelText = StringVar()
        receiveLabel = Label(canvas, textvariable=receiveLabelText)
        canvas.create_window(30, 100, window=receiveLabel)

        buttonWaitForNextStep = Button(canvas, text="NEXT STEP", command=self._nextStep)
        buttonWaitForNextStep.configure(width=40, height=3)
        canvas.create_window(150, 150, window=buttonWaitForNextStep)

        canvas.update()

        print("Rozpoczynam transmisje danych")

        buffer = [] # wyslane paczki
        indexes = [] #indeksy paczek
        errorBuf = [] #bufor zlych paczek
        errorIndexes = [] #indeksy zlych paczek

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

        while(sended < packets or len(errorBuf) > 0):  # ! U W A G A JEZELI JEST ZBYT DUZO BLEDOW TO PLIK NIE PRZEJDZIE BO SENDED DOJDZIE DO KONCA A ERRORBUF NIE BEDZIE PUSTY
            print("petla nr {}".format(sended))

            # dodajemy do bufora pakiety,
            # jezeli byly wczesniej jakies bledy to dodajemy mniej nowych pakietow bo miejsce w buforze zajmuja pakiety ktore trzeba wyslac od nowa
            while (len(buffer) < self.window - len(errorBuf) and sended < packets):

                # ZAKLOCANIE
                if (self.isBSC):
                    buffer.append(self.channelModel.addBSCNoise(self.sourcePackages[sended]))
                else:
                    buffer.append(self.channelModel.addGilbertNoise(self.sourcePackages[sended]))

                # Show nr of package
                packetLabelText.set("Nr package to send: " + str(sended))
                while (self.waitForNextStep):
                    canvas.update()

                if (self.isWindowDestroyed == False):
                    self.waitForNextStep = True
                canvas.update()

                indexes.append(sended)
                sended += 1
                #print("dodaje {}".format(sended))

            errors = [] #zbior blednych paczek w jednym oknie bufora

            #ODBIERANIE PAKIETOW
            while (len(buffer) > 0):
                packet = buffer.pop()
                index = indexes.pop()
                if (self.protocol.isValid(packet)): #TUTAJ BEDZIEMY SPRAWDZAC ACK == TRUE, NAK == FALSE
                    #print("\tpaczka prawidlowa")

                    # get ACK
                    receiveLabelText.set("ACK: " + str(index))
                    while (self.waitForNextStep):
                        canvas.update()

                    if (self.isWindowDestroyed == False):
                        self.waitForNextStep = True
                    canvas.update()

                    self.destPackages[index] = packet  # paczka zapisana
                else:
                    # get NAK
                    receiveLabelText.set("NAK: " + str(index))
                    while (self.waitForNextStep):
                        canvas.update()

                    if (self.isWindowDestroyed == False):
                        self.waitForNextStep = True
                    canvas.update()

                    print("\tpaczka NIEprawidlowa")
                    errors.append(index)  #  dodanie INDEKSU paczki jako bledna
                    self.errorCounter += 1
            while (len(errorBuf) > 0):  # jezeli w glownym buforze z blednymi paczkami sa jakies paczki to nastepuja proba ich wyslania
                packet = errorBuf.pop()
                index = errorIndexes.pop()
                print("Proba wyslania BLEDNYCH pakietow")

                # Show nr of package
                packetLabelText.set("Nr package to send: " + str(index))
                while (self.waitForNextStep):
                    canvas.update()

                if (self.isWindowDestroyed == False):
                    self.waitForNextStep = True
                canvas.update()

                if (self.protocol.isValid(packet)): # Sprawdzenie odkodowanego tymczasowo pakietu z TMR
                    print("\tpaczka prawidlowa")

                    # get ACK
                    receiveLabelText.set("ACK: " + str(index))
                    while (self.waitForNextStep):
                        canvas.update()

                    if (self.isWindowDestroyed == False):
                        self.waitForNextStep = True
                    canvas.update()

                    self.destPackages[index] = packet  # zapisanie paczki
                else:
                    # get NAK
                    receiveLabelText.set("NAK: " + str(index))
                    while (self.waitForNextStep):
                        canvas.update()

                    if (self.isWindowDestroyed == False):
                        self.waitForNextStep = True
                    canvas.update()

                    print("\tpaczka NIEprawidlowa")
                    errors.append(index)  # dodanie paczki jako bledna
                    self.errorCounter += 1
            while (len(errors) > 0):  # dodanie paczek do glownego bufora z blednymi paczkami, zostana wyslane w nastepnym kroku petli
                self.countOfRelay += 1
                index = errors.pop()
                if (self.isBSC):
                    errorBuf.append(self.channelModel.addBSCNoise(self.sourcePackages[index]))
                else:
                    errorBuf.append(self.channelModel.addGilbertNoise(self.sourcePackages[index]))
                errorIndexes.append(index)

        print("Ilosc retranmisji: " + str(self.countOfRelay))
