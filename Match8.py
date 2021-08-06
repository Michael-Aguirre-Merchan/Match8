import json
import pandas as pd
import requests
import pathlib

response = requests.get("https://mach-eight.uc.r.appspot.com/")

data = json.loads(response.text)
PLAYERS = data["values"]

dict = {}
pairs = []

for i in range(len(PLAYERS)):
    key = PLAYERS[i].get('h_in')
    value = PLAYERS[i].get('first_name') + ' ' + PLAYERS[i].get('last_name')
    dict.setdefault(key, [])
    dict[key].append(value)
    
def getPairs(value):

    keys = list(dict)
    for i in range(len(keys)):
        current = list(dict)[i]
        current_int = str(value - int(current))
        if current_int in keys:
            if current == current_int:
                for j in range(len(dict[current])):
                    for k in range(j+1, len(dict[current_int])):
                        pairs.append((dict[current][j], int(current), dict[current_int][k], int(current_int)))
            else:
                for j in range(len(dict[current])):
                    for k in range(len(dict[current_int])):
                        pairs.append((dict[current][j], int(current), dict[current_int][k], int(current_int)))
                keys.remove(current_int)
            keys.remove(current)

def xls():
    pair1 = []
    pair2 = []
    val1 = []
    val2 = []

    for i in range(len(pairs)):
        pair1.insert(0, pairs[i][0])
        val1.insert(0, pairs[i][1])
        pair2.insert(0, pairs[i][2])
        val2.insert(0, pairs[i][3])
        
        assert(pairs[i][1] + pairs[i][3] == int(value_int))

    df = pd.DataFrame({'Pair 1': pair1,
                        'Value 1': val1,
                        'Pair 2': pair2,
                        'Value 2': val2})

    path = str(pathlib.Path(__file__).parent.resolve()) + "\pairs.xlsx"

    print(path)
    
    df.to_excel(path, sheet_name= "Pairs for value " + str(value_int))

try:
    value_int = int(input("What number do you want to get your pairs from: \n"))
    getPairs(value_int)
except ValueError:
    print("That's not an number!")

if len(pairs) != 0:
    value = input("Do you want to export an xls file? (Y / N) \n")
    if value == "Y" or value == "y":
        
        try:
            xls()
            print("File created successfully")
        except:
            print("There has been an error creating the xlsx file. Please make sure you don't have the file open and try again")
    elif value == "N" or value == "n":
        print("Pairs for " + str(value_int))
        for i in range(len(pairs)):

            assert(pairs[i][1] + pairs[i][3] == int(value_int))

            print(pairs[i][0], pairs[i][2])
    else:
        print("Not a valid answer")

else:
    print("There aren't pairs that meet the requirements")