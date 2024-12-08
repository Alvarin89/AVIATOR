import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 1280, 720
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Aviator")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

# Fuentes
FUENTE = pygame.font.Font(None, 36)
TITULO_FUENTE = pygame.font.Font(None, 72)

# Cargar imágenes
FONDO = pygame.image.load("imagenes/desierto.jpg")
FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))

AVION = pygame.image.load("imagenes/avion.png")
AVION = pygame.transform.scale(AVION, (80, 60))

# Clase para manejar el juego Aviator
class JuegoAviator:
    def __init__(self):
        self.saldo = 1000  # Saldo inicial por defecto
        self.apuesta = 0
        self.multiplicador = 1.0
        self.posicion_x = 50  # Posición inicial del avión
        self.volando = False
        self.retirar = False
        self.avion_cayo = False
        self.tiempo_inicio = 0

    def reiniciar(self):
        """Reinicia los valores del juego para una nueva ronda."""
        self.multiplicador = 1.0
        self.posicion_x = 50
        self.volando = True
        self.retirar = False
        self.avion_cayo = False
        self.tiempo_inicio = pygame.time.get_ticks()

    def actualizar_vuelo(self):
        """Actualiza la posición y el estado del avión."""
        if self.volando:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio > 1000:  # Incremento más lento cada 1 segundo
                self.tiempo_inicio = tiempo_actual
                incremento = 0.05  # Velocidad de multiplicador más lenta
                self.multiplicador += incremento
                self.posicion_x += 2  # Movimiento horizontal del avión

                # Probabilidad de que el avión se caiga
                if random.random() < 0.01:
                    self.volando = False
                    self.avion_cayo = True
                    self.multiplicador = 0  # Perdiste


# Función para crear un botón
def crear_boton(texto, x, y, ancho, alto, color, color_hover):
    mouse = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()

    # Cambiar color si el mouse está encima
    color_actual = color_hover if x < mouse[0] < x + ancho and y < mouse[1] < y + alto else color
    pygame.draw.rect(VENTANA, color_actual, (x, y, ancho, alto))

    # Dibujar texto en el botón
    texto_boton = FUENTE.render(texto, True, NEGRO)
    VENTANA.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))

    # Verificar clic
    if clic[0] == 1 and x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        return True
    return False


def mostrar_menu():
    """Muestra el menú principal con un botón para comenzar el juego."""
    menu_activo = True
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Dibujar fondo
        VENTANA.blit(FONDO, (0, 0))

        # Dibujar título
        titulo_texto = TITULO_FUENTE.render("AVIATOR", True, BLANCO)
        VENTANA.blit(titulo_texto, ((ANCHO - titulo_texto.get_width()) // 2, ALTO // 4))

        # Dibujar botón de comenzar
        if crear_boton("Comenzar", ANCHO // 2 - 100, ALTO // 2, 200, 50, VERDE, BLANCO):
            menu_activo = False

        pygame.display.flip()


def aviator_game():
    mostrar_menu()

    juego = JuegoAviator()
    reloj = pygame.time.Clock()
    input_monto = ""
    jugando = True

    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    input_monto = input_monto[:-1]
                elif evento.unicode.isdigit() or (evento.unicode == "." and "." not in input_monto):
                    input_monto += evento.unicode

        # Actualizar lógica del juego
        if juego.volando:
            juego.actualizar_vuelo()

        # Dibujar fondo
        VENTANA.blit(FONDO, (0, 0))

        # Mostrar saldo y multiplicador
        texto_saldo = FUENTE.render(f"Saldo: ${juego.saldo:.2f}", True, BLANCO)
        texto_multiplicador = FUENTE.render(f"Multiplicador: x{juego.multiplicador:.2f}", True, BLANCO)
        VENTANA.blit(texto_saldo, (10, 10))
        VENTANA.blit(texto_multiplicador, (10, 50))

        # Campo de entrada para la apuesta
        pygame.draw.rect(VENTANA, GRIS, (10, 100, 200, 40))
        texto_apuesta = FUENTE.render(input_monto, True, NEGRO)
        VENTANA.blit(texto_apuesta, (15, 105))

        # Botón para apostar
        if crear_boton("Apostar", 10, 160, 200, 50, VERDE, BLANCO):
            if input_monto and float(input_monto) <= juego.saldo:
                juego.apuesta = float(input_monto)
                juego.saldo -= float(input_monto)
                juego.reiniciar()
                input_monto = ""
            else:
                print("Monto inválido o saldo insuficiente.")

        # Botón para retirar
        if crear_boton("Retirar", 220, 160, 200, 50, ROJO, BLANCO):
            if juego.volando:
                juego.volando = False
                ganancias = juego.apuesta * juego.multiplicador
                juego.saldo += ganancias
                print(f"Retiraste con multiplicador x{juego.multiplicador:.2f}. Ganaste ${ganancias:.2f}")

        # Dibujar el avión en movimiento si está volando
        if juego.volando:
            VENTANA.blit(AVION, (juego.posicion_x, ALTO // 2 - 30))

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()


# Ejecutar el juego
aviator_game()
