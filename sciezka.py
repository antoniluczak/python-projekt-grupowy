from pathlib import Path


def generuj_sciezke(miesiac: str, dzien: str, pora: str = "rano") -> tuple[Path, bool]:
    sciezka = Path(miesiac, dzien, pora)

    # Jeśli katalog już istnieje, zwracamy samą sciezke
    if sciezka.is_dir():
        return (sciezka)

    # Próba utworzenia nowego katalogu
    sciezka.mkdir(parents=True, exist_ok=True)
    return (sciezka)
   
