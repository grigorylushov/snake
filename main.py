from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import random

# Размеры сетки
GRID_SIZE = 20
CELL_SIZE = 20

class SnakeHead(Widget):
    pass

class SnakeSegment(Widget):
    pass

class Food(Widget):
    pass

class SnakeGame(Widget):
    snake = ObjectProperty(None)
    food = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake_body = []
        self.direction = Vector(0, -1)
        self.next_direction = Vector(0, -1)
        self.score = 0
        self.game_over = False
        self.speed = 0.15
        self.init_game()
        
    def init_game(self):
        # Начальная змейка из 3 сегментов
        self.snake_body = []
        start_x = self.width // 2 // CELL_SIZE * CELL_SIZE
        start_y = self.height // 2 // CELL_SIZE * CELL_SIZE
        
        for i in range(3):
            segment = SnakeSegment()
            segment.size = (CELL_SIZE, CELL_SIZE)
            segment.pos = (start_x + i * CELL_SIZE, start_y)
            self.add_widget(segment)
            self.snake_body.append(segment)
        
        # Голова (первый сегмент)
        self.snake = self.snake_body[0]
        self.snake.size = (CELL_SIZE, CELL_SIZE)
        
        # Еда
        self.food = Food()
        self.food.size = (CELL_SIZE, CELL_SIZE)
        self.spawn_food()
        self.add_widget(self.food)
        
        self.game_over = False
        self.score = 0
        self.direction = Vector(0, -1)
        self.next_direction = Vector(0, -1)
        
        # Запуск таймера
        Clock.schedule_interval(self.update, self.speed)
        
        # Привязка клавиш
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.next_direction = Vector(0, 1)
        elif keycode[1] == 'down':
            self.next_direction = Vector(0, -1)
        elif keycode[1] == 'left':
            self.next_direction = Vector(-1, 0)
        elif keycode[1] == 'right':
            self.next_direction = Vector(1, 0)
        elif keycode[1] == 'spacebar' and self.game_over:
            self.restart()
        return True
        
    def spawn_food(self):
        # Поиск свободной клетки
        while True:
            x = random.randint(0, (self.width // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (self.height // CELL_SIZE) - 1) * CELL_SIZE
            self.food.pos = (x, y)
            # Проверка, что еда не появилась внутри змейки
            collision = False
            for segment in self.snake_body:
                if segment.collide_widget(self.food):
                    collision = True
                    break
            if not collision:
                break
                
    def update(self, dt):
        if self.game_over:
            return
            
        # Обновление направления
        if self.next_direction != self.direction * -1:
            self.direction = self.next_direction
            
        # Новая позиция головы
        new_head_pos = self.snake.pos + self.direction * CELL_SIZE
        
        # Проверка столкновения с едой
        if self.food.collide_point(new_head_pos[0] + CELL_SIZE/2, new_head_pos[1] + CELL_SIZE/2):
            self.grow()
            self.spawn_food()
            self.score += 1
            # Увеличение скорости
            if self.speed > 0.08:
                self.speed -= 0.005
                Clock.unschedule(self.update)
                Clock.schedule_interval(self.update, self.speed)
        
        # Движение змейки
        head = self.snake_body[0]
        head.pos = new_head_pos
        
        # Движение остальных сегментов
        for i in range(1, len(self.snake_body)):
            prev = self.snake_body[i-1]
            current = self.snake_body[i]
            # Сохраняем старую позицию предыдущего сегмента
            current.pos = prev.pos - self.direction * CELL_SIZE
        
        # Проверка столкновения с границами
        if (head.x < 0 or head.x >= self.width or 
            head.y < 0 or head.y >= self.height):
            self.game_over = True
            self.show_game_over()
            return
            
        # Проверка столкновения с собой (кроме головы)
        for segment in self.snake_body[1:]:
            if head.collide_widget(segment):
                self.game_over = True
                self.show_game_over()
                return
                
    def grow(self):
        # Добавление нового сегмента в конец
        last = self.snake_body[-1]
        new_segment = SnakeSegment()
        new_segment.size = (CELL_SIZE, CELL_SIZE)
        new_segment.pos = (last.x, last.y)
        self.add_widget(new_segment)
        self.snake_body.append(new_segment)
        
    def show_game_over(self):
        from kivy.uix.label import Label
        self.game_over_label = Label(
            text=f"Game Over!\nScore: {self.score}\nPress SPACE to restart",
            font_size='24sp',
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.game_over_label)
        
    def restart(self):
        # Очистка
        for segment in self.snake_body:
            self.remove_widget(segment)
        self.snake_body.clear()
        self.remove_widget(self.game_over_label)
        self.remove_widget(self.food)
        
        self.init_game()


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game
        
    def on_start(self):
        Window.size = (400, 600)


if __name__ == '__main__':
    SnakeApp().run()        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    # Начальное направление (вправо)
    key = curses.KEY_RIGHT

    # Генерация еды
    def create_food():
        while True:
            fy = random.randint(1, game_height - 2)
            fx = random.randint(1, game_width - 2)
            if [fy, fx] not in snake:
                return [fy, fx]

    food = create_food()
    score = 0

    while True:
        stdscr.clear()
        
        # Инструкция и счет
        stdscr.addstr(0, 1, f"Счет: {score} | Выход: Q")
        
        # Рисуем рамку вокруг игрового поля
        win.box()

        # Отрисовка еды
        win.addch(food[0], food[1], '*')

        # Отрисовка змейки
        for i, head in enumerate(snake):
            char = 'O' if i == 0 else 'o'
            win.addch(head[0], head[1], char)

        # Отрисовка элементов управления для удобства на телефоне
        controls_y = game_height + 2
        if controls_y + 2 < max_y:
            stdscr.addstr(controls_y, 1, "   [W/↑]   ")
            stdscr.addstr(controls_y + 1, 1, "[A/←] [S/↓] [D/→]")

        stdscr.refresh()
        win.refresh()

        # Считываем ввод пользователя
        next_key = win.getch()

        # Преобразуем буквы WASD в соответствующие направления
        if next_key in [ord('w'), ord('W')]:
            next_key = curses.KEY_UP
        elif next_key in [ord('s'), ord('S')]:
            next_key = curses.KEY_DOWN
        elif next_key in [ord('a'), ord('A')]:
            next_key = curses.KEY_LEFT
        elif next_key in [ord('d'), ord('D')]:
            next_key = curses.KEY_RIGHT

        # Проверка на выход из игры
        if next_key in [ord('q'), ord('Q')]:
            break

        # Запрещаем разворот на 180 градусов
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (next_key == curses.KEY_UP and key != curses.KEY_DOWN) or \
               (next_key == curses.KEY_DOWN and key != curses.KEY_UP) or \
               (next_key == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
               (next_key == curses.KEY_RIGHT and key != curses.KEY_LEFT):
                key = next_key

        # Вычисляем новую позицию головы
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1

        # Проверка столкновения со стенами
        if (new_head[0] == 0 or new_head[0] == game_height - 1 or
                new_head[1] == 0 or new_head[1] == game_width - 1):
            break

        # Проверка столкновения с собственным хвостом
        if new_head in snake:
            break

        # Вставляем новую голову
        snake.insert(0, new_head)

        # Проверка поедания еды
        if new_head == food:
            score += 10
            food = create_food()
        else:
            # Если еду не съели, удаляем хвост
            snake.pop()

    # Сообщение о проигрыше
    stdscr.clear()
    stdscr.addstr(max_y // 2, max_x // 2 - 5, "GAME OVER")
    stdscr.addstr(max_y // 2 + 1, max_x // 2 - 8, f"Итоговый счет: {score}")
    stdscr.refresh()
    time.sleep(2)

if __name__ == "__main__":
    curses.wrapper(main)
