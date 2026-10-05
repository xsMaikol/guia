from views import SistemaEstudiantes
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar,
    es_entero_valido,
    es_flotante_valido
)


def main():
    sistema = SistemaEstudiantes()

    while True:
        imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
        print("1. Registrar nuevo estudiante")
        print("2. Listar todos los estudiantes")
        print("3. Buscar estudiante (ID, carnet o email)")
        print("4. Actualizar estudiante")
        print("5. Eliminar estudiante")
        print("6. Agregar nota")
        print("7. Ver promedio de estudiante")
        print("8. Ver materias ofertadas (global)")
        print("9. Ver materias en común entre dos estudiantes")
        print("10. Salir")
        print()

        opcion = input("Seleccione una opción (1-10): ").strip()

        if opcion == "1":
            imprimir_titulo("REGISTRAR ESTUDIANTE")
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            carnet = input("Carnet: ").strip()

            exito, mensaje = sistema.crear_estudiante(nombre, apellido, email, carnet)
            if exito:
                imprimir_exito(mensaje)
            else:
                imprimir_error(mensaje)
            input("\nPresione Enter para continuar...")

        elif opcion == "2":
            imprimir_titulo("LISTA DE ESTUDIANTES")
            estudiantes = sistema.obtener_todos()
            if not estudiantes:
                imprimir_info("No hay estudiantes registrados.")
            else:
                for est in estudiantes:
                    print(f"ID: {est.id} | Carnet: {est.carnet} | Nombre: {est.nombre} {est.apellido} | Email: {est.email}")
                    print(f"   Materias: {list(est.materias)} | Notas: {est.notas}")
                    print("-" * 60)
            input("\nPresione Enter para continuar...")

        elif opcion == "3":
            imprimir_titulo("BUSCAR ESTUDIANTE")
            criterio = input("Ingrese ID, carnet o email a buscar: ")
            resultados = sistema.buscar_estudiantes(criterio)
            if resultados:
                imprimir_exito(f"Se encontraron {len(resultados)} coincidencia(s):")
                for est in resultados:
                    print(f"ID: {est.id} | Carnet: {est.carnet} | {est.nombre} {est.apellido} | {est.email}")
            else:
                imprimir_error("No se encontraron registros con ese criterio.")
            input("\nPresione Enter para continuar...")

        elif opcion == "4":
            imprimir_titulo("ACTUALIZAR ESTUDIANTE")
            id_str = input("Ingrese el ID del estudiante a actualizar: ").strip()
            if not es_entero_valido(id_str):
                imprimir_error("ID inválido.")
            else:
                id_est = int(id_str)
                nombre = input("Nuevo nombre (deje en blanco para no cambiar): ").strip()
                apellido = input("Nuevo apellido (deje en blanco para no cambiar): ").strip()
                email = input("Nuevo email (deje en blanco para no cambiar): ").strip()
                
                exito, mensaje = sistema.actualizar_estudiante(id_est, nombre or None, apellido or None, email or None)
                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)
            input("\nPresione Enter para continuar...")

        elif opcion == "5":
            imprimir_titulo("ELIMINAR ESTUDIANTE")
            id_str = input("Ingrese el ID del estudiante a eliminar: ").strip()
            if not es_entero_valido(id_str):
                imprimir_error("ID inválido.")
            else:
                id_est = int(id_str)
                if confirmar("¿Está seguro de eliminar este estudiante?"):
                    exito, mensaje = sistema.eliminar_estudiante(id_est)
                    if exito:
                        imprimir_exito(mensaje)
                    else:
                        imprimir_error(mensaje)
                else:
                    imprimir_info("Operación cancelada.")
            input("\nPresione Enter para continuar...")

        elif opcion == "6":
            imprimir_titulo("AGREGAR NOTA")
            id_str = input("ID del estudiante: ").strip()
            materia = input("Materia: ").strip()
            nota_str = input("Nota (0 a 20): ").strip()

            if not es_entero_valido(id_str) or not es_flotante_valido(nota_str):
                imprimir_error("Datos numéricos inválidos.")
            else:
                exito, mensaje = sistema.agregar_nota(int(id_str), materia, float(nota_str))
                if exito:
                    imprimir_exito(mensaje)
                else:
                    imprimir_error(mensaje)
            input("\nPresione Enter para continuar...")

        elif opcion == "7":
            imprimir_titulo("VER PROMEDIO")
            id_str = input("ID del estudiante: ").strip()
            if not es_entero_valido(id_str):
                imprimir_error("ID inválido.")
            else:
                promedio, mensaje = sistema.calcular_promedio(int(id_str))
                if promedio is not None:
                    imprimir_exito(f"El promedio es: {promedio:.2f}")
                else:
                    imprimir_error(mensaje)
            input("\nPresione Enter para continuar...")

        elif opcion == "8":
            imprimir_titulo("MATERIAS OFERTADAS (GLOBAL)")
            materias = sistema.materias_ofertadas()
            if materias:
                print(f"Materias registradas en total: {list(materias)}")
            else:
                imprimir_info("No hay materias registradas aún.")
            input("\nPresione Enter para continuar...")

        elif opcion == "9":
            imprimir_titulo("MATERIAS EN COMÚN")
            id_a_str = input("ID del primer estudiante: ").strip()
            id_b_str = input("ID del segundo estudiante: ").strip()

            if not es_entero_valido(id_a_str) or not es_entero_valido(id_b_str):
                imprimir_error("IDs inválidos.")
            else:
                comun, mensaje = sistema.estudiantes_en_comun(int(id_a_str), int(id_b_str))
                if comun is not None:
                    if comun:
                        imprimir_exito(f"Materias en común: {list(comun)}")
                    else:
                        imprimir_info("No comparten materias.")
                else:
                    imprimir_error(mensaje)
            input("\nPresione Enter para continuar...")

        elif opcion == "10":
            imprimir_info("Saliendo del sistema. ¡Mucho éxito con tu tarea!")
            break
        else:
            imprimir_error("Opción inválida. Seleccione un número del 1 al 10.")
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()