import subprocess
import Loader

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
        print("Error al ejecutar el código JavaScript:")
        print(e.stderr)

def main():
    ejecutar_script_javascript("./data/gamestate0", "./output/output0.json")
    diccionario_completo=Loader.lectura("./output/output0.json")
    Loader.test_lectura("./output/output0.json")

if __name__ == "__main__":
    main()
