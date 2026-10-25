from pathlib import Path


def generuj_sciezke(miesiac: str, dzien: str, pora: str = "rano") -> tuple[Path, bool]:
    sciezka = Path(miesiac, dzien, pora)

    # Jeśli katalog już istnieje, zwracamy (sciezka, False) i nie tworzymy go ponownie
    if sciezka.is_dir():
        return (sciezka, False)

    # Próba utworzenia nowego katalogu
    try:
        sciezka.mkdir(parents=True, exist_ok=True)
        return (sciezka, True)
    except OSError:
        # Zwraca False, jeśli wystąpił błąd zapisu (np. brak uprawnień)
        return (sciezka, False)
