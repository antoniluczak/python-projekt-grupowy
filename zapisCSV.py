import csv 
import random
import os

#przyjmuje sciezke bez nazwy pliku,
#tworzy plik jezeli go nie ma, zapisuje od nowa jezeli jest

def dodajDaneCSV(sciezka):
    dane = ["Model","Wynik","Czas"]
    y = os.path.join(sciezka,"Dane.csv")
    with open(y, "w", encoding = "utf-8",newline = '') as plik:
        obiekt = csv.writer(plik,delimiter = ";")
        obiekt.writerow(dane)
        obiekt.writerow(_losuj())

def _losuj():
    x = random.choice(["A","B","C"])
    y = random.randint(0,1000)
    z = random.randint(0,1000)
    return [x,y,z]

#przyjmuje tablice sciezek
#dla kazdej sciezki sprawdza,czy w niej istnieje plkik csv
#jezeli tak, to dodaje czas z niego
#jezeli nie, to nic nie dodaje
#zwraca wynik (int)
def zczytajCSV(sciezka):
    j = 0
    for i in sciezka:
        y = os.path.join(i, "Dane.csv")
        if os.path.isfile(y):
            with open(y,"r",encoding = "utf-8") as plik:
                obiekt = csv.reader(plik, delimiter=';')
                pl = next(obiekt)
                pl = next(obiekt)
                j += int(pl[2])
        else:
            raise  FileNotFoundError('There is a folder without existing file')
    return j

   
