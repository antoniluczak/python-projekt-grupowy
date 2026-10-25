import argparse
import re
import sciezka
import zapisCSV

def parse_input_and_run() -> None:
    """Parse user input and run the program on it.
    
    Raises:
        ValueError: If the input was incorrect.
        OSError: If directory reading/generation failed.
    """
    # Used to parse intervals and validate input
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
    times_list = ['r', 'w']

    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('-o', action='store_true')
    parser.add_argument('-t', action='store_true')
    parser.add_argument('-c', action='store_true')
    parser.add_argument('-j', action='store_true')

    args = parser.parse_args()
    if args.t and args.o:
        raise ValueError('Błąd: flagi -t, -o nie mogą być jednocześnie zapalone')
    if args.c and args.j:
        raise ValueError('Błąd: flagi -c, -j nie mogą być jednocześnie zapalone')

    input_string = input()
    groups = re.findall(r'\[([^\]]*)\]', input_string)
    if len(groups) != 3:
        raise ValueError('Błędna liczba argumentów')

    # Parse months
    months_before_upper = groups[0].replace(" ", "").split(',')
    if len(months_before_upper) != len(set(months_before_upper)):
        raise ValueError('Błąd: powtarzające się miesiące')
    months = []
    for month in months_before_upper:
        if month not in months_list:
            raise ValueError('Błędny miesiąc: ' + month)
        
        months.append(month.upper())

    # Parse days
    days_before_split = groups[1].replace(" ", "").split(',')
    days = []
    for i in range(len(days_before_split)):
        days_helper = days_before_split[i].split('-')
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

    if len(months) != len(days):
        raise ValueError("Błąd: liczba miesięcy jest różna od liczby dni tygodnia")

    # Parse time                
    time_short = groups[2].replace(" ", "").split(',')
    times = []
    for time in time_short:
        if time not in times_list:
            raise ValueError("Błędna pora dnia: " + time)
        if time == 'r':
            times.append('rano')
        if time == 'w':
            times.append('wieczorem')

    # Generate a list of directories from the parsed data
    directories = []
    times_index = 0
    for i in range(len(months)):
        for j in range(len(days[i])):
            if times_index >= len(times):
                directories.append(sciezka.generuj_sciezke(months[i], days[i][j]))
            else:
                directories.append(sciezka.generuj_sciezke(months[i], days[i][j], times[times_index]))
                times_index += 1

    if args.c:
        if args.t:
            for directory in directories:
                zapisCSV.dodajDaneCSV(directory)
        else:
            print('Suma wartości z kolumny "Czas": ' + str(zapisCSV.zczytajCSV(directories)))
        
    # TODO: Handle JSON
    # No implementation in zapisJSON.py

if __name__ == "__main__":
    try:
        parse_input_and_run()
    except ValueError as e:
        print(e)
    except OSError as e:
        print(e)