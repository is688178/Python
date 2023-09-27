import csv
import os

# escribir
with open("./archivo.csv", "w", newline='') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(["twit_id", "user_id", "text"])
    writer.writerow([1000, 1, "este es un twit"])
    writer.writerow([1001, 2, "otro twit!"])

# leer
with open("./archivo.csv", newline='') as archivo:
    reader = csv.reader(archivo)
    print("Como lista:")
    print(reader)  # Objeto iterable
    print(list(reader))  # Imprimir creando lista
    archivo.seek(0)  # Regresamos puntero
    print("Iterando:")
    for linea in reader:
        print(linea)

# actualizar csv
with open("./archivo.csv", newline='') as r, open("./archivo_temp.csv", "w", newline='') as w:
    reader = csv.reader(r)
    writer = csv.writer(w)  # Archivo temporal para modificaciones
    for linea in reader:
        if linea[0] == "1000":  # Todos los datos de un csv se convierten en cadenas
            writer.writerow([1000, 1, "texto modificado"])
        else:
            writer.writerow(linea)
# Ahora eliminamos el original y renombramos el temporal (es lo mas eficiente)
os.remove("./archivo.csv")
os.rename("./archivo_temp.csv", "./archivo.csv")
