import json

def lectura(ruta_archivo):
    try:
        # Leer el contenido del archivo JSON
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)

        # Acceder a todas las entradas de "galactic_object"
        objetos_galacticos = datos_json.get("galactic_object", {})

        if objetos_galacticos:
            map = {}

            # Iterar a través de todas las entradas de "galactic_object"
            for id_objeto, objeto_galactico in objetos_galacticos.items():
                # Acceder e imprimir o utilizar propiedades específicas de cada "galactic_object"
                coordenada = objeto_galactico["coordinate"]
                clave_nombre = objeto_galactico["name"]["key"]
                hyperlane = objeto_galactico.get("hyperlane",[])

                # Guardamos la información necesaria en un diccionario
                map[id_objeto]=[coordenada["x"],  coordenada["y"], clave_nombre, hyperlane]
            
            for i in map:
                print(i, ":", map[i])
        else:
            print("La clave 'galactic_object' no existe en los datos JSON.")
    except Exception as e:
        print(f"Error al leer o analizar el archivo JSON: {e}")
    
lectura("./output/output0.json")