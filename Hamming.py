import numpy
from FileOperator import *

class Hamming:

    def createPacket4(self, pack): # robimy z naszych pakiecikow po 8, pakieciki po 4 do Hamminga
        packet = []
        newPacket = []
        counter = 0
        for bit in pack:
            if bit == '1':
                packet.append(1)
                counter += 1
            if bit == '0':
                packet.append(0)
                counter += 1
            if counter == 4:
                newPacket.append(packet)
                counter = 0
                packet = []
                '''
        length = len(packet)
        for i in range(0, 4 - length):
            packet.append(0)
        newPacket.append(packet)
        packet = []
        # kolejny wiersz, mowi ile zostalo dodanych 0
        if length == 1:
            packet.append(0)
            packet.append(0)
            packet.append(1)
            packet.append(1)
        if length == 2:
            packet.append(0)
            packet.append(0)
            packet.append(1)
            packet.append(0)
        if length == 3: # ilosc dodanych 0
            packet.append(0)
            packet.append(0)
            packet.append(0)
            packet.append(1)
        if length == 0:
            packet.append(0)
            packet.append(0)
            packet.append(0)
            packet.append(0)
        newPacket.append(packet)
        '''
        matrix = numpy.asarray(newPacket)
        return matrix

    def codeHamming(self, pack):   # uzywajac macierzy G kodujemy nasz pakiecik
        newPacket = self.createPacket4(pack)
        g = numpy.array([
            [1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1]
        ])  # (4,7)
        enc = numpy.dot(newPacket, g)%2
        return self.numpyToChar(enc)

    def parityCheck(self, enc): #uzywamy macierzy H aby stworzyc macierz na ktorej sprawdzimy czy sa bledy
        enc = self.charToNumpy(enc)
        h = numpy.array([
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ]) #(3,7)
        parch = numpy.dot(h, enc.T)%2
        parch = parch.T
        charParch = self.numpyToChar(parch)
        return charParch

    def isValid(self, enc):
        parch = self.parityCheck(enc)
        dlugosc = 0
        suma = 0
        for bit in parch: # liczymy od 0
            if bit == '1':
                number = 1*pow(2, dlugosc) # liczymy z binarki od razu na system dziesietny
                dlugosc += 1
                suma += number
            else:
                dlugosc += 1
        if suma > len(enc):
            return False #sa minimum 2 bledy, hamming juz tego nie ogarnie
        else:
            return True #nie ma bledu lub jest tylko 1 wiec mozna naprawic

    def decodeHamming(self, enc): # uzywamy macierz R do odkodowania
        # print("enc przed zmiana: ")
        # print(enc)
        # print("enc po zmianie:")
        # enc[0] = '1'
        # enc[3]='1'
        # print(enc)
        r = numpy.array([
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 1]
        ])
        parch = self.parityCheck(enc)
        # print("parch po zmianach: ")
        # print(parch)
        dlugosc = 0
        suma = 0
        for bit in parch: # liczymy od 0
            if bit == '1':
                number = 1*pow(2, dlugosc) # liczymy z binarki od razu na system dziesietny
                dlugosc += 1
                suma += number
            else:
                dlugosc += 1
        # print(suma)
        if suma < len(enc):
            for index, bit in enumerate(enc): # jezeli bylo 0 robimy 1, a z 1 robimy 0
                if index == suma & suma != 0:
                    if enc[index-1] == '1':
                        enc[index-1] = '0'
                    else:
                        enc[index-1] = '1'
        # print("enc po poprawie: ")
        # print(enc)
        enc = self.charToNumpy(enc)
        dec = numpy.dot(r, enc.T)
        charDec = self.numpyToChar(dec)
        '''
        b1 = charDec[len(charDec)-1] # ostatni bit
        b2 = charDec[len(charDec)-2] # przedostatni bit
        if b1 == '1' and b2 == '1': # 3 zera dodane
            charDec = charDec[:-7]
        if b1 == '0' and b2 == '1': # 2 zera dodane
            charDec = charDec[:-6]
        if b1 == '1' and b2 == '0': # 1 zero dodane
            charDec = charDec[:-5]
        if b1 == '0' and b2 == '0': # 0 zer dodanych :d
            charDec = charDec[:-8]
            '''
        return charDec

    def numpyToChar(self, enc):
        chA = []
        for row in enc:
            for col in row:
                if col == 1:
                    chA.append('1')
                if col == 0:
                    chA.append('0')
        return chA

    def charToNumpy(self, list):
        row = []
        col = []
        i = 0
        for char in list:
            if(char == '1'):
                col.append(1)
            else:
                col.append(0)

            i += 1

            if(i == 7):
                i = 0
                row.append(col)
                col = []

        return numpy.array(row)

    def chToInt(self, chA):
        intA = []
        for bit in chA:
            if bit == '1':
                intA.append(0)
            if bit == '0':
                intA.append(0)
        return numpy.array(intA)


#mala zabawa i powtorka z algebry
'''
a = numpy.array([[1,2],[3,4]])
b = numpy.array([[1,2],[3,4]])
wynik1 = numpy.dot(a,b)
b = numpy.transpose(b)
wynik2 = numpy.dot(a,b)
print(wynik1)
print(wynik2)
'''

# podstawowe testy


# bitList = []
# #bitList = ['0','0','0','0','0','0','0','0','0','0','0','1']
# #bitList = ['1','0','1','1','0']
# bitList = ['1','0','1','1']
# fileOperator = FileOperator()
# #bitList = fileOperator.readFile("test.txt")
# print(bitList)
# print("dlugosc bit list na samym pcozatku: ")
# print(len(bitList))
# hamming = Hamming()
# bitList = hamming.codeHamming(bitList)
# print("code hamming: ")
# print(bitList)
# print("dlugosc bit list po code: ")
# print(len(bitList))
# print("code paritycheck: ")
# print(hamming.parityCheck(bitList))
# print("dlugosc bitlist przed")
# print(len(bitList))
# bitList = hamming.decodeHamming(bitList)
# print("decode hamming: ")
# print(bitList)
# print("dlugosc bitlist po")
# print(len(bitList))

# testy kodu od Sembereckiego
'''
G = numpy.array([
    [1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1]
])

H = numpy.array([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1]
])

R = numpy.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1]
])


input_data = numpy.array([[1, 0, 1, 1]])  # dane wejsciowe
data_vector = numpy.dot(input_data, G) % 2  # obliczony wektor danych
#data_vector_noised = numpy.array([[0, 1, 1, 1, 0, 1, 1]])  # wektor sluzacy do sprawdzania dzialania syndromu
#syndrome_noised = numpy.dot(H, data_vector_noised.T) % 2
syndrome = numpy.dot(H, data_vector.T) % 2
# dane wyjsciowe uzyskane z rowmam
# output_data = [data_vector_const[0][2], data_vector_const[0][4], data_vector_const[0][5], data_vector_const[0][6]]
output_data = numpy.dot(R,  data_vector.T)
print("Dane wejsciowe")
print(data_vector)
print("Dane wejsciowe zaklocone")
#print(data_vector_noised)
print("Syndrom zaklocony")
#print(syndrome_noised)
print("Syndrom")
print(syndrome)
print("Odkodowane dane")
print(output_data)
'''