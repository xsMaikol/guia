def imprimir_titulo(titulo):
    print("\n" + "=" * 50)
    print(f" {titulo} ".center(50, "="))
    print("=" * 50)

def imprimir_exito(mensaje):
    print(f"[ÉXITO]: {mensaje}")

def imprimir_error(mensaje):
    print(f"[ERROR]: {mensaje}")

def imprimir_info(mensaje):
    print(f"[INFO]: {mensaje}")

def confirmar(mensaje):
    respuesta = input(f"{mensaje} (s/n): ").strip().lower()
    return respuesta == 's'

def es_entero_valido(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def es_flotante_valido(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False