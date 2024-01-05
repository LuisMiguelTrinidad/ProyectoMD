import json

def lectura(ruta_archivo):
    try:
        # Leer el contenido del archivo JSON
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)

        # Acceder a todas las entradas de "galactic_object"
        objetos_galacticos = datos_json.get("galactic_object", {})

        if objetos_galacticos:
            # Iterar a través de todas las entradas de "galactic_object"
            for id_objeto, objeto_galactico in objetos_galacticos.items():
                # Acceder e imprimir o utilizar propiedades específicas de cada "galactic_object"
                coordenada = objeto_galactico.get("coordinate", {})
                print(f"Objeto Galáctico {id_objeto} - Coordenadas:", "x=", coordenada.get("x"), "y=", coordenada.get("y"))

                clave_nombre = objeto_galactico.get("name", {}).get("key")
                print(f"Objeto Galáctico {id_objeto} - Nombre:", clave_nombre)

                hyperlane = objeto_galactico.get("hyperlane", [])
                print(f"Objeto Galáctico {id_objeto} - Hiperlínea:", hyperlane)
                print("\n")

        else:
            print("La clave 'galactic_object' no existe en los datos JSON.")
    except Exception as e:
        print(f"Error al leer o analizar el archivo JSON: {e}")

lectura("output.json")