//Función parseadora
const { Jomini } = require("jomini");
const fs = require("fs");

async function Parsea(rutaArchivoEntrada, rutaArchivoSalida) {
  try {
    // Leer el contenido del archivo de entrada
    const datos = await fs.promises.readFile(rutaArchivoEntrada, "utf-8");

    // Inicializar el analizador Jomini
    const analizador = await Jomini.initialize();

    // Analizar el contenido del archivo
    const resultado = analizador.parseText(datos);

    // Escribir los datos analizados en el archivo JSON de salida
    await fs.promises.writeFile(rutaArchivoSalida, JSON.stringify(resultado, null, 2), "utf-8");

    console.log("Análisis exitoso, resultado generado en:", rutaArchivoSalida);
  } catch (error) {
    console.error("Error al leer, analizar o escribir en el archivo:", error);
  }
}

// Especificar la ruta de tu archivo de entrada
const rutaArchivoEntrada = "./data/gamestate0";

// Especificar la ruta para el archivo JSON de salida
const rutaArchivoSalida = "./output/output0.json";

// Llamar a la función con las rutas de los archivos
Parsea(rutaArchivoEntrada, rutaArchivoSalida);
