import os
os.system("pip install requests")
os.system("pip install tabulate")
import re
import requests
import json
from tabulate import tabulate

url = "https://pokeapi.co/api/v2/"
infoPokeApi = requests.get(url).json()

with open('infoURLPokemon.json', 'w') as file:
    json.dump(infoPokeApi, file, indent=4)

with open('infoURLPokemon.json') as file:
    urlListPokemon = json.load(file)

def listOptions(urlListPokemon: dict, nameList: str)-> list:
    data = requests.get(urlListPokemon[nameList]).json()
    urlTotal = "offset=0&limit=" + str(data["count"])
    if data["next"] != None:
        jsonFile = requests.get(data["next"].replace("offset=20&limit=20", urlTotal)).json()["results"]
    else:
        jsonFile = data["results"]

    listResult = [result["name"] for result in jsonFile]

    return listResult

def abilitiesAndSprites(nameIDPokemons, option: str)->list:
    print()
    abilitiesPokemons = []
    imagesPokemons = []
    namePokemons = []
    for pokemon in nameIDPokemons:
        namePokemons.append(pokemon[0])
        url = "https://pokeapi.co/api/v2/pokemon/"
        dataPokemon = requests.get(url + pokemon[1]).json()
        abilities = [ability["ability"]["name"] for ability in dataPokemon["abilities"]]
        abilitiesPokemons.append(abilities)

        if dataPokemon["sprites"]["front_default"] == None:
            sprite = "No se encontró imagen frontal"
        else:
            sprite = dataPokemon["sprites"]["front_default"]
        imagesPokemons.append(sprite)

    numberPokemons = list(range(1,len(imagesPokemons)+1))

    if option != "ability":
        if namePokemons == []:
            print("No encontramos pokemons con la inicial que ingresaste\n")
        else:
            tuplePokemons = zip(numberPokemons,namePokemons, abilitiesPokemons, imagesPokemons)
            fieldNames = ["N°","Pokemon", "Habilidades", "URL Imagen"]
            print(tabulate(tuplePokemons, headers= fieldNames))
            print()
    else:
        tuplePokemons = zip(numberPokemons,namePokemons, imagesPokemons)
        fieldNames = ["N°","Pokemon", "URL Imagen"]
        print(tabulate(tuplePokemons, headers= fieldNames))
        print()

def chooseOption(question: str, answerone: str, answertwo: str):
    while True:
        showQuestion = input(question).upper()
        if showQuestion == answerone:
            return showQuestion
        elif showQuestion == answertwo:
            return showQuestion
        else:
            continue

def optionList(url: list, optionSelect: str, keyword: str):
    '''url: url con los datos de la opción seleccionada . optionSelect: opción a buscar. keyword: texto a preguntar si se desea repetir'''

    options = listOptions(url, optionSelect)

    while True:
        availableOptions = []
        print("Elige una opción:\n")
        for index, option in enumerate(options, 1):
            print(f"    {index}. {option.capitalize()}")
            availableOptions.append(index)

        print()

        while True:
            selectOption = input("Ingresa tu respuesta: ")
            if selectOption.isnumeric() and int(selectOption) in availableOptions:
                break
        
        if optionSelect == "type":
            pokemonOption = requests.get(url[optionSelect] + options[int(selectOption)-1]).json()["pokemon"]
            nameIDOption = [[pokemon["pokemon"]["name"].capitalize(), pokemon["pokemon"]["url"].split("/")[-2]] for pokemon in pokemonOption]

        else:
            pokemonOption =  requests.get(url[optionSelect] + options[int(selectOption) - 1]).json()["pokemon_species"]    
            nameIDOption = [[pokemon["name"].capitalize(), pokemon["url"].split("/")[-2]] for pokemon in pokemonOption]

        print(f"\nEcontramos {len(pokemonOption)} pokemons\n")

        showPokemons = chooseOption("¿Mostrar todos o por letra inicial? T/L: ", "T", "L")
        if showPokemons == "T":
            abilitiesAndSprites(nameIDOption, optionSelect)
            repeat = chooseOption(f"¿Seleccionar {keyword}? S/N: ", "S", "N")
            if repeat == "N":
                break
        elif showPokemons == "L":
            print()
            while True:
                letterShow = input("Ingresa una letra: ").capitalize()
                if letterShow.isalpha():
                    patronPokemon = re.compile('^' + letterShow)
                    selectedPokemons = [[pokemon[0], pokemon[1]] for pokemon in nameIDOption if patronPokemon.match(pokemon[0])]
                    abilitiesAndSprites(selectedPokemons, optionSelect)
                    repeat = chooseOption("¿Buscar con otra letra? S/N: ", "S", "N")
                    if repeat != "S":
                        break
                    print()
    
            print()
            anotherOption = chooseOption(f"¿Seleccionar {keyword}? S/N: ", "S", "N")
            if anotherOption != "S":
                break
        
        print()

def abilitites(url: list, optionSelect: str, keyword: str):

    options = listOptions(url, optionSelect)
    options.sort()

    while True:
        while True:
            letters = input("Ingresa el nombre de la habilidad (o las primeras letras): ").lower()
            if letters.isalpha():
                patron = re.compile('^' + letters)
                selectedAbilities = [ability.capitalize() for ability in options if patron.match(ability)]
                if selectedAbilities == []:
                    print("Vuelve a intentar con otras letras")
                    continue
                break
        print()
        availableOptions = []
        while True:
            print("Elige una opción:\n")
            for index, option in enumerate(selectedAbilities, 1):
                print(f"    {index}. {option.capitalize()}")
                availableOptions.append(index)

            print()

            while True:
                selectOption = input("Ingresa tu respuesta: ")
                if selectOption.isnumeric() and int(selectOption) in availableOptions:
                    break

            pokemonOption = requests.get(url[optionSelect] + options[int(selectOption)-1]).json()["pokemon"]
            nameIDOption = [[pokemon["pokemon"]["name"].capitalize(), pokemon["pokemon"]["url"].split("/")[-2]] for pokemon in pokemonOption]
            print(f"\nBuscando pokemons con la habilidad: {selectedAbilities[int(selectOption) - 1]}")

            abilitiesAndSprites(nameIDOption, optionSelect)

            repeat = chooseOption("¿Seleccionar otra opción? S/N: ", "S", "N")
            if repeat == "S":
                print()
                continue
            else:
                break
        print()
        anotherOption = chooseOption(f"¿Buscar {keyword}? S/N: ", "S", "N")
        if anotherOption != "S":
            break
        print()

    print()

options = ['optionList(urlListPokemon, "generation", "otra generación")', 'optionList(urlListPokemon, "pokemon-shape", "otra forma")', 'abilitites(urlListPokemon, "ability", "otra habilidad")', 'optionList(urlListPokemon, "pokemon-habitat", "otro habitat")', 'optionList(urlListPokemon, "type", "otro tipo")']

def showOptions():
    print("\t\t\tPOKEAPI\n")
    print("Elije una de las siguientes opciones:\n")
    print('''    Opción 1: Listar pokemons por generación.
    Opción 2: Listar pokemons por forma.
    Opción 3: Listar pokemons por habilidad.
    Opción 4: Listar pokemons por habitat.
    Opción 5: Listar pokemons por tipo.
    ''')

numbersOptions = [1, 2, 3, 4, 5]

print()

while True:
    os.system("cls")
    showOptions()
    while True:
        selectOption = input("Ingresa una opción: ")
        if selectOption.isnumeric() and int(selectOption) in numbersOptions:
            selectOption = int(selectOption)
            break
    print()
    eval(options[selectOption-1])
    print()
    anotherOption = input("¿Seleccionar otra lista? S/N: ").upper()
    if anotherOption == "S":
        continue
    elif anotherOption == "N":
        break