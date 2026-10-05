import os
import json


class GestorJSON:
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def _asegurar_directorio(self):
        directorio = os.path.dirname(self.ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

    def leer(self):
        if not os.path.exists(self.ruta_archivo):
            return []
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            return []

    def guardar(self, datos):
        try:
            self._asegurar_directorio()
            with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False