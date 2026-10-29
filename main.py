# menu principal con crud para la manipulacion de los datos
from docentes import RepositorioDocentes, DocenteError
from formatos import exportar, guardar


def mostrar_docentes(docentes):
    if not docentes:
        print("\nNo hay docentes registrados")
        return
    print("\n Docentes ED. 2")
    print(f"{'No. empleado':<16} {'Nombre':<35} {'Especialidad'}")
    print("-" * 75)
    for d in docentes:
        print(f"{d.numero_empleado:<16} {d.nombre:<35} {d.especialidad}")


def get_data():
    numero = input("Numero de empleado: ").strip()  # strip elimina espacios innecesarios
    nombre = input("Nombre completo: ").strip()
    especialidad = input("Especialidad: ").strip()
    return numero, nombre, especialidad


def pedir_formato() -> str:
    while True:
        formato = input("Formato (json/yaml/xml): ").strip().lower()
        if formato in ("json", "yaml", "xml"):
            return formato
        print("Formato invalido.")


def menu():
    repo = RepositorioDocentes("docentes.json")

    while True:
        print("""
Sistema de Docentes - ED 2
1. Registrar docente
2. Consultar docentes
3. Buscar docente por num de empleado
4. Actualizar docente
5. Eliminar docente
6. Exportar a YAML, XML o JSON
0. Salir
""")
        opcion = input("Opcion: ").strip()

        try:
            if opcion == "1":
                numero, nombre, especialidad = get_data()
                repo.crear(numero, nombre, especialidad)
                print("\nDocente registrado")

            elif opcion == "2":
                mostrar_docentes(repo.listar())

            elif opcion == "3":
                num = input("Numero de empleado: ").strip()
                mostrar_docentes([repo.obtener(num)])

            elif opcion == "4":
                num = input("Numero de empleado a actualizar: ").strip()
                print("(Enter para dejar igual)")
                d = repo.actualizar(
                    num,
                    nombre=input("Nuevo nombre: "),
                    especialidad=input("Nueva especialidad: "),
                )
                print("\nDocente actualizado")
                mostrar_docentes([d])

            elif opcion == "5":
                num = input("Numero de empleado a eliminar: ").strip()
                d = repo.eliminar(num)
                print(f"\nDocente eliminado: {d.nombre}")

            elif opcion == "6":
                print("a) Todos   b) Uno solo")
                alcance = input("Opcion: ").strip().lower()
                if alcance == "a":
                    docentes = repo.listar()
                    nombre_archivo = "exportacion_docentes"
                elif alcance == "b":
                    num = input("Numero de empleado: ").strip()
                    docentes = [repo.obtener(num)]
                    nombre_archivo = f"exportacion_docente_{num}"
                else:
                    print("\nOpcion invalida")
                    continue

                formato = pedir_formato()
                print()
                print(exportar(docentes, formato))  # se ve en pantalla
                ruta = guardar(docentes, formato, nombre_archivo)  # y se guarda
                print(f"\nArchivo guardado: {ruta}")

            elif opcion == "0":
                print("Hasta luego")
                break

            else:
                print("\nOpcion invalida")

        except DocenteError as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    menu()