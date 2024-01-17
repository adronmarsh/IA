import pdfkit

def convertir_a_pdf(archivo_entrada, archivo_salida, wkhtmltopdf_path):
    with open(archivo_entrada, "rb") as f:
        pdfkit.from_file(f, archivo_salida, wkhtmltopdf=wkhtmltopdf_path)

# Explicitly specify the path to wkhtmltopdf
wkhtmltopdf_path = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"



# Definir la función principal
def main():
    # Solicitar al usuario el nombre del archivo de entrada
    archivo_entrada = "presentacion.pptx"

    # Solicitar al usuario el nombre del archivo de salida
    archivo_salida = "salida.pdf"

# Convert the file
    convertir_a_pdf(archivo_entrada, archivo_salida, wkhtmltopdf_path)


# Ejecutar la función principal
if __name__ == "__main__":
    main()
