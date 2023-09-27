import json
from pathlib import Path

# escribir json
productos = [
    {"id": 1, "name": "Xbox"},
    {"id": 1, "name": "PlayStation"},
    {"id": 1, "name": "Nintendo"},
]

data = json.dumps(productos)
print(data)  # Es como una lista de diccionarios

Path("./productos.json").write_text(data)

# leer json
data = Path("./productos.json").read_text(encoding="UTF-8")
productos_json = json.loads(data)
print(productos_json)

# modificar json
productos_json[0]["name"] = "PC"
Path("./productos.json").write_text(json.dumps(productos_json))

# J ava
# S cript
# O bject
# N otation
