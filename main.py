import argparse
import re
import sciezka
import zapisCSV
import jsonUtility
from pathlib import Path

# Sets up the parser and generates argument values
def _generate_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
        Program tworzący oraz odczytujący pliki na podstawie danych wejściowych.

        Na wejściu powinny się pojawić:
        - Lista miesięcy
        - Lista zakresów dni tygodnia (tyle samo argumentów co w liście miesięcy)
        - Lista pór dnia (rano lub wieczór), domyślnie rano
        
        Przykład:
        [styczeń, luty], [pn-wt, pt], [r,w]

        Styczeń/poniedziałek/rano
        Styczeń/wtorek/wieczorem
        Luty/piątek/rano (bo domyślnie)
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-o', action='store_true',
                        help='Sprawia, że program czyta pliki podane na wejściu, '
                        "sumuje wartość 'Czas' dla wszystkich plików, "
                        "w których 'Model' ma wartość 'A'. W przypadku braku"
                        "istnienia jednego z plików zwraca błąd.")
    parser.add_argument('-t', action='store_true',
                        help='Sprawia, że program tworzy foldery '
                        'oraz pliki z danymi na podstawie wejścia.')
    parser.add_argument('-c', action='store_true',
                        help='Sprawia, że program pracuje z plikami CSV.')
    parser.add_argument('-j', action='store_true',
                        help='Sprawia, że program pracuje z plikami JSON.')

    args =  parser.parse_args()
    if args.t and args.o:
        raise ValueError('Błąd: flagi -t, -o nie mogą być jednocześnie zapalone')
    if args.c and args.j:
        raise ValueError('Błąd: flagi -c, -j nie mogą być jednocześnie zapalone')
    if not args.t and not args.o:
        raise ValueError('Błąd: brak flagi -o oraz -t')
    if not args.c and not args.j:
        raise ValueError('Błąd: brak flagi -c oraz -j')

    return args

def _parse_months(raw_months: list[str]) -> list[str]:
    months_list = [
        'styczeń',
        'luty',
        'marzec',
        'kwiecień',
        'maj',
        'czerwiec',
        'lipiec',
        'sierpień',
        'wrzesień',
        'październik',
        'listopad',
        'grudzień'
    ]
    if len(raw_months) != len(set(raw_months)):
        raise ValueError('Błąd: powtarzające się miesiące')
    months = []
    for month in raw_months:
        if month not in months_list:
            raise ValueError('Błędny miesiąc: ' + month)
        
        months.append(month.capitalize())

    return months

def _parse_days(raw_days: list[str]) -> list[str]:
    days_list = [
        'pn', 
        'wt', 
        'śr', 
        'czw', 
        'pt', 
        'sob', 
        'niedz'
    ]
    days_full_list = [
        'Poniedziałek',
        'Wtorek',
        'Środa',
        'Czwartek',
        'Piątek',
        'Sobota',
        'Niedziela'
    ]

    days = []
    for i in range(len(raw_days)):
        days_helper = raw_days[i].split('-')
        match len(days_helper):
            case 1:
                if days_helper[0] not in days_list:
                    raise ValueError('Błędny dzień tygodnia: ' + days_helper[0])
                    
                days.append([days_full_list[days_list.index(days_helper[0])]])
            case 2:
                if days_helper[0] not in days_list:
                    raise ValueError('Błędny dzień tygodnia: ' + days_helper[0])
                if days_helper[1] not in days_list:
                    raise ValueError('Błędny dzień tygodnia: ' + days_helper[1])
                
                begin = days_list.index(days_helper[0])
                end = days_list.index(days_helper[1])
                if begin > end:
                    raise ValueError('Błędna kolejność dni tygodnia ' + days_helper[0] + '-' + days_helper[1])
                
                days.append(days_full_list[begin:end + 1])
            case _:
                raise ValueError("Błędny zakres dni tygodnia")

    return days

def _parse_times(raw_times: list[str]) -> list[str]:
    times_list = ['r', 'w']

    times = []
    for time in raw_times:
        if time not in times_list:
            raise ValueError("Błędna pora dnia: " + time)
        if time == 'r':
            times.append('rano')
        if time == 'w':
            times.append('wieczorem')

    return times

def parse_input_and_run() -> None:
    """Parse user input and run the program on it.
    
    Raises:
        ValueError: If the input was incorrect.
        OSError: If directory reading/generation failed.
    """
    
    args = _generate_args()

    input_string = input()
    groups = re.findall(r'\[([^\]]*)\]', input_string)
    if len(groups) != 3:
        raise ValueError('Błędna liczba argumentów')

    raw_months = groups[0].replace(" ", "").split(',')
    months = _parse_months(raw_months)

    raw_days = groups[1].replace(" ", "").split(',')
    days = _parse_days(raw_days)
    
    if len(months) != len(days):
        raise ValueError("Błąd: liczba miesięcy jest różna od liczby dni tygodnia")
               
    raw_times = groups[2].replace(" ", "").split(',')
    times = _parse_times(raw_times)

    # Generate a list of directories from the parsed data
    directories = []
    times_index = 0
    for i in range(len(months)):
        for j in range(len(days[i])):
            if times_index >= len(times):
                directories.append(Path(months[i], days[i][j], "rano"))
                if args.t:
                    sciezka.generuj_sciezke(months[i], days[i][j])
            else:
                directories.append(Path(months[i], days[i][j], times[times_index]))
                if args.t:
                    sciezka.generuj_sciezke(months[i], days[i][j], times[times_index]) 
                times_index += 1

    if args.c:
        if args.t:
            for directory in directories:
                zapisCSV.dodajDaneCSV(directory)
        if args.o:
            print('Suma wartości z kolumny "Czas": ' + str(zapisCSV.zczytajCSV(directories)))
    if args.j:
        if args.t:
            for directory in directories:
                jsonUtility.stworz_badz_nadpisz_jsona(directory)
        if args.o:
            sum = 0
            for directory in directories:
                sum += jsonUtility.przetworz_istniejacy_plik(directory)
            print('Suma wartości z kolumny "Czas": ' + str(sum))

if __name__ == "__main__":
    try:
        parse_input_and_run()
    except Exception as e:
        print(e)