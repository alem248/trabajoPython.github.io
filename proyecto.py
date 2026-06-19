"""
BATERÍA 3 - Ejercicio 1: Lista de Reproducción Musical
Implementación de una Lista Doblemente Enlazada para gestionar
una playlist con navegación, búsqueda e información estadística.
"""

class NodoCancion:
    """Representa un nodo de la lista doblemente enlazada (una canción)."""

    def __init__(self, id_cancion, titulo, artista, duracion, genero):
        self.id = id_cancion
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion  # Almacenado en segundos totales
        self.genero = genero
        self.siguiente = None
        self.anterior = None

    def __str__(self):
        minutos = self.duracion // 60
        segundos = self.duracion % 60
        return f"ID: {self.id} | '{self.titulo}' - {self.artista} ({minutos}:{segundos:02d}) | [{self.genero}]"


class Playlist:
    """Gestiona la lista doblemente enlazada y los controles de reproducción."""

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.cancion_actual = None
        self.siguiente_id = 1  # Contador interno para generar IDs automáticamente

    # =========================================================================
    # 1. GESTIÓN DE CANCIONES
    # =========================================================================

    def agregar_cancion(self, titulo, artista, duracion, genero):
        """Agrega una nueva canción al final de la playlist.

        El ID se genera automáticamente, el usuario no lo proporciona.
        """
        if not isinstance(duracion, int) or duracion <= 0:
            print("❌ Error: la duración debe ser un entero positivo (en segundos).")
            return

        id_cancion = self.siguiente_id
        nuevo_nodo = NodoCancion(id_cancion, titulo, artista, duracion, genero)

        if self.cabeza is None:
            # Si la lista está vacía, el nuevo nodo es todo
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            self.cancion_actual = nuevo_nodo
        else:
            # Se enlaza al final utilizando el puntero 'cola'
            self.cola.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.cola
            self.cola = nuevo_nodo

        self.siguiente_id += 1
        print(f"🎵 Añadida con éxito (ID asignado: {id_cancion}): '{titulo}'")

    def eliminar_por_posicion(self, posicion):
        """Elimina una canción por su número de posición (1-based index)."""
        if self.cabeza is None:
            print("Error: La playlist está vacía.")
            return

        total = self.contar_canciones()
        if posicion < 1 or posicion > total:
            print(f"Error: Posición {posicion} inválida. Rango actual: (1-{total}).")
            return

        nodo_actual = self.cabeza
        contador = 1

        # Avanzar hasta el nodo en la posición deseada
        while contador < posicion:
            nodo_actual = nodo_actual.siguiente
            contador += 1

        # Si el nodo a eliminar es el que se está reproduciendo, mover el reproductor
        if nodo_actual == self.cancion_actual:
            if nodo_actual.siguiente:
                self.cancion_actual = nodo_actual.siguiente
            elif nodo_actual.anterior:
                self.cancion_actual = nodo_actual.anterior
            else:
                self.cancion_actual = None

        # Reajustar los enlaces
        if nodo_actual == self.cabeza:  # Eliminar el primer elemento
            self.cabeza = nodo_actual.siguiente
            if self.cabeza:
                self.cabeza.anterior = None
            else:
                self.cola = None  # La lista se quedó vacía
        elif nodo_actual == self.cola:  # Eliminar el último elemento
            self.cola = nodo_actual.anterior
            if self.cola:
                self.cola.siguiente = None
        else:  # Eliminar un nodo intermedio
            nodo_actual.anterior.siguiente = nodo_actual.siguiente
            nodo_actual.siguiente.anterior = nodo_actual.anterior

        print(f"🗑️ Eliminada la canción en la posición {posicion}: '{nodo_actual.titulo}'")
        del nodo_actual

    def buscar_por_titulo(self, titulo):
        """Busca una canción por coincidencia exacta (sin distinguir mayúsculas)."""
        actual = self.cabeza
        while actual:
            if actual.titulo.lower() == titulo.lower():
                print(f"🔍 Encontrada: {actual}")
                return actual
            actual = actual.siguiente
        print(f"🔍 No se encontró ninguna canción con el título '{titulo}'.")
        return None

    def buscar_por_artista(self, artista):
        """Muestra todas las canciones pertenecientes a un artista."""
        actual = self.cabeza
        encontrado = False
        print(f"\n🎼 Resultados para el artista '{artista}':")
        while actual:
            if actual.artista.lower() == artista.lower():
                print(f"   - {actual}")
                encontrado = True
            actual = actual.siguiente
        if not encontrado:
            print("   No se encontraron canciones registradas de este artista.")

    # =========================================================================
    # 2. REPRODUCCIÓN
    # =========================================================================

    def reproducir_actual(self):
        """Muestra la canción seleccionada actualmente."""
        if self.cancion_actual is None:
            print("\n⏹️ No hay ninguna canción en reproducción.")
        else:
            print(f"\n▶️ Reproduciendo: {self.cancion_actual}")

    def siguiente_cancion(self):
        """Avanza a la canción de la derecha (siguiente)."""
        if self.cancion_actual is None:
            print("\n⚠️ La playlist está vacía.")
        elif self.cancion_actual.siguiente:
            self.cancion_actual = self.cancion_actual.siguiente
            self.reproducir_actual()
        else:
            print("\n⚠️ Ya estás en la última canción. No hay pista siguiente.")

    def anterior_cancion(self):
        """Retrocede a la canción de la izquierda (anterior)."""
        if self.cancion_actual is None:
            print("\n⚠️ La playlist está vacía.")
        elif self.cancion_actual.anterior:
            self.cancion_actual = self.cancion_actual.anterior
            self.reproducir_actual()
        else:
            print("\n⚠️ Ya estás en la primera canción. No hay pista anterior.")

    def ir_a_primera(self):
        """Salta directamente al primer nodo de la lista."""
        if self.cabeza:
            self.cancion_actual = self.cabeza
            print("\n⏮️ Saltando a la primera canción:")
            self.reproducir_actual()
        else:
            print("\n⚠️ La playlist está vacía.")

    def ir_a_ultima(self):
        """Salta directamente al último nodo de la lista."""
        if self.cola:
            self.cancion_actual = self.cola
            print("\n⏭️ Saltando a la última canción:")
            self.reproducir_actual()
        else:
            print("\n⚠️ La playlist está vacía.")

    def seleccionar_por_posicion(self, posicion):
        """Apunta la reproducción a una canción específica mediante su índice."""
        total = self.contar_canciones()
        if posicion < 1 or posicion > total:
            print(f"❌ Posición {posicion} fuera de rango.")
            return

        actual = self.cabeza
        contador = 1
        while contador < posicion:
            actual = actual.siguiente
            contador += 1

        self.cancion_actual = actual
        print(f"\n🔄 Cambiado a posición {posicion}:")
        self.reproducir_actual()

    # =========================================================================
    # 3. INFORMACIÓN
    # =========================================================================

    def mostrar_playlist(self):
        """Imprime secuencialmente toda la playlist con sus posiciones."""
        if self.cabeza is None:
            print("\n--- Playlist Vacía ---")
            return

        print("\n==================== MI PLAYLIST ====================")
        actual = self.cabeza
        posicion = 1
        while actual:
            # Indicador dinámico para saber qué se está escuchando en la lista
            indicador = "👉" if actual == self.cancion_actual else "  "
            print(f"{indicador} [{posicion}] {actual}")
            actual = actual.siguiente
            posicion += 1
        print("=====================================================")

    def contar_canciones(self):
        """Devuelve el total de nodos en la lista."""
        actual = self.cabeza
        contador = 0
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def calcular_duracion_total(self):
        """Suma la duración de cada nodo y la presenta de manera legible."""
        actual = self.cabeza
        total_segundos = 0
        while actual:
            total_segundos += actual.duracion
            actual = actual.siguiente

        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60

        print(f"\n⏱️ Duración Total: {horas}h {minutos}m {segundos}s ({total_segundos} segundos)")
        return total_segundos

    def mostrar_por_genero(self, genero):
        """Muestra en pantalla una lista filtrada por el género ingresado."""
        actual = self.cabeza
        encontrado = False
        print(f"\n🎷 Canciones del género '{genero}':")
        while actual:
            if actual.genero.lower() == genero.lower():
                print(f"   - '{actual.titulo}' de {actual.artista}")
                encontrado = True
            actual = actual.siguiente
        if not encontrado:
            print("   No hay canciones asociadas a este género.")

    def cancion_mas_larga_y_corta(self):
        """Evalúa los extremos de tiempo entre los nodos cargados."""
        if self.cabeza is None:
            print("⚠️ Playlist vacía. No se pueden calcular extremos.")
            return

        mas_larga = self.cabeza
        mas_corta = self.cabeza
        actual = self.cabeza.siguiente

        while actual:
            if actual.duracion > mas_larga.duracion:
                mas_larga = actual
            if actual.duracion < mas_corta.duracion:
                mas_corta = actual
            actual = actual.siguiente

        print(f"\n🔝 Canción más larga: '{mas_larga.titulo}' con {mas_larga.duracion} segundos.")
        print(f"⬇️ Canción más corta: '{mas_corta.titulo}' con {mas_corta.duracion} segundos.")


# =========================================================================
# MENÚ INTERACTIVO
# =========================================================================

def pedir_entero(mensaje):
    """Solicita un entero al usuario validando el formato."""
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            print("❌ Por favor ingresa un número entero válido.")


def menu():
    reproductor = Playlist()

    opciones = """
==================== REPRODUCTOR DE MÚSICA ====================
 1. Agregar canción
 2. Eliminar canción por posición
 3. Buscar canción por título
 4. Buscar canciones por artista
 5. Reproducir canción actual
 6. Siguiente canción
 7. Canción anterior
 8. Ir a la primera canción
 9. Ir a la última canción
10. Seleccionar canción por posición
11. Mostrar playlist completa
12. Contar canciones
13. Calcular duración total
14. Mostrar canciones por género
15. Canción más larga y más corta
16. Cargar canciones de ejemplo
 0. Salir
=================================================================
"""

    while True:
        print(opciones)
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            titulo = input("Título: ").strip()
            artista = input("Artista: ").strip()
            duracion = pedir_entero("Duración (segundos): ")
            genero = input("Género: ").strip()
            reproductor.agregar_cancion(titulo, artista, duracion, genero)

        elif opcion == "2":
            pos = pedir_entero("Posición a eliminar: ")
            reproductor.eliminar_por_posicion(pos)

        elif opcion == "3":
            titulo = input("Título a buscar: ").strip()
            reproductor.buscar_por_titulo(titulo)

        elif opcion == "4":
            artista = input("Artista a buscar: ").strip()
            reproductor.buscar_por_artista(artista)

        elif opcion == "5":
            reproductor.reproducir_actual()

        elif opcion == "6":
            reproductor.siguiente_cancion()

        elif opcion == "7":
            reproductor.anterior_cancion()

        elif opcion == "8":
            reproductor.ir_a_primera()

        elif opcion == "9":
            reproductor.ir_a_ultima()

        elif opcion == "10":
            pos = pedir_entero("Posición a seleccionar: ")
            reproductor.seleccionar_por_posicion(pos)

        elif opcion == "11":
            reproductor.mostrar_playlist()

        elif opcion == "12":
            print(f"\n🔢 Cantidad de temas actuales: {reproductor.contar_canciones()}")

        elif opcion == "13":
            reproductor.calcular_duracion_total()

        elif opcion == "14":
            genero = input("Género a filtrar: ").strip()
            reproductor.mostrar_por_genero(genero)

        elif opcion == "15":
            reproductor.cancion_mas_larga_y_corta()

        elif opcion == "16":
            reproductor.agregar_cancion("Bohemian Rhapsody", "Queen", 355, "Rock")
            reproductor.agregar_cancion("Blinding Lights", "The Weeknd", 200, "Pop")
            reproductor.agregar_cancion("Hotel California", "Eagles", 390, "Rock")
            reproductor.agregar_cancion("Save Your Tears", "The Weeknd", 215, "Pop")
            print("✅ Canciones de ejemplo cargadas.")

        elif opcion == "0":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción inválida, intenta de nuevo.")


if __name__ == "__main__":
    print("\n\n¿Deseas usar el menú interactivo? (s/n)")
    if input().strip().lower() == "s":
        menu()
