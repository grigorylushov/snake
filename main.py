import curses
import random
import time

def main(stdscr):
    # Отключаем отображение курсора
    curses.curs_set(0)
    
    # Делаем getch() неблокирующим (не ждет нажатия клавиши)
    stdscr.nodelay(True)
    
    # Устанавливаем таймаут ввода в миллисекундах
    stdscr.timeout(100)

    # Получаем размеры экрана Termux
    max_y, max_x = stdscr.getmaxyx()

    # Размеры игрового поля
    game_height = min(18, max_y - 6)
    game_width = min(36, max_x - 4)

    if game_height < 8 or game_width < 12:
        stdscr.addstr(0, 0, "Экран слишком мал! Увеличьте шрифт или размер окна Termux.")
        stdscr.refresh()
        time.sleep(3)
        return

    # Создаем окно для игры
    win = curses.newwin(game_height, game_width, 1, 1)
    win.keypad(True)
    win.nodelay(True)

    # Начальные координаты змейки
    snake_y = game_height // 2
    snake_x = game_width // 4
    snake = [
        [snake_y, snake_x],
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
