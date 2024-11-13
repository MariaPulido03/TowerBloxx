import pygame
import random

# Inicialización de Pygame y el joystick
pygame.init()
pygame.joystick.init()

# Configuración inicial de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tower Bloxx")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOUSE_COLOR = (255, 255, 150)  # Color amarillo claro para la casa
WINDOW_COLOR = (135, 206, 235)  # Color azul claro para las ventanas
DOOR_COLOR = (139, 69, 19)  # Color marrón para la puerta
HOOK_COLOR = (135, 206, 235)  # Color azul cielo para el gancho

# Clase Casa
class Casa:
    def __init__(self, x, y, size=70):
        self.rect = pygame.Rect(x, y, size, size)

    def dibujar(self, surface):
        pygame.draw.rect(surface, HOUSE_COLOR, self.rect)
        pygame.draw.line(surface, BLACK, (self.rect.left, self.rect.top), (self.rect.right, self.rect.top), 4)
        pygame.draw.rect(surface, WINDOW_COLOR, (self.rect.left + 10, self.rect.top + 10, 10, 20))
        pygame.draw.rect(surface, WINDOW_COLOR, (self.rect.right - 30, self.rect.top + 10, 10, 20))
        pygame.draw.rect(surface, DOOR_COLOR, (self.rect.left + 40, self.rect.bottom - 20, 10, 20))

# Clase Grúa
class Grua:
    def __init__(self):
        self.x = screen_width // 2 - 50
        self.y = 50
        self.width = 10
        self.height = 10
        self.speed = 5
        self.direction = 1
        self.range = 200

    def mover(self):
        self.x += self.speed * self.direction
        if self.x > screen_width // 2 + self.range // 2 or self.x < screen_width // 2 - self.range // 2:
            self.direction *= -1

    def dibujar(self, surface):
        pygame.draw.rect(surface, HOOK_COLOR, (self.x, self.y, self.width, self.height))

# Clase Juego
class Juego:
    def __init__(self):
        self.bloques = []
        self.grua = Grua()
        self.score = 0
        self.falling_block = None
        self.bloques_colocados = 0  # Contador de bloques colocados
        self.base_incremento_altura = 200  # Incremento de altura base
        self.alineacion_perfecta = False
        self.juego_terminado = False
        self.mensaje = ""  # Variable para el mensaje de finalización

    def soltar_bloque(self):
        if not self.falling_block:
            block_x = self.grua.x + self.grua.width // 2 - 35
            block_y = self.grua.y + self.grua.height
            self.falling_block = Casa(block_x, block_y)

    def expandir_espacio(self):
        global screen_height, screen
        incremento_altura = self.base_incremento_altura
        screen_height += incremento_altura
        screen = pygame.display.set_mode((screen_width, screen_height))

        for bloque in self.bloques:
            bloque.rect.y += incremento_altura

    def actualizar(self):
        if self.juego_terminado:
            return

        if self.falling_block:
            self.falling_block.rect.y += 10
            self.alineacion_perfecta = False

            if self.bloques:
                last_block = self.bloques[-1]
                if self.falling_block.rect.colliderect(last_block.rect):
                    if self.falling_block.rect.x == last_block.rect.x:
                        self.score += 5
                        self.alineacion_perfecta = True
                    else:
                        self.score += 1

                    self.falling_block.rect.y = last_block.rect.y - self.falling_block.rect.height
                    self.bloques.append(self.falling_block)
                    self.bloques_colocados += 1
                    self.falling_block = None

                    if self.bloques_colocados % 3 == 0:
                        self.expandir_espacio()

            else:
                if self.falling_block.rect.y >= screen_height - self.falling_block.rect.height:
                    self.bloques.append(self.falling_block)
                    self.bloques_colocados += 1
                    self.score += 1
                    self.falling_block = None

                    if self.bloques_colocados % 3 == 0:
                        self.expandir_espacio()

        # Verificar si alcanzó los 100 bloques
        if self.bloques_colocados >= 100 and not self.juego_terminado:
            self.juego_terminado = True
            self.mensaje = f"¡Has colocado 100 bloques! Puntaje final: {self.score}"

        # Felicitación al alcanzar 500 puntos
        if self.score >= 500:
            self.mensaje = "¡Felicitaciones! Puntuación perfecta de 500 puntos"

    def dibujar(self):
        screen.fill(BLACK)

        if not self.juego_terminado:
            for bloque in self.bloques:
                bloque.dibujar(screen)

            if self.falling_block:
                self.falling_block.dibujar(screen)

            self.grua.dibujar(screen)
            self.mostrar_puntaje()

            if self.alineacion_perfecta:
                self.mostrar_mensaje("¡Alineación perfecta! +5 puntos")
        else:
            self.mostrar_pantalla_final()

    def mostrar_puntaje(self):
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))

    def mostrar_mensaje(self, mensaje):
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(mensaje, True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 50))

    def mostrar_pantalla_final(self):
        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"Juego terminado. Puntaje final: {self.score}", True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))

        quit_text = pygame.font.SysFont("Arial", 24).render("Presiona B para salir", True, WHITE)
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, screen_height // 2 + 20))

        if self.mensaje:
            self.mostrar_mensaje(self.mensaje)  # Mostrar el mensaje de finalización

# Crear una instancia del juego
juego = Juego()

# Inicializar el joystick (controlador de Xbox)
joystick = pygame.joystick.Joystick(0)
joystick.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.JOYBUTTONDOWN:  # Detecta cuando un botón del joystick es presionado
            if juego.juego_terminado:
                if event.button == 1:  # El botón B en un control Xbox es el botón 1
                    running = False  # Salir del juego
            elif event.button == 0:  # El botón X en un control Xbox es el botón 0
                juego.soltar_bloque()

    juego.grua.mover()
    juego.actualizar()
    juego.dibujar()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()


