import sys
import random

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Board(QFrame):
    def __init__(self, parent, windowWidth, windowHeight):
        super(Board, self).__init__(parent)
        self.SPEED = 100
        self.WIDTHINBLOCKS = int(windowWidth/10)
        self.HEIGHTINBLOCKS = int(windowHeight/10)
        self.timer = QBasicTimer()
        self.snake = [[5, 10], [5, 11]]
        self.current_x_head = self.snake[0][0]
        self.current_y_head = self.snake[0][1]
        self.food = []
        self.grow_snake = False
        self.board = []
        self.direction = 1
        self.drop_food()
        self.setFocusPolicy(Qt.StrongFocus)

    def square_width(self):
        return self.contentsRect().width() / self.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / self.HEIGHTINBLOCKS

    def start(self):
        self.timer.start(self.SPEED, self)

    def paintEvent(self, _):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = rect.bottom() - self.HEIGHTINBLOCKS * self.square_height()

        for pos in self.snake:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())
        for pos in self.food:
            self.draw_square(painter, rect.left() + pos[0] * self.square_width(),
                             boardtop + pos[1] * self.square_height())

    def draw_square(self, painter, x, y):
        color = QColor(0xFFFFFF)
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Left:
            if self.direction != 2:
                self.direction = 1
        elif key == Qt.Key_Right:
            if self.direction != 1:
                self.direction = 2
        elif key == Qt.Key_Down:
            if self.direction != 4:
                self.direction = 3
        elif key == Qt.Key_Up:
            if self.direction != 3:
                self.direction = 4

    def move_snake(self):
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            if self.current_x_head < 0:
                self.current_x_head = self.WIDTHINBLOCKS - 1
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            if self.current_x_head == self.WIDTHINBLOCKS:
                self.current_x_head = 0
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            if self.current_y_head == self.HEIGHTINBLOCKS:
                self.current_y_head = 0
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            if self.current_y_head < 0:
                self.current_y_head = self.HEIGHTINBLOCKS

        head = [self.current_x_head, self.current_y_head]
        self.snake.insert(0, head)
        if not self.grow_snake:
            self.snake.pop()
        else:
            self.grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
            self.is_food_collision()
            self.is_suicide()
            self.update()

    def is_suicide(self):
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.timer.stop()
                self.snake = [[5, 10], [5, 11]]
                self.current_x_head = self.snake[0][0]
                self.current_y_head = self.snake[0][1]
                self.food = []
                self.board = []
                self.direction = 1
                self.drop_food()
                self.SPEED = 100
                break
        self.start()

    def is_food_collision(self):
        for pos in self.food:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.drop_food()
                self.grow_snake = True
                self.SPEED -= 1

    def drop_food(self):
        x = random.randint(3, self.WIDTHINBLOCKS-2)
        y = random.randint(3, self.HEIGHTINBLOCKS-2)
        for pos in self.snake:
            if pos == [x, y]:
                self.drop_food()
        self.food.append([x, y])


def main():
    app = QApplication([])
    _ = SnakeGame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
