import tkinter as tk
import turtle

class Chess(object):
    def __init__(self, player, size):
        self.player = player
        self.size = size
        self.cbc = 1
        self.ingrid = str(self.player + self.size * 2)
    
    def reset(self):
        self.__init__(self.player, self.size)
    
    def set_pos(self, pos):
        self.pos = pos
    
    def set_ingrid(self, grid_ix):
        self.ingrid = grid_ix

    def change_cbc(self):
        if self.cbc:
            self.cbc = 0
        else:
            self.cbc = 1

    def set_button(self, button):
        self.button = button
    
    def move_to(self, to, cv, m):
        x_change = to[0] - self.pos[0]
        y_change = to[1] - self.pos[1]
        cv.move(self.button, x_change*m, y_change*m)
        cv.lift(self.button)
        self.set_pos(to)

class Grid(object):
    def __init__(self, pos, type_):
        self.pos = pos
        self.chess = []
        # type为1表示棋盘的grid，0表示剩余棋子的"grid"
        self.type = type_ 
        self.begin_chess = []
        # self.init_nb()
        # self.player = 9
        # self.size = -1

    def reset(self):
        self.chess = self.begin_chess[:]

    def ischess(self):
        if self.chess:
            return True
        else:
            return False

    # 往棋盘里添加棋子
    def add_chess(self, chess):
        if self.chess and self.type:
            if chess.size > self.chess[-1].size:
                self.chess[-1].change_cbc()
                self.chess.append(chess)
            # if size > self.size:
            #     self.chess.append((size, player))
            #     self.size = size
            #     self.player = player
                return True
            else:
                return False
        else:
            self.chess.append(chess)
            # self.chess.append((size, player))
            # self.size = size
            # self.player = player
            return True
    
    # 从棋盘中拿走棋子
    def move_chess(self):
        if self.chess:
            self.chess = self.chess[:-1]
            if self.chess and self.type:
                self.chess[-1].change_cbc()
        # if self.chess:
        #     self.size, self.player = self.chess[-1]
        # else:
        #     self.size = -1
        #     self.player = 9
            return True
        else:
            return False

class Game(object):
    def __init__(self, m=100):
        self.init_grids()
        self.init_winlist()
        # 小中大的棋子数
        self.chess_default = (2,2,2)
        self.size_list = [0.2, 0.38, 0.56]
        self.init_chess()
        # self.chess_status = [9] * 9
        self.m = m
        self.h = self.m * 6
        self.w = self.m * 8
        self.game_stat = 1
        self.win_stat = ['红方胜利！','蓝方胜利！','Draw Game！']
        self.player_list = ['red', 'blue']
        self.playernow = 0
        self.player_write = ['红', '蓝']
        self.type_list = ['小', '中', '大']
        # self.player_chess = [[2] * 3, [2] * 3]
        self.undolist = []
        self.Tk = tk.Tk()
        self.cv = tk.Canvas(self.Tk, bg='white', width=self.w, height=self.h)
        self.hint = tk.Label(self.Tk, text="q键返回上一步，r键重新开始", font=("楷体", 20))
        self.label_text = tk.StringVar(value='游戏开始！请红方单击选取你想移动的棋子。')
        self.label = tk.Label(self.Tk, textvariable=self.label_text, font=("楷体", 20))
        self.label.pack(side="top")
        self.hint.pack(side="bottom")
        self.draw_bell()
        self.draw_chess()

    def init_grids(self):
        self.grids = []
        pos_list = [(i * 4 / 3 + 4, j * 4 / 3 + 3) for j in range(-1, 2) for i in range(-1, 2)]
        for pos in pos_list:
            self.grids.append(Grid(pos, type_=1))
    
    def init_chess(self):
        self.chess = {0:[], 1:[]}
        # 剩余棋子的“格子”
        self.rest_grids = [] 
        # self.first_pos = {0:[], 1:[]}
        sp = 1
        for i, num in enumerate(self.chess_default):
            size = self.size_list[i]
            fps = [(2 / 3, sp + size), (8 - 2 / 3, sp + size)]
            for j in range(2):
                rest_grid = Grid(fps[j], type_=0)
                for _ in range(num):
                    # self.first_pos[j].append(fps[j])
                    chess = Chess(j, i)
                    chess.set_pos(fps[j])
                    rest_grid.chess.append(chess)
                    rest_grid.begin_chess.append(chess)
                    self.chess[j].append(chess)
                self.rest_grids.append(rest_grid)
            sp += 0.86 + self.size_list[self.chess[0][-1].size] * 2
    
    def init_winlist(self):
        winlist1 = [[i, i+1, i+2] for i in [0, 3, 6]]
        winlist2 = [[i, i+3, i+6] for i in range(3)]
        winlist3 = [[0, 4, 8], [2, 4, 6]]
        self.winlist = winlist1 + winlist2 + winlist3

    def check_win(self):
        red_point = 0
        blue_point = 0
        for winlist in self.winlist:
            wholist = []
            for grid_ix in winlist:
                grid = self.grids[grid_ix]
                if grid.ischess():
                    wholist.append(grid.chess[-1].player)
            if len(wholist) == 3:
                if sum(wholist) == 0:
                    red_point += 1
                elif sum(wholist) == 3:
                    blue_point += 1
        if red_point > 0:
            if blue_point > 0:
                return 2
            else:
                return 0
        else:
            if blue_point > 0:
                return 1
            else:
                return -1

    # 重启游戏
    def resetgame(self):
        # self.__init__(self.m)
        for grid in self.grids:
            grid.reset()
        for i in range(2):
            for j, chess in enumerate(self.chess[i]):
                chess.reset()
                ingrid = int(chess.ingrid)
                x_reset, y_reset = self.rest_grids[ingrid].pos
                chess.move_to((x_reset,y_reset), self.cv, self.m)
        self.playernow = 0
        self.cv.itemconfig(self.show_now, text='红方', fill='red')
        self.label_text.set('游戏开始！请红方单击选取你想移动的棋子。')
        for i, rest_grid in enumerate(self.rest_grids):
            rest_grid.reset()
            btn = self.rest_button[i]
            self.cv.itemconfig(btn, text=str(len(rest_grid.chess)))
            self.cv.lift(btn)

    # 下一位玩家
    def set_nextplayer(self):
        if self.playernow:
            self.playernow = 0
        else:
            self.playernow = 1
        if self.game_stat:
            next_write = self.player_write[self.playernow]
            next_fill = self.player_list[self.playernow]
            self.label_text.set('到%s方行动，请%s方单击选取你想移动的棋子。' % (next_write, next_write))
            self.cv.itemconfig(self.show_now, text='%s方' % next_write, fill=next_fill)

    # 撤回
    def undo(self):
        if self.undolist:
            self.game_stat = 1
            chess, last_ingrid = self.undolist[-1]
            ingrid = chess.ingrid
            grid = self.grids[ingrid]
            if type(last_ingrid) == int:
                last_grid = self.grids[last_ingrid]
            else:
                last_grid = self.rest_grids[int(last_ingrid)]
                button = self.rest_button[int(last_ingrid)]
            to = last_grid.pos
            grid.move_chess()
            last_grid.add_chess(chess)
            chess.move_to(to, self.cv, self.m)
            chess.set_ingrid(last_ingrid)
            if type(last_ingrid) == str:
                self.cv.itemconfig(button, text=str(len(last_grid.chess)))
                self.cv.lift(button)
            self.set_nextplayer()
            self.undolist = self.undolist[:-1]

    # 画棋盘
    def draw_bell(self):
        x1, y1 = 2, 1
        x2, y2 = 6, 1
        x3, y3 = 2, 5
        m = self.m
        for i in range(4):
            self.cv.create_line(x1 * m, (y1 + i * 4 / 3) * m, x2 * m, (y2 + i * 4 / 3) * m)
            self.cv.create_line((x1 + i * 4 / 3) * m, y1 * m, (x3 + i * 4 / 3) * m, y3 * m)
    
    # 画初始的棋子并记录各类参数
    def draw_chess(self):
        m = self.m
        # 剩余棋子数文本的button
        self.rest_button = []
        for i in range(2):
            for chess in self.chess[i]:
                r = self.size_list[chess.size]
                x1, y1 = ((i-r) * m for i in chess.pos)
                x2, y2 = ((i+r) * m for i in chess.pos)
                chess.set_button(self.cv.create_oval(x1, y1, x2, y2, fill=self.player_list[chess.player]))
        # 画初始棋子数
        for rest_grid in self.rest_grids:
            x, y = rest_grid.pos
            num = len(rest_grid.chess)
            temp = self.cv.create_text(x * self.m, y * self.m, text=str(num), font=('楷体', 20))
            self.rest_button.append(temp)
            # 在没有棋子的时候就不再标注0
            if num == 0:
                self.cv.itemconfig(temp, text='')
        # 显示目前的行动方
        self.show_now = self.cv.create_text(4 * self.m, 0.5 * self.m, text="红方", font=('微软雅黑', 35), fill='red')

    def play(self):
        self.chosen = 0
        def cancle(event):
            self.chosen = 0
            self.label_text.set('请选择棋子。')
        def choose(event):
            if self.game_stat:
                player = self.playernow
                x, y = event.x / self.m, event.y / self.m
                if not self.chosen:
                    for i, chess in enumerate(self.chess[player]):
                        if chess.cbc:
                            if (x - chess.pos[0]) ** 2 + (y - chess.pos[1]) ** 2 < self.size_list[chess.size] ** 2:
                                self.chosen = i + 1
                                self.label_text.set('你选中了%s棋子，请选择移动的地点，按右键取消选取。' % self.type_list[chess.size])
                                break
                else:
                    chosen_chess = self.chess[player][self.chosen-1]
                    x_ori, y_ori = chosen_chess.pos
                    x_pos, y_pos = -1, -1
                    for i in range(3):
                        if 2 + i * 4 / 3 < x < 2 + (i+1) * 4 / 3:
                            x_pos = i
                        if 1 + i * 4 / 3 < y < 1 + (i+1) * 4 / 3:
                            y_pos = i
                    if x_pos == -1 or y_pos == -1:
                        self.label_text.set('移动地点有误，请重新选择地点，按右键更换棋子。')
                    else:
                        grid_ix = 3 * y_pos + x_pos
                        grid = self.grids[3 * y_pos + x_pos]
                        x_next, y_next = grid.pos
                        if grid.add_chess(chosen_chess):
                            chosen_chess.move_to((x_next,y_next), self.cv, self.m)
                            ingrid = chosen_chess.ingrid
                            self.undolist.append([chosen_chess, ingrid])
                            if type(ingrid) == int:
                                self.grids[ingrid].move_chess()
                            else:
                                rest_grid = self.rest_grids[int(ingrid)]
                                rest_grid.move_chess()
                                rn = len(rest_grid.chess)
                                rn_btn = self.rest_button[int(ingrid)]
                                if rn:
                                    self.cv.itemconfig(rn_btn, text=str(rn))
                                else:
                                    self.cv.itemconfig(rn_btn, text='')
                            chosen_chess.set_ingrid(grid_ix)
                            check_win = self.check_win()
                            if check_win != -1:
                                self.cv.itemconfig(self.show_now, text=self.win_stat[check_win])
                                self.game_stat = 0
                                self.label_text.set('游戏结束！请按q返回上一步或按r重新开始。')
                            self.set_nextplayer()
                            self.chosen = 0
                        else:
                            self.label_text.set('移动地点有误，请重新选择地点，按右键更换棋子。')
        # 左键选择，右键取消，q键返回上一步，r键重新开始
        self.cv.bind('<ButtonRelease-1>', choose)
        self.cv.bind('<ButtonRelease-3>', cancle)
        self.cv.bind_all('<Key-q>', lambda e: self.undo())
        self.cv.bind_all('<Key-r>', lambda e: self.resetgame())
        self.cv.pack()
        self.Tk.mainloop()

if __name__ == '__main__':
    game = Game(120)
    game.play()