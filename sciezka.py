#tworzy katalogi i zwraca sciezke, pod ktora trzeba stworzyc plik
from pathlib import Path


# zwracamy sciezke oraz bool w zaleznosci czy poprawnie utworzono katalog 
def generujSciezke(miesiac:str, dzien:str, pora:str = "rano") -> tuple[str, bool]:
    sciezka = Path(miesiac, dzien, pora)
    katalog_istnieje = sciezka.is_dir()
    katalog_nie_istnieje = not katalog_nie_istnieje

    if(katalog_istnieje):
        return (sciezka, 0)
    else:
        sciezka.mkdir(parents=True, exist_ok=True)
        if sciezka.is_dir():
            return (sciezka, 1)
        else:
            return (sciezka, 0)

    



