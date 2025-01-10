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
MULTIPLICADOR_FUENTE = pygame.font.Font(None, 64)
MENSAJE_FUENTE = pygame.font.Font(None, 50)

# Cargar imágenes
FONDO = pygame.image.load("imagenes/desierto1.png")
FONDO = pygame.transform.scale(FONDO, (ANCHO, ALTO))
TITULO_IMAGEN = pygame.image.load("imagenes/image.png")
TITULO_IMAGEN = pygame.transform.scale(TITULO_IMAGEN, (500, 250))
AVION = pygame.image.load("imagenes/image1.png")
AVION = pygame.transform.scale(AVION, (550, 250))
EXPLOSION = pygame.image.load("imagenes/image2.png")
EXPLOSION = pygame.transform.scale(EXPLOSION, (550, 250))

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
        self.mensaje = ""

    def reiniciar(self):
        """Reinicia los valores del juego para una nueva ronda."""
        self.multiplicador = random.uniform(1.0, 1.5)  # Multiplicador inicial aleatorio
        self.posicion_x = 50
        self.volando = True
        self.retirar = False
        self.avion_cayo = False
        self.tiempo_inicio = pygame.time.get_ticks()
        self.mensaje = ""

    def actualizar_vuelo(self):
        """Actualiza la posición y el estado del avión."""
        if self.volando:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_inicio > 1000:  # Incremento cada 1 segundo
                self.tiempo_inicio = tiempo_actual
                incremento = random.uniform(0.02, 0.05)  # Incremento aleatorio
                self.multiplicador += incremento

            self.posicion_x += 3  # Movimiento horizontal más lento del avión

            # Probabilidad de que el avión se caiga
            if random.random() < 0.01:
                self.volando = False
                self.avion_cayo = True
                self.multiplicador = 0  # Perdiste
                self.mensaje = "¡Has perdido!"

# Función para crear un botón con esquinas curvas
def crear_boton(texto, x, y, ancho, alto, color, color_hover):
    mouse = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()

    # Cambiar color si el mouse está encima
    color_actual = color_hover if x < mouse[0] < x + ancho and y < mouse[1] < y + alto else color
    pygame.draw.rect(VENTANA, color_actual, (x, y, ancho, alto), border_radius=15)

    # Dibujar texto en el botón
    texto_boton = FUENTE.render(texto, True, NEGRO)
    VENTANA.blit(texto_boton, (x + (ancho - texto_boton.get_width()) // 2, y + (alto - texto_boton.get_height()) // 2))

    # Verificar clic
    if clic[0] == 1 and x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        return True
    return False

def mostrar_menu():
    """Muestra el menú principal con botones para comenzar y salir del juego."""
    menu_activo = True
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Dibujar fondo
        VENTANA.blit(FONDO, (0, 0))

        # Dibujar título (imagen)
        VENTANA.blit(TITULO_IMAGEN, ((ANCHO - TITULO_IMAGEN.get_width()) // 2, ALTO // 5))  # Ajusta ALTO // 5 para mover

        # Dibujar botón de comenzar
        if crear_boton("Comenzar", ANCHO // 2 - 220, ALTO // 2, 200, 50, VERDE, BLANCO):
            menu_activo = False

        # Dibujar botón de salir
        if crear_boton("Salir", ANCHO // 2 + 20, ALTO // 2, 200, 50, ROJO, BLANCO):
            pygame.quit()
            exit()

        pygame.display.flip()

def aviator_game():
    while True:
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
                    elif evento.key == pygame.K_RETURN and input_monto:
                        if float(input_monto) <= juego.saldo:
                            juego.apuesta = float(input_monto)
                            juego.saldo -= float(input_monto)
                            juego.reiniciar()
                            input_monto = ""

            # Actualizar lógica del juego
            if juego.volando:
                juego.actualizar_vuelo()

            # Dibujar fondo
            VENTANA.blit(FONDO, (0, 0))

            # Mostrar saldo en la esquina superior derecha
            texto_saldo = FUENTE.render(f"Saldo: ${juego.saldo:.2f}", True, NEGRO)
            VENTANA.blit(texto_saldo, (ANCHO - texto_saldo.get_width() - 10, 10))

            # Mostrar multiplicador en la parte superior centrada
            texto_multiplicador = MULTIPLICADOR_FUENTE.render(f"x{juego.multiplicador:.2f}", True, NEGRO)
            VENTANA.blit(texto_multiplicador, ((ANCHO - texto_multiplicador.get_width()) // 2, 20))

            # Campo de entrada para la apuesta
            pygame.draw.rect(VENTANA, GRIS, (ANCHO // 2 - 100, ALTO - 170, 200, 40))
            texto_apuesta = FUENTE.render(input_monto, True, NEGRO)
            VENTANA.blit(texto_apuesta, (ANCHO // 2 - texto_apuesta.get_width() // 2, ALTO - 165))

            # Botón para regresar al menú
            if crear_boton("Menú", 10, 10, 100, 40, GRIS, BLANCO):
                jugando = False

            # Botones para apostar y retirar centrados en la parte inferior
            if crear_boton("Apostar", ANCHO // 2 - 220, ALTO - 100, 200, 50, VERDE, BLANCO):
                if input_monto and float(input_monto) <= juego.saldo:
                    juego.apuesta = float(input_monto)
                    juego.saldo -= float(input_monto)
                    juego.reiniciar()
                    input_monto = ""

            if crear_boton("Retirar", ANCHO // 2 + 20, ALTO - 100, 200, 50, ROJO, BLANCO):
                if juego.volando:
                    juego.volando = False
                    ganancias = juego.apuesta * juego.multiplicador
                    juego.saldo += ganancias
                    juego.mensaje = f"¡Has ganado ${ganancias:.2f}!"

            if juego.volando:
                VENTANA.blit(AVION, (juego.posicion_x, ALTO // 2 - 30))
            elif juego.avion_cayo:
                VENTANA.blit(EXPLOSION, (juego.posicion_x, ALTO // 2 - 30))

            # Mostrar mensaje en el centro si aplica
            if juego.mensaje:
                mensaje_texto = MENSAJE_FUENTE.render(juego.mensaje, True, NEGRO)
                VENTANA.blit(mensaje_texto, ((ANCHO - mensaje_texto.get_width()) // 2, ALTO // 2 - 100))

            pygame.display.flip()
            reloj.tick(30)

    pygame.quit()

# Ejecutar el juego
aviator_game()