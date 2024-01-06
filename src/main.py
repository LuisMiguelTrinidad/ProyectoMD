import subprocess

def ejecutar_script_javascript(ruta_archivo_entrada, ruta_archivo_salida):
    try:
        # Especifica la ruta a tu archivo JavaScript
        ruta_archivo_javascript = "./src/Parser.js"

        # Ejecuta el código JavaScript usando Node.js, pasando las rutas de archivo de entrada y salida
        resultado = subprocess.run(["node", ruta_archivo_javascript, ruta_archivo_entrada, ruta_archivo_salida], check=True, capture_output=True, text=True)
        
        # Imprime la salida estándar
        print("Código JavaScript ejecutado exitosamente.")
        print("Salida generada en: ./output/output0.json")
        
    except subprocess.CalledProcessError as e:
        # Imprime el error estándar en caso de un error
        print("Error al ejecutar el código JavaScript:", e)
        print("Salida de error:")
        print(e.stderr)

# Especifica la ruta a tu archivo de entrada
ruta_archivo_entrada = "./data/gamestate0"

# Especifica la ruta para el archivo JSON de salida
ruta_archivo_salida = "./output/output0.json"

# Llama a la función para ejecutar el código JavaScript
ejecutar_script_javascript(ruta_archivo_entrada, ruta_archivo_salida)
