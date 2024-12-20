from random import choice, randint
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

directions = [UP, DOWN, LEFT, RIGHT]

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Основной класс, который служит базой для всех объектов в игре."""

    def __init__(self, position=None):
        """Инициализирует объект с базовыми атрибутами."""
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = position
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для управления яблоком в игре."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока с выбором цвета и позиции."""
        super().__init__(None)
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает яблоко в случайное место на игровом поле."""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self):
        """Отображает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для управления змейкой и её поведением."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Настраивает стартовое состояние змейки."""
        super().__init__(None)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.body_color = body_color
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на новое место на игровом поле."""
        head = list(self.get_head_position())
        head[0] = (head[0] + GRID_SIZE * self.direction[0]) % SCREEN_WIDTH
        head[1] = (head[1] + GRID_SIZE * self.direction[1]) % SCREEN_HEIGHT
        if head[0] < 0:
            head[0] = SCREEN_WIDTH - GRID_SIZE
        if head[1] < 0:
            head[1] = SCREEN_HEIGHT - GRID_SIZE
        head = tuple(head)
        self.positions.insert(0, head)
        self.positions.pop()
        if len(self.positions) > 4 and head in self.positions[1:]:
            self.reset()

    def draw(self):
        """Рисует змейку с её телом и головой."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает параметры змейки до начальных значений."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice(directions)


def handle_keys(game_object):
    """Обрабатывает события нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры, управляющий процессом."""
    pygame.init()
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(SPEED + snake.length)
        handle_keys(snake)
        snake.update_direction()
        if snake.length == 1:
            head = snake.get_head_position()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.positions.insert(0, apple.position)
            if snake.length == 1:
                snake.positions.insert(1, head)
            snake.length += 1
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
