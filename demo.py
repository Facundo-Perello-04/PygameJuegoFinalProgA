# =============================================================
#  SECTOR 7 — Shooter Espacial Vertical 2D
#  Archivo único, sin dependencias externas.
#  Autor: Facundo Perello
# =============================================================

import pygame
import random

# ─────────────────────────────────────────────
#  CONFIGURACIÓN GLOBAL DEL JUEGO
#  Modificar estas constantes cambia el juego entero.
# ─────────────────────────────────────────────
ANCHO_PANTALLA  = 600          # Ancho de la ventana en píxeles
ALTO_PANTALLA   = 700          # Alto  de la ventana en píxeles
FPS             = 60           # Fotogramas por segundo

# Colores (R, G, B) — sin imágenes externas
COLOR_FONDO      = (5,   5,  20)   # Azul muy oscuro, estilo espacio
COLOR_JUGADOR    = (0,  220, 80)   # Verde brillante
COLOR_ENEMIGO    = (220,  40, 40)  # Rojo intenso
COLOR_BALA       = (255, 230, 50)  # Amarillo
COLOR_TEXTO      = (255, 255, 255) # Blanco
COLOR_TITULO     = (80,  200, 255) # Azul cielo para HUD

# ─────────────────────────────────────────────
#  CLASE: Jugador
# ─────────────────────────────────────────────
class Jugador(pygame.sprite.Sprite):
    """Nave del jugador. Se mueve en el eje X con las flechas."""

    VELOCIDAD      = 5     # ← MODIFICAR AQUÍ SI EL PROFESOR PIDE CAMBIAR LA VELOCIDAD DE LA NAVE
    CADENCIA       = 20    # ← MODIFICAR AQUÍ PARA LA CADENCIA DE DISPARO (fotogramas entre disparos; menor = más rápido)
    ANCHO_SPRITE   = 50
    ALTO_SPRITE    = 40

    def __init__(self):
        super().__init__()

        # Dibujar la nave como un triángulo verde sobre un Surface transparente
        self.image = pygame.Surface((self.ANCHO_SPRITE, self.ALTO_SPRITE), pygame.SRCALPHA)
        puntos = [
            (self.ANCHO_SPRITE // 2, 0),                    # Punta superior (morro)
            (0,          self.ALTO_SPRITE),                 # Esquina inferior izquierda
            (self.ANCHO_SPRITE, self.ALTO_SPRITE),          # Esquina inferior derecha
        ]
        pygame.draw.polygon(self.image, COLOR_JUGADOR, puntos)

        # Rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO_PANTALLA // 2            # Empieza centrado
        self.rect.bottom   = ALTO_PANTALLA - 20            # Pegado al fondo

        self.cooldown = 0   # Contador de espera entre disparos

    def update(self, teclas):
        """Mueve la nave según las teclas presionadas y decrementa el cooldown."""

        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.VELOCIDAD
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.VELOCIDAD

        # Evitar salir de los bordes de la pantalla
        self.rect.left  = max(0, self.rect.left)
        self.rect.right = min(ANCHO_PANTALLA, self.rect.right)

        # Reducir el temporizador de cadencia cada frame
        if self.cooldown > 0:
            self.cooldown -= 1

    def puede_disparar(self):
        """Retorna True si ya pasó suficiente tiempo desde el último disparo."""
        return self.cooldown == 0

    def disparar(self):
        """Crea una bala y reinicia el cooldown."""
        self.cooldown = self.CADENCIA
        return Bala(self.rect.centerx, self.rect.top)


# ─────────────────────────────────────────────
#  CLASE: Bala
# ─────────────────────────────────────────────
class Bala(pygame.sprite.Sprite):
    """Proyectil disparado por el jugador. Sube recto."""

    VELOCIDAD    = 10    # ← MODIFICAR AQUÍ PARA CAMBIAR LA VELOCIDAD DEL PROYECTIL
    ANCHO_SPRITE = 6
    ALTO_SPRITE  = 14

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((self.ANCHO_SPRITE, self.ALTO_SPRITE))
        self.image.fill(COLOR_BALA)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom   = y   # Nace en la punta de la nave

    def update(self):
        """Sube verticalmente cada frame. Se destruye al salir de la pantalla."""
        self.rect.y -= self.VELOCIDAD
        if self.rect.bottom < 0:
            self.kill()   # Elimina el sprite de todos los grupos


# ─────────────────────────────────────────────
#  CLASE: Enemigo (asteroide)
# ─────────────────────────────────────────────
class Enemigo(pygame.sprite.Sprite):
    """Asteroide que cae desde la parte superior en una posición X aleatoria."""

    VELOCIDAD_MIN = 2   # ← MODIFICAR AQUÍ PARA QUE LOS ENEMIGOS CAIGAN MÁS LENTO (valor mínimo)
    VELOCIDAD_MAX = 5   # ← MODIFICAR AQUÍ PARA QUE LOS ENEMIGOS CAIGAN MÁS RÁPIDO (valor máximo)
    TAMANIO       = 36  # ← MODIFICAR AQUÍ PARA CAMBIAR EL TAMAÑO DE LOS ASTEROIDES

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((self.TAMANIO, self.TAMANIO), pygame.SRCALPHA)

        # Dibujar un círculo rojo irregular (simula un asteroide)
        cx = cy = self.TAMANIO // 2
        pygame.draw.circle(self.image, COLOR_ENEMIGO, (cx, cy), cx)
        pygame.draw.circle(self.image, (180, 20, 20), (cx - 5, cy - 4), cx // 3)  # Mancha decorativa

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.TAMANIO)  # Posición X aleatoria
        self.rect.y = -self.TAMANIO   # Empieza fuera de la pantalla (arriba)

        # Velocidad aleatoria dentro del rango configurado
        self.velocidad = random.randint(self.VELOCIDAD_MIN, self.VELOCIDAD_MAX)

    def update(self):
        """Cae verticalmente. Se destruye al salir por abajo."""
        self.rect.y += self.velocidad
        if self.rect.top > ALTO_PANTALLA:
            self.kill()


# ─────────────────────────────────────────────
#  FUNCIÓN: dibujar_estrellas
#  Fondo con estrellas estáticas (decorativo).
# ─────────────────────────────────────────────
def crear_estrellas(cantidad=80):
    """Genera una lista de posiciones y tamaños para las estrellas del fondo."""
    return [
        (random.randint(0, ANCHO_PANTALLA),
         random.randint(0, ALTO_PANTALLA),
         random.randint(1, 2))   # tamaño 1 o 2 px
        for _ in range(cantidad)
    ]

def dibujar_estrellas(pantalla, estrellas):
    for x, y, tam in estrellas:
        pygame.draw.circle(pantalla, (200, 200, 200), (x, y), tam)


# ─────────────────────────────────────────────
#  FUNCIÓN: mostrar_hud
#  Muestra el puntaje y las vidas en pantalla.
# ─────────────────────────────────────────────
def mostrar_hud(pantalla, fuente, puntaje):
    texto = fuente.render(f"PUNTAJE: {puntaje}", True, COLOR_TITULO)
    pantalla.blit(texto, (10, 10))


# ─────────────────────────────────────────────
#  FUNCIÓN: pantalla_game_over
#  Muestra el puntaje final y espera input del jugador.
# ─────────────────────────────────────────────
def pantalla_game_over(pantalla, fuente_grande, fuente_chica, puntaje):
    """Bloquea el loop principal y muestra la pantalla de Game Over."""
    pantalla.fill(COLOR_FONDO)

    linea1 = fuente_grande.render("GAME OVER", True, (220, 50, 50))
    linea2 = fuente_chica.render(f"Puntaje final: {puntaje}", True, COLOR_TEXTO)
    linea3 = fuente_chica.render("Presioná R para reiniciar  |  ESC para salir", True, (160, 160, 160))

    pantalla.blit(linea1, linea1.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 60)))
    pantalla.blit(linea2, linea2.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 10)))
    pantalla.blit(linea3, linea3.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 60)))
    pygame.display.flip()

    # Esperar decisión del jugador
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False   # Salir del juego
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True    # Reiniciar
                if evento.key == pygame.K_ESCAPE:
                    return False   # Salir


# ─────────────────────────────────────────────
#  FUNCIÓN: iniciar_juego
#  Crea y devuelve todos los objetos del juego desde cero.
# ─────────────────────────────────────────────
def iniciar_juego():
    """Instancia al jugador y todos los grupos de sprites. Permite reiniciar limpiamente."""
    jugador      = Jugador()
    grupo_todo   = pygame.sprite.Group()
    grupo_balas  = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()

    grupo_todo.add(jugador)

    return jugador, grupo_todo, grupo_balas, grupo_enemigos


# ─────────────────────────────────────────────
#  LOOP PRINCIPAL
# ─────────────────────────────────────────────
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Sector 7")
    reloj = pygame.time.Clock()

    fuente_grande = pygame.font.SysFont("consolas", 52, bold=True)
    fuente_chica  = pygame.font.SysFont("consolas", 24)

    estrellas = crear_estrellas()

    # ─── Variables del juego ─────────────────
    INTERVALO_SPAWN = 60   # ← MODIFICAR AQUÍ PARA CAMBIAR CADA CUÁNTOS FRAMES APARECE UN ENEMIGO (menor = más frecuente)
    PUNTOS_POR_ENEMIGO = 10  # ← MODIFICAR AQUÍ PARA CAMBIAR CUÁNTOS PUNTOS DA CADA ENEMIGO

    jugando = True
    while jugando:   # Loop externo: permite reiniciar el juego

        jugador, grupo_todo, grupo_balas, grupo_enemigos = iniciar_juego()
        puntaje      = 0
        frame        = 0   # Contador de frames para el spawn de enemigos
        partida_activa = True

        while partida_activa:   # Loop interno: una partida
            reloj.tick(FPS)
            frame += 1

            # ─── Eventos ─────────────────────
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jugando = False
                    partida_activa = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and jugador.puede_disparar():
                        bala = jugador.disparar()
                        grupo_balas.add(bala)
                        grupo_todo.add(bala)

            # ─── Spawner de enemigos ──────────
            if frame % INTERVALO_SPAWN == 0:
                enemigo = Enemigo()
                grupo_enemigos.add(enemigo)
                grupo_todo.add(enemigo)

            # ─── Actualización ───────────────
            teclas = pygame.key.get_pressed()
            jugador.update(teclas)
            grupo_balas.update()
            grupo_enemigos.update()

            # ─── Colisiones: bala vs enemigo ─
            colisiones = pygame.sprite.groupcollide(
                grupo_balas, grupo_enemigos, True, True   # True, True = elimina ambos sprites
            )
            puntaje += len(colisiones) * PUNTOS_POR_ENEMIGO

            # ─── Colisión: enemigo vs jugador ─
            if pygame.sprite.spritecollide(jugador, grupo_enemigos, False):
                partida_activa = False   # Game Over

            # ─── Dibujo ──────────────────────
            pantalla.fill(COLOR_FONDO)
            dibujar_estrellas(pantalla, estrellas)
            grupo_todo.draw(pantalla)
            mostrar_hud(pantalla, fuente_chica, puntaje)
            pygame.display.flip()

        # ─── Fin de partida ──────────────────
        if jugando:
            reiniciar = pantalla_game_over(pantalla, fuente_grande, fuente_chica, puntaje)
            jugando = reiniciar

    pygame.quit()


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()