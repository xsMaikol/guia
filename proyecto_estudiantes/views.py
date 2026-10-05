from models import Estudiante
from shared.json_manager import GestorJSON
from shared.herramientas import es_entero_valido, es_flotante_valido


class SistemaEstudiantes:
    def __init__(self):
        self.gestor = GestorJSON("data/estudiantes.json")
        self.estudiantes = self.cargar_estudiantes()
        # Usamos un set para validar carnets duplicados rápidamente en O(1)
        self._carnets_registrados = {est.carnet for est in self.estudiantes if est.carnet}

    def cargar_estudiantes(self):
        datos = self.gestor.leer()
        return [Estudiante.desde_diccionario(d) for d in datos]

    def guardar_cambios(self):
        datos = [est.a_diccionario() for est in self.estudiantes]
        return self.gestor.guardar(datos)

    def _generar_nuevo_id(self):
        """Genera un nuevo ID seguro evitando errores si la lista está vacía."""
        if not self.estudiantes:
            return 1
        ids = [est.id for est in self.estudiantes if est.id is not None]
        if not ids:
            return 1
        return max(ids) + 1

    def crear_estudiante(self, nombre, apellido, email, carnet):
        if carnet in self._carnets_registrados:
            return False, "Ya existe un estudiante registrado con ese carnet."
        
        nuevo_id = self._generar_nuevo_id()
        nuevo = Estudiante(id_estudiante=nuevo_id, nombre=nombre, apellido=apellido, email=email, carnet=carnet)
        
        self.estudiantes.append(nuevo)
        self._carnets_registrados.add(carnet)
        
        if self.guardar_cambios():
            return True, "Estudiante creado exitosamente."
        return False, "Error al guardar en el archivo JSON."

    def obtener_todos(self):
        return self.estudiantes

    def buscar_estudiantes(self, criterio):
        """Busca por ID, carnet o email."""
        criterio = criterio.strip().lower()
        resultados = []
        for est in self.estudiantes:
            if (str(est.id) == criterio or 
                (est.carnet and est.carnet.lower() == criterio) or 
                (est.email and est.email.lower() == criterio)):
                resultados.append(est)
        return resultados

    def actualizar_estudiante(self, id_estudiante, nombre=None, apellido=None, email=None):
        for est in self.estudiantes:
            if est.id == id_estudiante:
                if nombre: est.nombre = nombre
                if apellido: est.apellido = apellido
                if email: est.email = email
                
                if self.guardar_cambios():
                    return True, "Estudiante actualizado correctamente."
                return False, "Error al guardar los cambios."
        return False, "ID de estudiante inexistente."

    def eliminar_estudiante(self, id_estudiante):
        for est in self.estudiantes:
            if est.id == id_estudiante:
                if est.carnet in self._carnets_registrados:
                    self._carnets_registrados.remove(est.carnet)
                self.estudiantes.remove(est)
                if self.guardar_cambios():
                    return True, "Estudiante eliminado correctamente."
                return False, "Error al guardar los cambios."
        return False, "ID de estudiante inexistente."

    def agregar_nota(self, id_estudiante, materia, nota):
        if not (0 <= nota <= 20):
            return False, "La nota debe ser un número entre 0 y 20."
        
        for est in self.estudiantes:
            if est.id == id_estudiante:
                materia = materia.strip().capitalize()
                if materia not in est.notas:
                    est.notas[materia] = []
                est.notas[materia].append(nota)
                est.materias.add(materia) # Agregamos al set de materias del estudiante
                
                if self.guardar_cambios():
                    return True, "Nota agregada exitosamente."
                return False, "Error al guardar los cambios."
        return False, "ID de estudiante inexistente."

    def calcular_promedio(self, id_estudiante):
        for est in self.estudiantes:
            if est.id == id_estudiante:
                todas_las_notas = [nota for lista_notas in est.notas.values() for nota in lista_notas]
                if not todas_las_notas:
                    return 0.0, "El estudiante no tiene notas registradas."
                promedio = sum(todas_las_notas) / len(todas_las_notas)
                return promedio, "Promedio calculado con éxito."
        return None, "ID de estudiante inexistente."

    def materias_ofertadas(self):
        """Devuelve un set con todas las materias inscritas por todos los estudiantes, sin repetir."""
        materias_totales = set()
        for est in self.estudiantes:
            materias_totales.update(est.materias)
        return materias_totales

    def estudiantes_en_comun(self, id_a, id_b):
        """Usa la intersección de conjuntos para mostrar las materias que dos estudiantes comparten."""
        est_a = next((e for e in self.estudiantes if e.id == id_a), None)
        est_b = next((e for e in self.estudiantes if e.id == id_b), None)
        
        if not est_a or not est_b:
            return None, "Uno o ambos IDs de estudiantes no existen."
        
        comun = est_a.materias.intersection(est_b.materias)
        return comun, "Intersección calculada con éxito."