import os
import random
import json
import math

# does not handle exceptions related to the system failing to open the file
# writes pure string data into file in the given folder
def _overwrite_or_create_in_existing_folder(file, folder, data):
  path = os.path.join(folder, file)
  if not os.path.exists(folder):
    raise FileNotFoundError('Folder does not exist')
  
  with open(path, 'w') as f:
    f.write(data)

# does not handle exceptions related to the system failing to read the file
# returns json data from file as dictionary, not yet processed
def _read_from_existing_file(file):
  if not os.path.isfile(file):
    raise FileNotFoundError('File does not exist')
  
  with open(file, 'r') as f:
    data = json.load(f)
    return data



# does not handle exceptions related to the system failing to read the file
# does not handle exception of invalid json, try except is a must
# returns time if model is equal to A, 0 otherwise
def przetworz_istniejacy_plik(folder):
  file = os.path.join(folder, 'dane.json')
  dataArr = _read_from_existing_file(file)
  if len(dataArr) != 1:
    raise ValueError(f'W jsonie jest {len(dataArr)} rekordow, zamiast oczekiwanych dwoch')
  suma = 0

  for data in dataArr:
    if data.get('Model') == None or data.get('Czas') == None:
      raise ValueError('W jsonie nie ma oczekiwanego \'Model\' ani \'Czas\'')  
    if data.get('Model') == 'A':
      if (len(data.get('Czas')) < 2):
        raise ValueError('Czas jest w zlym formacie')
      czasStr = data.get('Czas')[:-1]
      if not czasStr.isdecimal():
        raise ValueError('Czas jest w zlym formacie')
      suma += int(czasStr)
  return suma



def stworz_badz_nadpisz_jsona(folder):
  opcje = ['A', 'B', 'C']
  rekord = {
    'Model': opcje[random.randint(0, 2)],
    'Wynik': random.randint(0, 1000),
    'Czas': str(random.randint(0, 1000))+'s'
  }
  data = [rekord]
  dataStr = json.dumps(data, indent=10) # 10 bo to moja biblioteka
  _overwrite_or_create_in_existing_folder('dane.json', folder, dataStr)

# dla dumnego (nie za bardzo) developera tej okropnej biblioteki
def _test_run():
  tenFolder = os.getcwd()
  stworz_badz_nadpisz_jsona(tenFolder)
  print(przetworz_istniejacy_plik(os.path.join(tenFolder, 'dane.json')))

if __name__=='__main__':
  _test_run()
  