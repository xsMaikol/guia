class Estudiante:
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        self.notas = notas if notas is not None else {}
        self.materias = set(materias) if materias is not None else set()

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            "materias": list(self.materias)
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            id_estudiante=datos.get("id"),
            nombre=datos.get("nombre"),
            apellido=datos.get("apellido"),
            email=datos.get("email"),
            carnet=datos.get("carnet"),
            notas=datos.get("notas", {}),
            materias=set(datos.get("materias", []))
        )