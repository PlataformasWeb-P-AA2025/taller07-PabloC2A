from sqlalchemy.orm import sessionmaker
from genera_tablas import Club, Jugador, engine

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Ruta a los archivos
archivo_clubs = "./data/datos_clubs.txt"
archivo_jugadores = "./data/datos_jugadores.txt"

# 1. Cargar datos de Club
with open(archivo_clubs, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        nombre, deporte, fundacion = linea.strip().split(";")
        club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
        session.add(club)

session.commit()

# 2. Cargar los datos de Jugador y hacer consulta de club
with open(archivo_jugadores, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        nombre_club, posicion, dorsal, nombre_jugador = linea.strip().split(";")
        dorsal = int(dorsal)

        try:
            # Buscar el club por su nombre
            club = session.query(Club).filter_by(nombre=nombre_club).one()
            # Crear el jugador asociado
            jugador = Jugador(
                nombre=nombre_jugador,
                dorsal=dorsal,
                posicion=posicion,
                club=club.id
            )
            session.add(jugador)
        except Exception as e:
            print(f"No se pudo asociar el jugador {nombre_jugador} al club {nombre_club}: {e}")

session.commit()
session.close()

print("Datos guardados exitosamente")
