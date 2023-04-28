import requests
#import pyfiglet
import random   
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup
from itertools import zip_longest
import pandas as pd
import time
#from tabulate import tabulate
import matplotlib.pyplot as plt

url = 'https://pokemondb.net/pokedex/all'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

#contenido de la pagina
contenido = soup.find(id='pokedex')
contenido = contenido.find_all('tr')
contenido = contenido[1:]

numero = []
nombre = []
tipos = []
estadisticas = []
hp = []
atk = []
deff = []
spatk = []
spdef = []
spd = []
total = []

for i in contenido:
    #ordenados por numero
    numero_pokemon = i.find('span', class_='infocard-cell-data').text
    numero.append(numero_pokemon)

    #ordenados por nombre
    nombre_pokemon = i.find('a', class_='ent-name').text
    nombre.append(nombre_pokemon)

    #ordenados por tipo
    tipos.append([t.text for t in i.find_all('a', class_='type-icon')])

    #ordenados por estadisticas
    stats = i.find_all('td', class_='cell-num')[2:]
    temp = []
    for s in stats:
        temp.append(int(s.text))
        if len(temp) == 6:
            estadisticas.append(temp)
            temp = []


    #ordenados por total
    total_pokemon = i.find('td', class_='cell-total').text
    total.append(total_pokemon)

    #ordenados por estadisticas (hp, atk, def, spatk, spdef, spd)
    hp.append(estadisticas[-1][0])
    atk.append(estadisticas[-1][1])
    deff.append(estadisticas[-1][2])
    spatk.append(estadisticas[-1][3])
    spdef.append(estadisticas[-1][4])
    spd.append(estadisticas[-1][5])
    
data = {
    'numero': numero,
    'nombre': nombre,
    'tipos': tipos,
    'hp': hp,
    'atk': atk,
    'def': deff,
    'spatk': spatk,
    'spdef': spdef,
    'spd': spd,
    'total': total
}

df = pd.DataFrame(data)

#hp, atk, def, spatk, spdef, spd

#banner = pyfiglet.figlet_format("Pokemon")

infinito = False
while infinito == False:
    print(Fore.RED + """    ██████╗  ██████╗ ██╗  ██╗███████╗███╗   ███╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗ ████║██╔═══██╗████╗  ██║
    ██████╔╝██║   ██║█████╔╝ █████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
    ██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
    ██║     ╚██████╔╝██║  ██╗███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                """ + Style.RESET_ALL)
    print("\n¡Bienvenido al mundo de los Pokémon!\n\nAquí podrás encontrar cuatro divertidas aplicaciones para sacar el máximo provecho a tu pasión por los Pokémon. Por favor, seleccione una opción:\n\n" + Fore.GREEN + "1. Pokédex interactiva:" + Style.RESET_ALL + " Explora la lista completa de Pokémon y aprende más sobre cada uno de ellos. Podrás buscar por nombre o por tipo, y ver información detallada como sus habilidades, estadísticas, movimientos y mucho más.\n\n" + Fore.GREEN + "2. Simulador de combate: " + Style.RESET_ALL + "¿Quieres poner a prueba tus habilidades como entrenador Pokémon? Usa nuestro simulador de combate para crear un equipo de Pokémon y luchar contra otros entrenadores. Podrás personalizar tus Pokémon con habilidades, movimientos y objetos, y experimentar con diferentes estrategias para ganar.\n\n" + Fore.GREEN + "3. Clasificador de Pokémon:" + Style.RESET_ALL + "¿No sabes cuales son los Pokémons mas fuertes o mas debiles? ¿No estás seguro de cuales tienen determinadas cualidades mas altas? Nuestro clasificador de Pokémon te permitirá buscar cualquier Pokémon por nombre y te mostrará toda su información detallada.\n\n" + Fore.GREEN + "4. Descargar mi csv actualizado:" + Style.RESET_ALL + " Si desea descargar la base de datos de pokemon actualizada cada vez que se ejecuta el programa.\n\n" + "Por favor, seleccione una opción escribiendo su número correspondiente (1, 2, 3 o 4) 'exit' para salir y presione ENTER. ¡Que te diviertas!\n")
    opcion = input("Opción: ")
    if opcion == "1":
        # función para la Pokédex interactiva
        def buscar_pokemon_nombre(df):
            pokenombre = input("Ingrese el nombre del Pokémon que desea buscar: ")
            pokemon = df.loc[df['nombre'].str.lower() == pokenombre.lower()]
            if len(pokemon) > 0:
                print(pokemon.to_string(index=False))
            else:
                print("El Pokémon no fue encontrado.")

        buscar_pokemon_nombre(df)

        time.sleep(2)

    elif opcion == "2":
        
        def seleccionar_pokemon(df):
            pokemon_seleccionados = []
            while len(pokemon_seleccionados) < 3:
                pokenombre = input("Ingrese el nombre del Pokémon que desea seleccionar: ")
                pokemon = df.loc[df['nombre'].str.lower() == pokenombre.lower()]
                if len(pokemon) > 0:
                    pokemon_seleccionados.append(pokemon.iloc[0])
                else:
                    print("El Pokémon no fue encontrado.")
            return pokemon_seleccionados

        def generar_pokemon_aleatorios(df):
            indices_aleatorios = random.sample(range(len(df)), 3)
            return [df.iloc[i] for i in indices_aleatorios]

        def simulador_combate(df):
            print("¡Bienvenido al simulador de combate!")
            print("Seleccione sus tres Pokémon:")
            pokemon_seleccionados = seleccionar_pokemon(df)
            print("\nSus Pokémon seleccionados son:")
            for pokemon in pokemon_seleccionados:
                print(pokemon['nombre'])
            print("\nAhora generaremos tres Pokémon aleatorios para que se enfrenten:")
            pokemon_aleatorios = generar_pokemon_aleatorios(df)
            for pokemon in pokemon_aleatorios:
                print(pokemon['nombre'])
            print("\n¡Que comience el combate!")
            time.sleep(2)
            for i in range(3):
                print("\nRound", i+1, "!")
                time.sleep(1)
                print(pokemon_seleccionados[i]['nombre'], "vs.", pokemon_aleatorios[i]['nombre'])
                time.sleep(1)
                if pokemon_seleccionados[i]['total'] > pokemon_aleatorios[i]['total']:
                    print(pokemon_seleccionados[i]['nombre'], "gana!")
                elif pokemon_seleccionados[i]['total'] < pokemon_aleatorios[i]['total']:
                    print(pokemon_aleatorios[i]['nombre'], "gana!")
                else:
                    print("¡Empate!")
                time.sleep(2)
            print("\n¡El combate ha terminado!")

        generar_pokemon_aleatorios(df)
        simulador_combate(df)
        time.sleep(2)

    elif opcion == "3":

        def obtener_id_pokemon(nombre_pokemon):
            url = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1000"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for pokemon in data['results']:
                    if pokemon['name'] == nombre_pokemon:
                        return pokemon['url'].split('/')[-2]
            return None
        
        def obtener_info_pokemon(nombre_pokemon):
            id_pokemon = obtener_id_pokemon(nombre_pokemon)
            url = f"https://pokeapi.co/api/v2/pokemon/{id_pokemon}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                nombre = data['name']
                altura = data['height']
                peso = data['weight']
                tipos = [tipo['type']['name'] for tipo in data['types']]
                stats = {}
                for stat in data['stats']:
                    stat_nombre = stat['stat']['name']
                    stat_valor = stat['base_stat']
                    stats[stat_nombre] = stat_valor
                return {
                    'nombre': nombre,
                    'altura': altura,
                    'peso': peso,
                    'tipos': tipos,
                    'stats': stats
                }
            else:
                return None
            

        def graficar_stats_pokemon(nombre_pokemon):
            info_pokemon = obtener_info_pokemon(nombre_pokemon)
            if info_pokemon:
                stats = info_pokemon['stats']
                plt.bar(stats.keys(), stats.values())
                plt.title(f"Estadísticas de base de {nombre_pokemon}")
                plt.xlabel("Estadística")
                plt.ylabel("Valor")
                plt.show()
            else:
                print(f"No se encontró ningún Pokémon llamado {nombre_pokemon}.")

        nombre_pokemon = input("Ingrese el nombre del Pokémon que desea buscar: ")
        graficar_stats_pokemon(nombre_pokemon)
    
        time.sleep(2)

    elif opcion == "4":
        def guardar_pokedex(df):
            df.to_csv("pokedex.csv", index=False)
            print("Pokedex guardada como pokedex.csv")
        guardar_pokedex(df)

        time.sleep(2)

    elif opcion == "exit":
        print("¡Hasta luego!")
        infinito = True
        break

    else:
        print("Opción no válida. Por favor, seleccione una opción escribiendo su número correspondiente (1, 2, 3 o 4) y presione ENTER.")
    
    time.sleep(2)