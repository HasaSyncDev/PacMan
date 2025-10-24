# pylint: disable=no-member,import-error,no-name-in-module
import pygame
import pygame.display
import pygame.event
import pygame.font
import pygame.draw
import pygame.time
import pygame.mouse
import pygame.constants
import random
import math
from collections import deque

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
BASE_CELL_SIZE = 20
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h

# Configuración adaptable más conservadora
SCALE_FACTOR = min(SCREEN_WIDTH / 1200, SCREEN_HEIGHT / 800, 1.2)  # Limitar escala máxima
CELL_SIZE = max(16, min(24, int(BASE_CELL_SIZE * SCALE_FACTOR)))
GRID_WIDTH = 26
GRID_HEIGHT = 30
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

# Configuración de pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman - Versión Mejorada")
pygame.mouse.set_visible(False)

# Colores optimizados
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 80)
BLUE = (30, 30, 180)
LIGHT_BLUE = (100, 100, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BRIGHT_YELLOW = (255, 255, 150)
RED = (255, 50, 50)
PINK = (255, 150, 200)
CYAN = (0, 255, 255)
ORANGE = (255, 150, 50)
GREEN = (50, 255, 50)

# Variables del juego
FPS = 60
clock = pygame.time.Clock()

# Cache para optimización
path_cache = {}
collision_cache = {}

class Cursor:
    def __init__(self):
        self.visible = True
        self.pos = (0, 0)
        self.trail = deque(maxlen=3)  # Reducir trail
        
    def update(self, pos):
        self.pos = pos
        self.trail.append(pos)
        
    def draw(self):
        if not self.visible:
            return
            
        # Trail simple
        for i, pos in enumerate(self.trail):
            alpha = 200 - i * 80
            if alpha > 0:
                size = 4 - i
                pygame.draw.circle(screen, YELLOW, pos, size)
        
        # Cursor principal
        x, y = self.pos
        pygame.draw.circle(screen, BRIGHT_YELLOW, (x, y), 3)
        pygame.draw.circle(screen, WHITE, (x, y), 3, 1)

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=LIGHT_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont('Arial', 24, bold=True)
        self.hovered = False
        
    def draw(self, display_surface):
        color = self.hover_color if self.hovered else self.color
        
        # Botón simple
        pygame.draw.rect(display_surface, color, self.rect, border_radius=8)
        pygame.draw.rect(display_surface, WHITE, self.rect, 2, border_radius=8)
        
        # Texto
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        display_surface.blit(text_surf, text_rect)
        
    def is_hovered(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Menu:
    def __init__(self):
        self.background_phase = 0
        
    def draw_main_menu(self, display_surface, cursor):
        # Fondo simple
        display_surface.fill(BLACK)
        
        # Título
        title_font = pygame.font.SysFont('Arial', 64, bold=True)
        title = title_font.render("PACMAN", True, YELLOW)
        display_surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        
        # Subtítulo
        sub_font = pygame.font.SysFont('Arial', 20)
        subtitle = sub_font.render("Presiona JUGAR para comenzar", True, WHITE)
        display_surface.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//3 + 60))
        
        # Botones
        play_button = Button(WIDTH//2-100, HEIGHT//2, 200, 50, "JUGAR", GREEN)
        quit_button = Button(WIDTH//2-100, HEIGHT//2+70, 200, 50, "SALIR", RED)
        
        play_button.draw(display_surface)
        quit_button.draw(display_surface)
        
        # Instrucciones
        controls_font = pygame.font.SysFont('Arial', 16)
        controls = [
            "Controles: Flechas para mover, ESC para pausa",
            "R para reiniciar, M para menú principal"
        ]
        
        for i, control in enumerate(controls):
            text = controls_font.render(control, True, LIGHT_BLUE)
            display_surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 60 + i * 20))
        
        cursor.draw()
        return play_button, quit_button
        
    def draw_pause_menu(self, display_surface, cursor):
        # Overlay semi-transparente
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        display_surface.blit(overlay, (0, 0))
        
        # Texto de pausa
        font = pygame.font.SysFont('Arial', 48, bold=True)
        text = font.render("PAUSA", True, YELLOW)
        display_surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))
        
        # Instrucciones
        small_font = pygame.font.SysFont('Arial', 20)
        instructions = [
            "ESC: Reanudar",
            "R: Reiniciar", 
            "M: Menú principal"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, WHITE)
            display_surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + i * 30))
            
        cursor.draw()

# Laberinto original
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 1, 0, 0, 1, 2, 1, 0, 0, 1, 2, 1, 1, 2, 1, 0, 0, 1, 2, 1, 0, 0, 1, 3, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

original_maze = [row[:] for row in maze]

class PathFinder:
    @staticmethod
    def bfs(start, target, maze_grid):
        if start == target:
            return []
        
        cache_key = (start, target)
        if cache_key in path_cache:
            return path_cache[cache_key]
        
        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()
            x, y = current

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
                    maze_grid[ny][nx] != 1 and next_pos not in visited):

                    visited[next_pos] = current

                    if next_pos == target:
                        path = []
                        while next_pos != start:
                            path.append(next_pos)
                            next_pos = visited[next_pos]
                        result = path[::-1]
                        path_cache[cache_key] = result
                        return result

                    queue.append(next_pos)

        path_cache[cache_key] = []
        return []

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0
        self.speed = 0
        self.radius = CELL_SIZE // 2 - 2

    def get_grid_pos(self):
        return (int(self.x // CELL_SIZE), int(self.y // CELL_SIZE))

    def is_at_center(self):
        grid_x, grid_y = self.get_grid_pos()
        center_x = grid_x * CELL_SIZE + CELL_SIZE // 2
        center_y = grid_y * CELL_SIZE + CELL_SIZE // 2
        return abs(self.x - center_x) < 2 and abs(self.y - center_y) < 2

    def can_move(self, direction):
        grid_x, grid_y = self.get_grid_pos()
        
        cache_key = (grid_x, grid_y, direction)
        if cache_key in collision_cache:
            return collision_cache[cache_key]

        if direction == 0:
            next_x, next_y = grid_x + 1, grid_y
        elif direction == 1:
            next_x, next_y = grid_x, grid_y - 1
        elif direction == 2:
            next_x, next_y = grid_x - 1, grid_y
        elif direction == 3:
            next_x, next_y = grid_x, grid_y + 1
        else:
            collision_cache[cache_key] = False
            return False

        result = (0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT and
                 maze[next_y][next_x] != 1)
        
        if len(collision_cache) < 1000:
            collision_cache[cache_key] = result
        
        return result

    def move_in_direction(self, direction):
        if direction == 0:
            self.x += self.speed
        elif direction == 1:
            self.y -= self.speed
        elif direction == 2:
            self.x -= self.speed
        elif direction == 3:
            self.y += self.speed

        if self.x < -self.radius:
            self.x = WIDTH + self.radius
        elif self.x > WIDTH + self.radius:
            self.x = -self.radius

class Pacman(Entity):
    def __init__(self):
        super().__init__(13 * CELL_SIZE + CELL_SIZE // 2, 23 * CELL_SIZE + CELL_SIZE // 2)
        self.next_direction = 0
        self.mouth_angle = 45
        self.mouth_change = -3
        self.reset()
        self.lives = 3
        self.score = 0
        self.power_mode = False
        self.power_timer = 0
        self.invincible = 0
        self.pellets_eaten = 0

    def reset(self):
        self.x = 13 * CELL_SIZE + CELL_SIZE // 2
        self.y = 23 * CELL_SIZE + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2 - 2
        # VELOCIDAD REDUCIDA: Pacman más lento como en el juego original
        self.speed = 2.5  # Reducido de 3 a 2.5
        self.direction = 0
        self.next_direction = 0
        self.mouth_angle = 45
        self.mouth_change = -3

    def move(self):
        if self.is_at_center() and self.can_move(self.next_direction):
            self.direction = self.next_direction

        if self.can_move(self.direction):
            self.move_in_direction(self.direction)
        else:
            self.align_to_center()

        self.mouth_angle += self.mouth_change
        if self.mouth_angle <= 0 or self.mouth_angle >= 45:
            self.mouth_change = -self.mouth_change

        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False

        if self.invincible > 0:
            self.invincible -= 1

    def align_to_center(self):
        grid_x, grid_y = self.get_grid_pos()
        target_x = grid_x * CELL_SIZE + CELL_SIZE // 2
        target_y = grid_y * CELL_SIZE + CELL_SIZE // 2

        if abs(self.x - target_x) > 1:
            self.x += 1 if self.x < target_x else -1
        if abs(self.y - target_y) > 1:
            self.y += 1 if self.y < target_y else -1

    def draw(self):
        if self.invincible == 0 or (self.invincible // 10) % 2 == 0:
            # Calcular ángulos de la boca
            start_angle = 0
            end_angle = 360
            
            if self.direction == 0:
                start_angle = self.mouth_angle
                end_angle = 360 - self.mouth_angle
            elif self.direction == 1:
                start_angle = 90 + self.mouth_angle
                end_angle = 90 - self.mouth_angle
            elif self.direction == 2:
                start_angle = 180 + self.mouth_angle
                end_angle = 180 - self.mouth_angle
            elif self.direction == 3:
                start_angle = 270 + self.mouth_angle
                end_angle = 270 - self.mouth_angle

            # Dibujar Pacman
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
            
            # Boca
            points = [
                (self.x, self.y),
                (self.x + self.radius * math.cos(math.radians(start_angle)),
                 self.y - self.radius * math.sin(math.radians(start_angle))),
                (self.x + self.radius * math.cos(math.radians(end_angle)),
                 self.y - self.radius * math.sin(math.radians(end_angle)))
            ]
            pygame.draw.polygon(screen, BLACK, points)

        # Dibujar vidas
        for i in range(self.lives):
            pygame.draw.circle(screen, YELLOW, (20 + i * 25, HEIGHT - 20), 8)

class Ghost(Entity):
    def __init__(self, color, x, y, ghost_type):
        super().__init__(x, y)
        self.color = color
        # VELOCIDAD AJUSTADA: Fantasmas más rápidos que Pacman
        self.speed = 2  # Aumentado de 2 a 3.0
        self.base_speed = 2.1 
        self.direction = random.randint(0, 3)
        self.ghost_type = ghost_type
        self.frightened = False
        self.frightened_timer = 0
        self.eye_direction = 0
        self.current_mode = "scatter"
        self.mode_timer = 0
        self.last_decision_time = 0
        self.decision_interval = 10  # Más decisiones por segundo
        self.scatter_target = self.get_scatter_corner()
        self.home_position = (x, y)
        self.target_position = self.scatter_target
        self.personality_aggressiveness = self.get_personality_aggressiveness()
        self.path = []
        self.last_pacman_position = None
        self.prediction_steps = 3

    def get_personality_aggressiveness(self):
        """Define qué tan agresivo es cada fantasma"""
        return {
            "blinky": 0.9,    # Muy agresivo
            "pinky": 0.7,     # Moderadamente agresivo
            "inky": 0.6,      # Estratégico
            "clyde": 0.3      # Menos agresivo
        }.get(self.ghost_type, 0.5)

    def get_scatter_corner(self):
        corners = {
            "blinky": (GRID_WIDTH - 2, 1),
            "pinky": (1, 1),
            "inky": (GRID_WIDTH - 2, GRID_HEIGHT - 2),
            "clyde": (1, GRID_HEIGHT - 2)
        }
        return corners.get(self.ghost_type, (1, 1))

    def move(self, pacman, blinky=None):
        self.update_mode()

        if self.ghost_type == "blinky":
            self.update_speed_based_on_pellets(pacman.pellets_eaten)

        if pacman.power_mode and not self.frightened:
            self.frightened = True
            self.frightened_timer = 300
            self.speed = 1.5  # Velocidad reducida cuando está asustado

        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False
                self.speed = self.base_speed

        # Tomar decisiones más frecuentemente para mejor IA
        if self.is_at_center() and pygame.time.get_ticks() - self.last_decision_time > self.decision_interval:
            if self.frightened:
                self.move_frightened()
            else:
                if self.ghost_type == "inky" and blinky:
                    self.move_inky(pacman, blinky)
                else:
                    self.move_standard(pacman, blinky)
            self.last_decision_time = pygame.time.get_ticks()

        if self.can_move(self.direction):
            self.move_in_direction(self.direction)
        else:
            self.choose_new_direction(pacman, blinky)

        self.eye_direction = self.direction

    def update_speed_based_on_pellets(self, pellets_eaten):
        """Blinky se vuelve más rápido a medida que se comen más pellets"""
        if pellets_eaten > 100:
            self.speed = self.base_speed * 1.4
        elif pellets_eaten > 70:
            self.speed = self.base_speed * 1.3
        elif pellets_eaten > 40:
            self.speed = self.base_speed * 1.2
        elif pellets_eaten > 20:
            self.speed = self.base_speed * 1.1
        else:
            self.speed = self.base_speed

    def update_mode(self):
        """Actualiza el modo entre scatter y chase con temporizadores del original"""
        self.mode_timer -= 1
        if self.mode_timer <= 0:
            if self.current_mode == "chase":
                self.current_mode = "scatter"
                self.mode_timer = 210  # 7 segundos en scatter
            else:
                self.current_mode = "chase"
                self.mode_timer = 1020  # 34 segundos en chase

    def predict_pacman_position(self, pacman, steps=3):
        """Predice la posición futura de Pacman basado en su dirección actual"""
        pacman_pos = pacman.get_grid_pos()
        predicted_pos = pacman_pos
        
        for _ in range(steps):
            if pacman.direction == 0:  # Derecha
                predicted_pos = (predicted_pos[0] + 1, predicted_pos[1])
            elif pacman.direction == 1:  # Arriba
                predicted_pos = (predicted_pos[1] - 1, predicted_pos[1])
            elif pacman.direction == 2:  # Izquierda
                predicted_pos = (predicted_pos[0] - 1, predicted_pos[1])
            elif pacman.direction == 3:  # Abajo
                predicted_pos = (predicted_pos[1] + 1, predicted_pos[1])
            
            # Verificar si la posición predicha es válida
            if (0 <= predicted_pos[0] < GRID_WIDTH and 
                0 <= predicted_pos[1] < GRID_HEIGHT and
                maze[predicted_pos[1]][predicted_pos[0]] != 1):
                continue
            else:
                break
                
        return predicted_pos

    def get_optimal_target(self, pacman, blinky=None):
        """Calcula el objetivo óptimo basado en la personalidad del fantasma"""
        pacman_pos = pacman.get_grid_pos()
        ghost_pos = self.get_grid_pos()
        
        if self.current_mode == "scatter":
            return self.scatter_target
        
        # Comportamientos específicos por fantasma
        if self.ghost_type == "blinky":
            # Blinky: Persigue directamente a Pacman
            return pacman_pos
            
        elif self.ghost_type == "pinky":
            # Pinky: Intenta interceptar a Pacman
            return self.get_interception_point(pacman, 4)
            
        elif self.ghost_type == "inky":
            # Inky: Comportamiento más complejo e impredecible
            if blinky:
                return self.get_inky_target(pacman, blinky)
            else:
                return pacman_pos
                
        elif self.ghost_type == "clyde":
            # Clyde: Alterna entre perseguir y huir
            distance = math.dist(ghost_pos, pacman_pos)
            if distance < 8:
                return self.scatter_target
            else:
                return pacman_pos

    def get_interception_point(self, pacman, look_ahead=4):
        """Calcula punto de intercepción basado en la dirección de Pacman"""
        pacman_pos = pacman.get_grid_pos()
        pacman_dir = pacman.direction
        
        target_x, target_y = pacman_pos
        
        if pacman_dir == 0:  # Derecha
            target_x += look_ahead
        elif pacman_dir == 1:  # Arriba
            target_y -= look_ahead
        elif pacman_dir == 2:  # Izquierda
            target_x -= look_ahead
        elif pacman_dir == 3:  # Abajo
            target_y += look_ahead
        
        # Ajustar target si está fuera de límites
        target_x = max(1, min(GRID_WIDTH - 2, target_x))
        target_y = max(1, min(GRID_HEIGHT - 2, target_y))
        
        return (target_x, target_y)

    def move_standard(self, pacman, blinky=None):
        """Movimiento mejorado con pathfinding más inteligente"""
        ghost_pos = self.get_grid_pos()
        
        # Obtener objetivo basado en personalidad
        self.target_position = self.get_optimal_target(pacman, blinky)
        
        # Usar pathfinding para encontrar el mejor camino
        self.path = PathFinder.bfs(ghost_pos, self.target_position, maze)
        
        if self.path:
            next_pos = self.path[0]
            self.direction = self.get_direction_to(ghost_pos, next_pos)
        else:
            # Fallback: movimiento inteligente hacia Pacman
            self.choose_smart_direction(pacman.get_grid_pos())

    def move_inky(self, pacman, blinky):
        """Comportamiento mejorado para Inky"""
        ghost_pos = self.get_grid_pos()
        pacman_pos = pacman.get_grid_pos()
        blinky_pos = blinky.get_grid_pos()

        if self.current_mode == "scatter":
            target_pos = self.scatter_target
        else:
            # Comportamiento más impredecible para Inky
            if random.random() < 0.4:  # 40% de probabilidad de comportamiento errático
                target_pos = self.get_erratic_target(pacman_pos)
            else:
                target_pos = self.get_inky_target(pacman_pos, blinky_pos)

        self.path = PathFinder.bfs(ghost_pos, target_pos, maze)

        if self.path:
            next_pos = self.path[0]
            self.direction = self.get_direction_to(ghost_pos, next_pos)
        else:
            self.choose_smart_direction(pacman_pos)

    def get_inky_target(self, pacman_pos, blinky_pos):
        """Target mejorado para Inky - más estratégico"""
        # Vector desde Blinky hasta Pacman
        vector_x = pacman_pos[0] - blinky_pos[0]
        vector_y = pacman_pos[1] - blinky_pos[1]
        
        # Duplicar el vector para crear un punto más adelante
        target_x = pacman_pos[0] + vector_x * 2
        target_y = pacman_pos[1] + vector_y * 2
        
        # Agregar aleatoriedad controlada
        target_x += random.randint(-3, 3)
        target_y += random.randint(-3, 3)
        
        return (max(1, min(GRID_WIDTH - 2, target_x)),
                max(1, min(GRID_HEIGHT - 2, target_y)))

    def get_erratic_target(self, pacman_pos):
        """Target errático mejorado"""
        if random.random() < 0.7:
            # 70% de probabilidad de perseguir a Pacman
            return pacman_pos
        else:
            # 30% de probabilidad de movimiento aleatorio
            random_x = pacman_pos[0] + random.randint(-8, 8)
            random_y = pacman_pos[1] + random.randint(-8, 8)
            return (max(1, min(GRID_WIDTH - 2, random_x)),
                    max(1, min(GRID_HEIGHT - 2, random_y)))

    def get_direction_to(self, current_pos, target_pos):
        """Mejor cálculo de dirección considerando múltiples factores"""
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        # Preferir dirección horizontal si la diferencia es mayor
        if abs(dx) > abs(dy):
            return 0 if dx > 0 else 2
        else:
            return 3 if dy > 0 else 1

    def choose_smart_direction(self, pacman_pos):
        """Elección de dirección más inteligente"""
        ghost_pos = self.get_grid_pos()
        possible_directions = []

        for direction in range(4):
            if self.can_move(direction) and direction != (self.direction + 2) % 4:
                possible_directions.append(direction)

        if possible_directions:
            # Evaluar cada dirección posible
            best_direction = possible_directions[0]
            best_score = -float('inf')

            for direction in possible_directions:
                if direction == 0:
                    new_pos = (ghost_pos[0] + 1, ghost_pos[1])
                elif direction == 1:
                    new_pos = (ghost_pos[0], ghost_pos[1] - 1)
                elif direction == 2:
                    new_pos = (ghost_pos[0] - 1, ghost_pos[1])
                else:
                    new_pos = (ghost_pos[0], ghost_pos[1] + 1)

                # Calcular puntuación basada en distancia y agresividad
                distance_to_pacman = math.dist(new_pos, pacman_pos)
                
                # Fantasmas agresivos prefieren acercarse, otros pueden ser más cautelosos
                if self.personality_aggressiveness > 0.5:
                    score = -distance_to_pacman  # Mientras más cerca, mejor
                else:
                    score = distance_to_pacman  # Mientras más lejos, mejor (para Clyde)
                
                # Bonus por moverse hacia el objetivo
                if self.target_position:
                    distance_to_target = math.dist(new_pos, self.target_position)
                    score -= distance_to_target * 0.5

                if score > best_score:
                    best_score = score
                    best_direction = direction

            self.direction = best_direction

    def choose_new_direction(self, pacman, blinky):
        """Elección de nueva dirección mejorada"""
        possible_directions = []
        for direction in range(4):
            if self.can_move(direction) and direction != (self.direction + 2) % 4:
                possible_directions.append(direction)

        if possible_directions:
            if self.frightened:
                self.direction = random.choice(possible_directions)
            else:
                if self.ghost_type == "inky" and blinky:
                    self.move_inky(pacman, blinky)
                else:
                    self.move_standard(pacman, blinky)
        else:
            # Si no hay direcciones posibles, buscar cualquier dirección disponible
            for direction in range(4):
                if self.can_move(direction):
                    self.direction = direction
                    break

    def move_frightened(self):
        """Movimiento asustado más errático"""
        possible_directions = []
        for direction in range(4):
            if self.can_move(direction) and direction != (self.direction + 2) % 4:
                possible_directions.append(direction)

        if possible_directions:
            # Los fantasmas asustados son más erráticos
            if random.random() < 0.8:  # 80% de probabilidad de cambio aleatorio
                self.direction = random.choice(possible_directions)
            # 20% de probabilidad de mantener dirección actual

    def draw(self):
        color = BLUE if self.frightened else self.color

        if self.frightened and self.frightened_timer < 60:
            if (self.frightened_timer // 10) % 2 == 0:
                color = WHITE

        # Cuerpo del fantasma
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(screen, color,
                         (int(self.x) - self.radius, int(self.y),
                          self.radius * 2, self.radius))

        # Parte inferior ondulada
        points = []
        for i in range(5):
            x_offset = -self.radius + i * (self.radius * 2) // 4
            y_offset = self.radius + (5 if i % 2 == 0 else 0)
            points.append((int(self.x) + x_offset, int(self.y) + y_offset))
        pygame.draw.polygon(screen, color, points)

        if not self.frightened:
            # Ojos
            eye_radius = self.radius // 2
            left_eye_x = int(self.x) - eye_radius
            right_eye_x = int(self.x) + eye_radius
            eye_y = int(self.y) - eye_radius

            pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_radius)

            # Pupilas
            pupil_radius = eye_radius // 2
            dx, dy = 0, 0

            if self.eye_direction == 0:
                dx = pupil_radius
            elif self.eye_direction == 1:
                dy = -pupil_radius
            elif self.eye_direction == 2:
                dx = -pupil_radius
            elif self.eye_direction == 3:
                dy = pupil_radius

            pygame.draw.circle(screen, BLACK, (left_eye_x + dx, eye_y + dy), pupil_radius)
            pygame.draw.circle(screen, BLACK, (right_eye_x + dx, eye_y + dy), pupil_radius)

def draw_maze():
    """Dibujar laberinto simple y limpio"""
    cell_half = CELL_SIZE // 2
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell_value = maze[y][x]
            if cell_value == 0:
                continue
                
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            center_x = x * CELL_SIZE + cell_half
            center_y = y * CELL_SIZE + cell_half
            
            if cell_value == 1:
                # Paredes simples
                pygame.draw.rect(screen, DARK_BLUE, rect)
                pygame.draw.rect(screen, BLUE, rect.inflate(-4, -4))
                
            elif cell_value == 2:
                # Puntos normales
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 3)
                
            elif cell_value == 3:
                # Power-ups
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 6)
                pygame.draw.circle(screen, YELLOW, (center_x, center_y), 4)

def check_collisions(pacman, ghosts):
    grid_x, grid_y = pacman.get_grid_pos()

    # Recolectar puntos
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        cell_value = maze[grid_y][grid_x]
        if cell_value == 2:
            maze[grid_y][grid_x] = 0
            pacman.score += 10
            pacman.pellets_eaten += 1
        elif cell_value == 3:
            maze[grid_y][grid_x] = 0
            pacman.score += 50
            pacman.pellets_eaten += 1
            pacman.power_mode = True
            pacman.power_timer = 300

    # Colisiones con fantasmas
    for ghost in ghosts:
        distance = math.sqrt((pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2)
        collision_threshold = pacman.radius + ghost.radius - 2
        
        if distance < collision_threshold and pacman.invincible == 0:
            if ghost.frightened:
                # Comer fantasma
                ghost.x = ghost.home_position[0]
                ghost.y = ghost.home_position[1]
                ghost.frightened = False
                ghost.direction = random.randint(0, 3)
                pacman.score += 200
            else:
                # Perder vida
                pacman.lives -= 1
                pacman.reset()
                pacman.invincible = 120

                # Resetear fantasmas
                for g in ghosts:
                    g.x = g.home_position[0]
                    g.y = g.home_position[1]
                    g.direction = random.randint(0, 3)
                    g.frightened = False
                    g.current_mode = "scatter"
                    g.mode_timer = 210

                return True
    return False

def check_win():
    return not any(2 in row or 3 in row for row in maze)

def draw_score(pacman):
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f'Score: {pacman.score}', True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont('Arial', 48)
    text = font.render('GAME OVER', True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 24))

def draw_win():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont('Arial', 48)
    text = font.render('YOU WIN!', True, YELLOW)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 24))

def reset_game():
    global maze  # pylint: disable=global-statement,global-variable-not-assigned
    maze = [row[:] for row in original_maze]

    pacman = Pacman()
    ghosts = [
        Ghost(RED, 13 * CELL_SIZE + CELL_SIZE // 2, 11 * CELL_SIZE + CELL_SIZE // 2, "blinky"),
        Ghost(PINK, 13 * CELL_SIZE + CELL_SIZE // 2, 11 * CELL_SIZE + CELL_SIZE // 2, "pinky"),
        Ghost(CYAN, 13 * CELL_SIZE + CELL_SIZE // 2, 11 * CELL_SIZE + CELL_SIZE // 2, "inky"),
        Ghost(ORANGE, 13 * CELL_SIZE + CELL_SIZE // 2, 11 * CELL_SIZE + CELL_SIZE // 2, "clyde")
    ]

    return pacman, ghosts

def main():
    pacman, ghosts = reset_game()
    menu = Menu()
    cursor = Cursor()
    
    game_state = {
        'running': True,
        'game_over': False,
        'win': False,
        'paused': False,
        'current_screen': 'main'
    }
    
    blinky = None
    for ghost in ghosts:
        if ghost.ghost_type == "blinky":
            blinky = ghost
            break
    
    while game_state['running']:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state['running'] = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state['current_screen'] == 'game':
                        game_state['paused'] = not game_state['paused']
                    elif game_state['current_screen'] == 'main':
                        game_state['running'] = False
                elif event.key == pygame.K_m and game_state['paused']:
                    game_state['current_screen'] = 'main'
                    game_state['paused'] = False
                elif event.key == pygame.K_r and (game_state['game_over'] or game_state['win'] or game_state['paused']):
                    pacman, ghosts = reset_game()
                    game_state['game_over'] = game_state['win'] = game_state['paused'] = False
                elif event.key in (pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN):
                    pacman.next_direction = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN].index(event.key)

        cursor.update(mouse_pos)

        if game_state['current_screen'] == 'main':
            play_button, quit_button = menu.draw_main_menu(screen, cursor)
            
            if play_button.is_clicked(mouse_pos, mouse_click):
                game_state['current_screen'] = 'game'
                pacman, ghosts = reset_game()
            elif quit_button.is_clicked(mouse_pos, mouse_click):
                game_state['running'] = False
            
        elif game_state['current_screen'] == 'game':
            if not game_state['game_over'] and not game_state['win'] and not game_state['paused']:
                pacman.move()

                for ghost in ghosts:
                    if ghost.ghost_type == "inky":
                        ghost.move(pacman, blinky)
                    else:
                        ghost.move(pacman)

                if check_collisions(pacman, ghosts):
                    if pacman.lives <= 0:
                        game_state['game_over'] = True
                elif check_win():
                    game_state['win'] = True

            # Dibujar juego
            screen.fill(BLACK)
            draw_maze()
            pacman.draw()
            
            for ghost in ghosts:
                ghost.draw()
                
            draw_score(pacman)
            
            # Menús de juego
            if game_state['paused']:
                menu.draw_pause_menu(screen, cursor)
            elif game_state['game_over']:
                draw_game_over()
                
                restart_button = Button(WIDTH//2-100, HEIGHT//2+20, 200, 50, "REINICIAR", GREEN)
                menu_button = Button(WIDTH//2-100, HEIGHT//2+90, 200, 50, "MENÚ", BLUE)
                
                restart_button.draw(screen)
                menu_button.draw(screen)
                
                if restart_button.is_clicked(mouse_pos, mouse_click):
                    pacman, ghosts = reset_game()
                    game_state['game_over'] = False
                elif menu_button.is_clicked(mouse_pos, mouse_click):
                    game_state['current_screen'] = 'main'
                    game_state['game_over'] = False
                    
            elif game_state['win']:
                draw_win()
                
                restart_button = Button(WIDTH//2-100, HEIGHT//2+20, 200, 50, "JUGAR DE NUEVO", GREEN)
                menu_button = Button(WIDTH//2-100, HEIGHT//2+90, 200, 50, "MENÚ", BLUE)
                
                restart_button.draw(screen)
                menu_button.draw(screen)
                
                if restart_button.is_clicked(mouse_pos, mouse_click):
                    pacman, ghosts = reset_game()
                    game_state['win'] = False
                elif menu_button.is_clicked(mouse_pos, mouse_click):
                    game_state['current_screen'] = 'main'
                    game_state['win'] = False
            
            cursor.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()