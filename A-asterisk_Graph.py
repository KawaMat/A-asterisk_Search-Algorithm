

nazwa_pliku = "1.txt"

import sys
import math

punkty = {}
start_stop = []
temp_string = ""
temp_list = []

###############################    pobieranie punktów do postaci słowników, gdzie kluczami za numery pkt, a wartosciami  "int-y" współrzędnych

string = open(nazwa_pliku,"r").readline()
string = string.rstrip()
string = string.replace(', ',',')
string = string.replace('(','')
string = string.replace(')','')
string = string.replace(' ','.')
string = string.split('.')
string = [x.split(',') for x in string]
for i in range(len(string)):                    # tworzenie slownika gdzie wartosciami sa listy intow wspolrzednych
     punkty[i+1] = [int(string[i][0]),int(string[i][1])]
ile_pkt = len(punkty.keys())

################################  pobieranie do listy punktu pocz i końc. w postaci int-ów

start_stop = open(nazwa_pliku,"r").readlines()[1]
start_stop = start_stop.rstrip()
start_stop = start_stop.split(' ')
start_stop = [int(start_stop[0]) , int(start_stop[1])]

if start_stop[0]>len(punkty.keys()) or start_stop[1]>len(punkty.keys()):   # warunek dzialania programu - okerslone wartosci pocz i konca musza miescic sie w przedziale istniejacych punktów
    print("BLAD!: WYBRANY PUNKT POCZATKOWY LUB KONCOWY JEST SPOZA PRZEDZIALU")
    sys.exit(0)

################################## tworzenie macierzy sasiedztwa w postaci listy list

macierz_s = []
temp_string = ""
flaga =0
num = 1

for x in range(ile_pkt):
    file = open(nazwa_pliku, "r")
    string = file.readlines()[2+x]
    temp_list = string.rsplit()
    for i in range(ile_pkt):
        temp_list[i] = float(temp_list[i])
    macierz_s.append(temp_list)

############################### robienie slownika sasiadow dla kazdego punktu

dict_sasiad = dict.fromkeys(punkty.keys(),[]) # tworzenie pustego slowniaka na listy jako wartosci i nr punktow jako klucze

temp_k=[]                                     # kazdej podyzji w macierzy wiekszej od 0 nr wiersza staje sie kluczem a nr kolumnu dopisuje sie do listy wartosci przy tym kluczu
for i in range(ile_pkt):
    for k in range(ile_pkt) :
         if macierz_s[i][k] > 0:
            temp_k.append(k+1)
            dict_sasiad[i+1] = list(temp_k)
    temp_k.clear()

################################## dopisywanie do slownika punktow wartosci heurystyk


for i in range(ile_pkt):                        # Długość przekątnej Pitagorasa pomiedzy każdym punktem a punktem końcowym dopisywana jest do listy wartości w słowniku punkty na 2 pozycji liczac od zera, po wartościach wspołrzędnych
    if len(dict_sasiad[i+1]) == 0:
        punkty[i+1].append(-1)
        continue
    odleglosc = math.sqrt( (punkty[i+1][0]-punkty[start_stop[1]][0])**2 + (punkty[i+1][1]-punkty[start_stop[1]][1])**2)
    punkty[i+1].append(odleglosc)
    
################################# #wyświetlanie wartości pobranych do programu z pliku .txt

print("Wczytano:\nPunkty: ", punkty, "\nPoczatek sciezki: ", start_stop[0], "\nKoniec sciezki: ", start_stop[1],
      "\nMacierz sasiedztwa: ", macierz_s)

################################# Creme de la creme - A*

start = start_stop[0]
meta = start_stop[1]

rozpatrywane = {start}
przyszedlz ={}
g = dict.fromkeys(punkty.keys(), math.inf)
g[start] = 0
f = dict.fromkeys(punkty.keys(), math.inf)
f[start] = punkty[start][2]
x=0
while len(rozpatrywane):
    temp = math.inf
    for i in rozpatrywane:              # wybieranie wierzcholka o najmniejszym f sposrod rozpatrywnych
        if f[i] < temp:
            x = int(i)
            temp = f[i]
    if x == meta:                       #jeśli natrafimy na wierzcholek koncowy przelicza trase
        droga = [x]
        temp = math.inf
        flaga=0 ## jezeli droga ma tylko 2 wierzcholki to while ponizej sie nie wykona i wtedy zadziala if pod while-em
        temp = przyszedlz[x]
        while temp != start:
            droga.append(temp)
            if temp == start: break
            temp = przyszedlz[temp]
            if temp == start: droga.append(temp); break
            flaga =1
        if flaga == 0: droga.append(temp)
        droga.reverse()
        print('_'*180,'\nDroga biegnie przez wierzcholki: ',droga)
        sys.exit(0)

    rozpatrywane.remove(x)          #rozpatrywany jest usuwany z listy rozpatrywanych w przyszlosci
    for y in dict_sasiad[x]:         #dla kazdego sasiada z rozpatrywanych porownywane jest i ewentualne podmienianie wartosci g,f, zmiana wartosci w slowniku skad przyszedl, jeśli sasiada nie bylo w rozpatrywanych to ie go dopisuje
        temp_g = g[x] + float(macierz_s[x-1][y - 1])
        if temp_g < g[y]:
            przyszedlz[y] = x
            g[y] = temp_g
            f[y] = g[y] + punkty[y][2]
            if not(y in rozpatrywane):
                rozpatrywane.add(y)

print("Nie znaleziono drogi dla tego grafu")




