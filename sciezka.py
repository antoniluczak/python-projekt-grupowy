#tworzy katalogi i zwraca sciezke, pod ktora trzeba stworzyc plik
def generujSciezke(miesiac:str, dzien:str, pora:str) -> tuple[str, bool]:
    sciezka = miesiac + '/' + dzien + '/' + pora
    try:
        with open(sciezka, "r") as file:
            zawartosc = file.read()
    except


