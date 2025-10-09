import pygame
import random
import math
from collections import deque

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
CELL_SIZE = 25
GRID_WIDTH = 26
GRID_HEIGHT = 30
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Profesional")

# Colores
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Variables del juego
FPS = 60
clock = pygame.time.Clock()

# Laberinto (0: vacío, 1: pared, 2: punto, 3: power-up)
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

# Crear copia del laberinto original
original_maze = [row[:] for row in maze]


class PathFinder:
    @staticmethod
    def bfs(start, target, maze):
        """Algoritmo BFS optimizado para encontrar el camino más corto"""
        if start == target:
            return []

        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()
            x, y = current

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
                        maze[ny][nx] != 1 and next_pos not in visited):

                    visited[next_pos] = current

                    if next_pos == target:
                        # Reconstruir el camino
                        path = []
                        while next_pos != start:
                            path.append(next_pos)
                            next_pos = visited[next_pos]
                        return path[::-1]

                    queue.append(next_pos)

        return []


class Entity:
    """Clase base para Pacman y Fantasmas"""

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

        if direction == 0:  # Derecha
            next_x, next_y = grid_x + 1, grid_y
        elif direction == 1:  # Arriba
            next_x, next_y = grid_x, grid_y - 1
        elif direction == 2:  # Izquierda
            next_x, next_y = grid_x - 1, grid_y
        elif direction == 3:  # Abajo
            next_x, next_y = grid_x, grid_y + 1
        else:
            return False

        if 0 <= next_x < GRID_WIDTH and 0 <= next_y < GRID_HEIGHT:
            return maze[next_y][next_x] != 1
        return False

    def move_in_direction(self, direction):
        if direction == 0:  # Derecha
            self.x += self.speed
        elif direction == 1:  # Arriba
            self.y -= self.speed
        elif direction == 2:  # Izquierda
            self.x -= self.speed
        elif direction == 3:  # Abajo
            self.y += self.speed

        # Teletransporte entre los lados
        if self.x < -self.radius:
            self.x = WIDTH + self.radius
        elif self.x > WIDTH + self.radius:
            self.x = -self.radius


class Pacman(Entity):
    def __init__(self):
        super().__init__(13 * CELL_SIZE + CELL_SIZE // 2, 23 * CELL_SIZE + CELL_SIZE // 2)
        self.reset()
        self.lives = 3
        self.score = 0
        self.power_mode = False
        self.power_timer = 0
        self.invincible = 0
        self.pellets_eaten = 0  # Contador de puntos comidos

    def reset(self):
        self.x = 13 * CELL_SIZE + CELL_SIZE // 2
        self.y = 23 * CELL_SIZE + CELL_SIZE // 2
        self.radius = CELL_SIZE // 2 - 2
        self.speed = 3
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
            if self.direction == 0:  # Derecha
                start_angle = self.mouth_angle
                end_angle = 360 - self.mouth_angle
            elif self.direction == 1:  # Arriba
                start_angle = 90 + self.mouth_angle
                end_angle = 90 - self.mouth_angle
            elif self.direction == 2:  # Izquierda
                start_angle = 180 + self.mouth_angle
                end_angle = 180 - self.mouth_angle
            elif self.direction == 3:  # Abajo
                start_angle = 270 + self.mouth_angle
                end_angle = 270 - self.mouth_angle

            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
            pygame.draw.polygon(screen, BLACK, [
                (self.x, self.y),
                (self.x + self.radius * math.cos(math.radians(start_angle)),
                 self.y - self.radius * math.sin(math.radians(start_angle))),
                (self.x + self.radius * math.cos(math.radians(end_angle)),
                 self.y - self.radius * math.sin(math.radians(end_angle)))
            ])

        for i in range(self.lives):
            pygame.draw.circle(screen, YELLOW, (20 + i * 30, HEIGHT - 20), 10)


class Ghost(Entity):
    def __init__(self, color, x, y, ghost_type):
        super().__init__(x, y)
        self.color = color
        self.speed = 2
        self.base_speed = 2
        self.direction = random.randint(0, 3)
        self.ghost_type = ghost_type  # "blinky", "pinky", "inky", "clyde"
        self.frightened = False
        self.frightened_timer = 0
        self.eye_direction = 0
        self.current_mode = "chase"
        self.mode_timer = 0
        self.last_decision_time = 0
        self.decision_interval = 15
        self.scatter_target = self.get_scatter_corner()

    def get_scatter_corner(self):
        """Obtener la esquina de dispersión según el tipo de fantasma"""
        corners = {
            "blinky": (GRID_WIDTH - 2, 1),  # Esquina superior derecha
            "pinky": (1, 1),  # Esquina superior izquierda
            "inky": (GRID_WIDTH - 2, GRID_HEIGHT - 2),  # Esquina inferior derecha
            "clyde": (1, GRID_HEIGHT - 2)  # Esquina inferior izquierda
        }
        return corners.get(self.ghost_type, (1, 1))

    def move(self, pacman, blinky=None):
        self.update_mode()

        # Actualizar velocidad basada en puntos comidos (solo para Blinky)
        if self.ghost_type == "blinky":
            self.update_speed_based_on_pellets(pacman.pellets_eaten)

        if pacman.power_mode and not self.frightened:
            self.frightened = True
            self.frightened_timer = 300
            self.speed = 1

        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False
                self.speed = self.base_speed

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
        """Blinky se vuelve más rápido cuantos más puntos come Pacman"""
        if pellets_eaten > 50:
            self.speed = self.base_speed * 1.3  # 30% más rápido
        elif pellets_eaten > 30:
            self.speed = self.base_speed * 1.2  # 20% más rápido
        elif pellets_eaten > 10:
            self.speed = self.base_speed * 1.1  # 10% más rápido
        else:
            self.speed = self.base_speed

    def update_mode(self):
        self.mode_timer -= 1
        if self.mode_timer <= 0:
            if self.current_mode == "chase":
                self.current_mode = "scatter"
                self.mode_timer = 210
            else:
                self.current_mode = "chase"
                self.mode_timer = 420

    def move_standard(self, pacman, blinky=None):
        """Movimiento estándar para Blinky, Pinky y Clyde"""
        ghost_pos = self.get_grid_pos()

        if self.current_mode == "scatter":
            target_pos = self.scatter_target
        else:
            target_pos = self.get_chase_target(pacman, blinky)

        path = PathFinder.bfs(ghost_pos, target_pos, maze)

        if path:
            next_pos = path[0]
            self.direction = self.get_direction_to(ghost_pos, next_pos)
        else:
            self.choose_smart_direction(pacman.get_grid_pos())

    def move_inky(self, pacman, blinky):
        """Comportamiento específico de Inky - el más impredecible"""
        ghost_pos = self.get_grid_pos()
        pacman_pos = pacman.get_grid_pos()
        blinky_pos = blinky.get_grid_pos()

        if self.current_mode == "scatter":
            target_pos = self.scatter_target
        else:
            # Comportamiento complejo de Inky
            if random.random() < 0.3:  # 30% de ser errático
                # Movimiento aleatorio pero estratégico
                target_pos = self.get_erratic_target(pacman_pos)
            else:
                # Comportamiento basado en Blinky y Pacman
                target_pos = self.get_inky_target(pacman_pos, blinky_pos)

        path = PathFinder.bfs(ghost_pos, target_pos, maze)

        if path:
            next_pos = path[0]
            self.direction = self.get_direction_to(ghost_pos, next_pos)
        else:
            self.choose_smart_direction(pacman_pos)

    def get_chase_target(self, pacman, blinky=None):
        """Obtener objetivo de persecución según el tipo de fantasma"""
        pacman_pos = pacman.get_grid_pos()
        ghost_pos = self.get_grid_pos()

        if self.ghost_type == "blinky":
            # Blinky: persigue directamente a Pacman
            return pacman_pos

        elif self.ghost_type == "pinky":
            # Pinky: emboscada - 4 casillas adelante de Pacman
            return self.get_pinky_target(pacman, pacman_pos)

        elif self.ghost_type == "clyde":
            # Clyde: huye si está cerca de Pacman
            return self.get_clyde_target(pacman_pos, ghost_pos)

        else:
            return pacman_pos

    def get_pinky_target(self, pacman, pacman_pos):
        """Pinky: objetivo 4 casillas adelante de Pacman"""
        offset = 4
        if pacman.direction == 0:  # Derecha
            target = (pacman_pos[0] + offset, pacman_pos[1])
        elif pacman.direction == 1:  # Arriba
            target = (pacman_pos[0], pacman_pos[1] - offset)
        elif pacman.direction == 2:  # Izquierda
            target = (pacman_pos[0] - offset, pacman_pos[1])
        elif pacman.direction == 3:  # Abajo
            target = (pacman_pos[0], pacman_pos[1] + offset)
        else:
            target = pacman_pos

        # Asegurar que el target esté dentro del laberinto
        target = (max(1, min(GRID_WIDTH - 2, target[0])),
                  max(1, min(GRID_HEIGHT - 2, target[1])))
        return target

    def get_clyde_target(self, pacman_pos, ghost_pos):
        """Clyde: huye a su esquina si está cerca de Pacman"""
        distance = math.dist(pacman_pos, ghost_pos)

        if distance < 8:  # Menos de 8 casillas de distancia
            # Huye a su esquina
            return self.scatter_target
        else:
            # Persigue a Pacman
            return pacman_pos

    def get_inky_target(self, pacman_pos, blinky_pos):
        """Inky: objetivo complejo basado en Pacman y Blinky"""
        # Vector desde Blinky a Pacman
        vector_x = pacman_pos[0] - blinky_pos[0]
        vector_y = pacman_pos[1] - blinky_pos[1]

        # Duplicar el vector (comportamiento clásico de Inky)
        target_x = pacman_pos[0] + vector_x
        target_y = pacman_pos[1] + vector_y

        # Añadir algo de aleatoriedad para hacerlo impredecible
        target_x += random.randint(-2, 2)
        target_y += random.randint(-2, 2)

        target = (max(1, min(GRID_WIDTH - 2, target_x)),
                  max(1, min(GRID_HEIGHT - 2, target_y)))
        return target

    def get_erratic_target(self, pacman_pos):
        """Comportamiento errático para Inky"""
        if random.random() < 0.5:
            return pacman_pos
        else:
            # Objetivo aleatorio pero no demasiado lejano
            random_x = pacman_pos[0] + random.randint(-5, 5)
            random_y = pacman_pos[1] + random.randint(-5, 5)
            return (max(1, min(GRID_WIDTH - 2, random_x)),
                    max(1, min(GRID_HEIGHT - 2, random_y)))

    def get_direction_to(self, current_pos, target_pos):
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]

        if abs(dx) > abs(dy):
            return 0 if dx > 0 else 2
        else:
            return 3 if dy > 0 else 1

    def choose_smart_direction(self, pacman_pos):
        ghost_pos = self.get_grid_pos()
        possible_directions = []

        for direction in range(4):
            if self.can_move(direction) and direction != (self.direction + 2) % 4:
                possible_directions.append(direction)

        if possible_directions:
            best_direction = possible_directions[0]
            min_distance = float('inf')

            for direction in possible_directions:
                if direction == 0:
                    new_pos = (ghost_pos[0] + 1, ghost_pos[1])
                elif direction == 1:
                    new_pos = (ghost_pos[0], ghost_pos[1] - 1)
                elif direction == 2:
                    new_pos = (ghost_pos[0] - 1, ghost_pos[1])
                else:
                    new_pos = (ghost_pos[0], ghost_pos[1] + 1)

                distance = math.dist(new_pos, pacman_pos)
                if distance < min_distance:
                    min_distance = distance
                    best_direction = direction

            self.direction = best_direction

    def choose_new_direction(self, pacman, blinky):
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
            for direction in range(4):
                if self.can_move(direction):
                    self.direction = direction
                    break

    def move_frightened(self):
        possible_directions = []
        for direction in range(4):
            if self.can_move(direction) and direction != (self.direction + 2) % 4:
                possible_directions.append(direction)

        if possible_directions:
            self.direction = random.choice(possible_directions)

    def draw(self):
        color = BLUE if self.frightened else self.color

        if self.frightened and self.frightened_timer < 60:
            if (self.frightened_timer // 10) % 2 == 0:
                color = WHITE

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(screen, color,
                         (int(self.x) - self.radius, int(self.y),
                          self.radius * 2, self.radius))

        points = []
        for i in range(5):
            x_offset = -self.radius + i * (self.radius * 2) // 4
            y_offset = self.radius + (5 if i % 2 == 0 else 0)
            points.append((int(self.x) + x_offset, int(self.y) + y_offset))
        pygame.draw.polygon(screen, color, points)

        if not self.frightened:
            eye_radius = self.radius // 2
            left_eye_x = int(self.x) - eye_radius
            right_eye_x = int(self.x) + eye_radius
            eye_y = int(self.y) - eye_radius

            pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_radius)

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
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, DARK_BLUE, rect)
                pygame.draw.rect(screen, BLUE, rect.inflate(-4, -4))
            elif maze[y][x] == 2:
                pygame.draw.circle(screen, WHITE,
                                   (x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2), 3)
            elif maze[y][x] == 3:
                pygame.draw.circle(screen, WHITE,
                                   (x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2), 6)
                pygame.draw.circle(screen, YELLOW,
                                   (x * CELL_SIZE + CELL_SIZE // 2,
                                    y * CELL_SIZE + CELL_SIZE // 2), 4)


def check_collisions(pacman, ghosts):
    grid_x, grid_y = pacman.get_grid_pos()

    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        if maze[grid_y][grid_x] == 2:
            maze[grid_y][grid_x] = 0
            pacman.score += 10
            pacman.pellets_eaten += 1
        elif maze[grid_y][grid_x] == 3:
            maze[grid_y][grid_x] = 0
            pacman.score += 50
            pacman.pellets_eaten += 1
            pacman.power_mode = True
            pacman.power_timer = 300

    blinky = None
    for ghost in ghosts:
        if ghost.ghost_type == "blinky":
            blinky = ghost

    for ghost in ghosts:
        distance = math.dist((pacman.x, pacman.y), (ghost.x, ghost.y))
        if distance < pacman.radius + ghost.radius and pacman.invincible == 0:
            if ghost.frightened:
                ghost.x = 13 * CELL_SIZE + CELL_SIZE // 2
                ghost.y = 11 * CELL_SIZE + CELL_SIZE // 2
                ghost.frightened = False
                ghost.direction = random.randint(0, 3)
                pacman.score += 200
            else:
                pacman.lives -= 1
                pacman.reset()
                pacman.invincible = 120

                for g in ghosts:
                    g.x = 13 * CELL_SIZE + CELL_SIZE // 2
                    g.y = 11 * CELL_SIZE + CELL_SIZE // 2
                    g.direction = random.randint(0, 3)
                    g.frightened = False

                return True
    return False


def check_win():
    return not any(2 in row or 3 in row for row in maze)


def draw_score(pacman):
    font = pygame.font.SysFont('Arial', 24)
    score_text = font.render(f'Score: {pacman.score}', True, WHITE)
    screen.blit(score_text, (WIDTH - 200, 10))


def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont('Arial', 48)
    text = font.render('GAME OVER', True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 24))


def draw_win():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont('Arial', 48)
    text = font.render('YOU WIN!', True, YELLOW)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 24))


def reset_game():
    global maze
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
    running = True
    game_over = False
    win = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or win):
                    pacman, ghosts = reset_game()
                    game_over = win = False
                elif event.key in (pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN):
                    pacman.next_direction = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN].index(event.key)

        if not game_over and not win:
            pacman.move()

            # Obtener referencia a Blinky para Inky
            blinky = next((ghost for ghost in ghosts if ghost.ghost_type == "blinky"), None)

            for ghost in ghosts:
                if ghost.ghost_type == "inky":
                    ghost.move(pacman, blinky)
                else:
                    ghost.move(pacman)

            if check_collisions(pacman, ghosts) and pacman.lives <= 0:
                game_over = True
            elif check_win():
                win = True

        screen.fill(BLACK)
        draw_maze()
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()
        draw_score(pacman)

        if game_over:
            draw_game_over()
        elif win:
            draw_win()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()