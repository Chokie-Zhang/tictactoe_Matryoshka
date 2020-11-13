import tkinter as tk
import turtle

class Grid(object):
    def __init__(self, pos):
        self.pos = pos
        self.chess = []
        # self.init_nb()
        self.player = 9
        self.size = -1

    def ischess(self):
        if self.size != -1:
            return True
        else:
            return False

    def add_chess(self, size, player):
        if self.ischess():
            if size > self.size:
                self.chess.append((size, player))
                self.size = size
                self.player = player
                return True
            else:
                return False
        else:
            self.chess.append((size, player))
            self.size = size
            self.player = player
            return True
    
    def move_chess(self):
        self.chess = self.chess[:-1]
        if self.chess:
            self.size, self.player = self.chess[-1]
        else:
            self.size = -1
            self.player = 9

class Game(object):
    def __init__(self, l):
        self.init_grids()
        self.init_winlist()
        self.chess_status = [9] * 9
        self.len = l
        self.h = self.len * 4
        self.w = self.h * 4 / 3
        self.size_list = [0.3 * l, 0.55 * l, 0.8 * l]
        self.player_list = ['red', 'blue']
        self.playernow = 0
        self.player_write = ['红', '蓝']
        self.player_chess = [[2,2,2], [2,2,2]]
        self.undolist = []
        self.Tk = tk.Tk()
        self.cv = tk.Canvas(self.Tk, bg='white', width=self.w, height=self.h)

    def init_grids(self):
        self.grids = []
        pos_list = [(i, j) for j in list(range(-1, 2))[::-1] for i in range(-1, 2)]
        for pos in pos_list:
            self.grids.append(Grid(pos))
    
    def init_winlist(self):
        winlist1 = [[i, i+1, i+2] for i in [0, 3, 6]]
        winlist2 = [[i, i+3, i+6] for i in range(3)]
        winlist3 = [[0, 4, 8], [2, 4, 6]]
        self.winlist = winlist1 + winlist2 + winlist3

    def resetgame(self):
        self.__init__(self.len)

    def set_nextplayer(self):
        if self.playernow:
            self.playernow = 0
        else:
            self.playernow = 1
    
    def checkwin(self):
        for winadd in self.winlist:
            s = 0
            for x in winadd:
                s += self.chess_status[x]
                if s > 3:
                    break
            if s == 0:
                return 0
            elif s == 3:
                return 1
        return 2

    def chess_in(self, id_, size):
        grid = self.grids[id_]
        chess_num = self.player_chess[self.playernow][size]
        if chess_num > 0:
            if grid.add_chess(size, self.playernow):
                self.player_chess[self.playernow][size] -= 1
                self.chess_status[id_] = self.playernow
                self.undolist.append(('in', id_, size, self.playernow))
                return True
        return False

    def chess_move(self, id_, id_next):
        grid = self.grids[id_]
        grid_next = self.grids[id_next]
        if grid.ischess():
            size = grid.size
            if grid.player == self.playernow:
                if grid_next.add_chess(size, self.playernow):
                    grid.move_chess()
                    self.chess_status[id_] = grid.player
                    self.chess_status[id_next] = self.playernow
                    self.undolist.append(('move', id_, id_next, size, self.playernow))
                    return True
        return False

    def undo(self):
        if self.undolist:
            toundo = self.undolist[-1]
            if toundo[0] == 'in':
                grid = self.grids[toundo[1]]
                grid.move_chess()
                self.chess_status[toundo[1]] = grid.player
                self.player_chess[toundo[3]][toundo[2]] += 1
            else:
                grid_next = self.grids[toundo[2]]
                grid = self.grids[toundo[1]]
                grid_next.move_chess()
                grid.add_chess(toundo[3], toundo[4])
                self.chess_status[toundo[1]] = grid.player
                self.chess_status[toundo[2]] = grid_next.player
            self.undolist = self.undolist[:-1]
            return True
        else:
            return False

    # def draw_bell(self):
    #     x1, y1 = (self.w - self.len * 3) / 2, (self.h - self.len * 3) / 2
    #     x2, y2 = x1 + self.len * 3, y1 + self.len * 3
    #     for i in range(1, 3):
    #         self.cv.create_line(x1, y1 + self.len * i, x2, y1 + self.len * i)
    #         self.cv.create_line(x1 + self.len * i, y1, x1 + self.len * i, y2)

    def draw_bell(self):
        start_point = [(-1.5, 0.5, 0), (-1.5, -0.5, 0), (-0.5, -1.5, 90), (0.5, -1.5, 90)]
        for x, y, angle in start_point:
            turtle.penup()
            turtle.goto(x * self.len, y * self.len)
            turtle.setheading(angle)
            turtle.pendown()
            turtle.forward(3 * self.len)
        turtle.penup()

    def draw_circle(self, id_):
        grid = self.grids[id_]
        

    def draw_circle(self, id_):
        grid = self.grids[id_]
        if grid.ischess():
            size, player = grid.chess[-1]
            x, y = grid.pos
            x = x * self.len
            y = y * self.len
            turtle.goto(x, y)
            turtle.dot(self.size_list[size], self.player_list[player])

    def drawthegame(self):
        turtle.reset()
        turtle.hideturtle()
        turtle.speed(1000)
        self.draw_bell()
        for id_ in range(9):
            self.draw_circle(id_)
        turtle.goto(0, self.len / 2.5 * 5)
        turtle.write(self.player_write[self.playernow] + '方', align='center', font=("Arial", 40))
        turtle.goto(0, self.len / 3 * 5)
        s, m, b = self.player_chess[self.playernow]
        turtle.write('剩余棋子数为：小-%d, 中-%d, 大-%d' % (s, m, b), align='center', font=("Arial", 30))
        
        
        

def in_chess(flag=1):
    while True:
        id_ = input('请输入棋子放置的位置，请输入1-9其中一位数字' + '(q-返回上一步)' * flag + '：').strip()
        if id_ in [str(i) for i in range(1, 10)]:
            while True:
                size = input('请输入选用的棋子(1-小 / 2-中 / 3-大 / q-返回上一步)：').strip()
                if size in ['1', '2', '3']:
                    return int(id_) - 1, int(size) - 1
                elif size == 'q':
                    break
                else:
                    print('输入有误。')
        elif id_ == 'q' and flag:
            return (-1, -1)
        else:
            print('输入有误。')

def mov_chess(flag=1):
    while True:
        id_ = input('请输入想移动的棋子，请输入1-9其中一位数字' + '(q-返回上一步)' * flag + '：').strip()
        if id_ in [str(i) for i in range(1, 10)]:
            while True:
                id_next = input('请输入想移动到的位置(q-返回上一步)：').strip()
                if id_next in [str(i) for i in range(1, 10)]:
                    return int(id_) - 1, int(id_next) - 1
                elif id_next == 'q':
                    break
        elif id_ == 'q' and flag:
            return (-1, -1)
        else:
            print('输入有误。')

def main():
    game = Game(150)
    flag = 1
    while flag:
        try:
            game.drawthegame()
            if not game.playernow in game.chess_status:
                if game.undolist:
                    while True:
                        q = input('请输入下棋的方式(1-下棋 / 3-让对方悔棋)：').strip()
                        if q == '1':
                            id_, size = in_chess(1)
                            if id_ < 0:
                                continue
                            if game.chess_in(id_, size):
                                break
                            else:
                                print('下棋有误，请考虑棋的大小以及是否有棋。')
                                continue
                        elif q == '3':
                            game.undo()
                            break
                        else:
                            print('输入有误。')
                else:
                    id_, size = in_chess(0)
                    game.chess_in(id_, size)
            else:
                while True:
                    q = input('请输入下棋的方式(1-下棋 / 2-移棋 / 3-让对方悔棋)：').strip()
                    if q == '1':
                        id_, size = in_chess()
                        if id_ < 0:
                            continue
                        if game.chess_in(id_, size):
                            break
                        else:
                            print('下棋有误，请考虑棋的大小以及是否有棋。')
                            continue
                    elif q == '2':
                        id_, id_next = mov_chess()
                        if id_ < 0:
                            continue
                        if game.chess_move(id_, id_next):
                            break
                        else:
                            print('移棋有误，请考虑好棋的大小。')
                            continue
                    elif q == '3':
                        game.undo()
                        break
                    else:
                        print('输入有误。')
            print(game.undolist)
            if game.checkwin() != 2:
                game.drawthegame()
                turtle.goto(0, 250)
                if game.checkwin():
                    turtle.write('Blue win!', align='center', font=("Arial", 100))
                else:
                    turtle.write('Red win!', align='center', font=("Arial", 100))
                almostwin = input('游戏结束，是否返回上一步(1-返回)：')
                if almostwin == '1':
                    game.undo()
                else:
                    while True:
                        q = input('重新玩吗(0-退出 / 1-继续)？').strip()
                        if q == '0':
                            flag = 0
                            break
                        elif q == '1':
                            game.resetgame()
                            break
                        else:
                            print('输出有误，请重新输入。')
            else:
                game.set_nextplayer()
        except KeyboardInterrupt:
            game.resetgame()
        
if __name__ == '__main__':
    # main()
    game = Game(150)
    game.draw_bell()

