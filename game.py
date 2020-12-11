import tkinter as tk
import turtle

class Chess(object):
    def __init__(self, player, size, pos, button):
        self.player = player
        self.size = size
        self.cbc = 1
        self.ingrid = str(self.player * 3 + self.size)
        self.begin_pos = pos
        self.pos = pos
        self.button = button

    def reset(self):
        self.__init__(self.player, self.size, self.begin_pos, self.button)

    def set_pos(self, pos):
        self.pos = pos
    
    def set_ingrid(self, grid_ix):
        self.ingrid = grid_ix

    def change_cbc(self):
        self.cbc = 1 - self.cbc

# 放初始棋子的地方
class Chess_bag(object):
    def __init__(self, pos, chess, button):
        self.pos = pos
        self.chess = chess
        self.begin_chess = chess[:]
        self.button = button
    
    def reset(self):
        self.chess = self.begin_chess[:]
    
    def ischess(self):
        return bool(self.chess)
    
    def add_chess(self, chess):
        self.chess.append(chess)
        return True
    
    def move_chess(self):
        if self.ischess():
            self.chess = self.chess[:-1]

# 棋盘的格子
class Grid(object):
    def __init__(self, pos):
        self.pos = pos
        self.chess = []
        self.player = -1

    def reset(self):
        self.chess = []

    def ischess(self):
        return bool(self.chess)

    # 往棋盘里添加棋子
    def add_chess(self, chess):
        if self.ischess():
            if chess.size > self.chess[-1].size:
                self.chess[-1].change_cbc()
                self.chess.append(chess)
                self.player = chess.player
                return True
            else:
                return False
        else:
            self.chess.append(chess)
            self.player = chess.player
            return True
    
    # 从棋盘中拿走棋子
    def move_chess(self):
        if self.chess:
            self.chess = self.chess[:-1]
            if self.chess:
                self.chess[-1].change_cbc()
                self.player = self.chess[-1].player
            else:
                self.player = -1

class Game(object):
    # m为放大的倍数（默认的100为800x600的窗口大小，50为400x300）
    def __init__(self, m=100):
        # 一些常量
        self.win_stat = ['红方胜利！','蓝方胜利！','Draw Game！']
        self.player_list = ['red', 'blue']
        self.player_write = ['红', '蓝']
        self.type_list = ['小', '中', '大']
        self.m = m
        self.h = self.m * 6
        self.w = self.m * 8
        # 初始化图形界面
        self.Tk = tk.Tk()
        self.cv = tk.Canvas(self.Tk, bg='white', width=self.w, height=self.h)
        # 显示目前的行动方
        self.show_now = self.cv.create_text(4 * self.m, 0.5 * self.m, text="红方", font=('微软雅黑', 35), fill='red')
        self.hint = tk.Label(self.Tk, text="q键返回上一步，r键重新开始", font=("楷体", 20))
        self.label_text = tk.StringVar(value='游戏开始！请红方单击选取你想移动的棋子。')
        self.label = tk.Label(self.Tk, textvariable=self.label_text, font=("楷体", 20))
        self.label.pack(side="top")
        self.hint.pack(side="bottom")
        # 初始化棋盘，棋子
        self.init_grids()
        self.init_winlist()
        # 小中大的棋子数
        self.chess_default = (2,2,2)
        self.size_list = [0.2, 0.38, 0.56]
        self.init_chess()
        self.playernow = 0
        self.game_stat = 1
        self.undolist = []

    # 初始化棋盘格子并画棋盘
    def init_grids(self):
        self.grids = []
        pos_list = [(i * 4 / 3 + 4, j * 4 / 3 + 3) for j in range(-1, 2) for i in range(-1, 2)]
        for pos in pos_list:
            self.grids.append(Grid(pos))
        x1, y1 = 2, 1
        x2, y2 = 6, 1
        x3, y3 = 2, 5
        m = self.m
        for i in range(4):
            self.cv.create_line(x1 * m, (y1 + i * 4 / 3) * m, x2 * m, (y2 + i * 4 / 3) * m)
            self.cv.create_line((x1 + i * 4 / 3) * m, y1 * m, (x3 + i * 4 / 3) * m, y3 * m)
    
    # 初始化棋子并画棋子
    def init_chess(self):
        self.chess = [[], []]
        # 剩余棋子
        self.chess_bags = []
        m = self.m
        for j in range(2):
            sp = 1
            for i, num in enumerate(self.chess_default):
                size = self.size_list[i]
                # 棋子的初始位置
                fps = [(2 / 3, sp + size), (8 - 2 / 3, sp + size)]
                chesses = []
                for _ in range(num):
                    x1, y1 = ((i-size) * m for i in fps[j])
                    x2, y2 = ((i+size) * m for i in fps[j])
                    chess_button = self.cv.create_oval(x1, y1, x2, y2, fill=self.player_list[j])
                    chess = Chess(j, i, fps[j], chess_button)
                    chesses.append(chess)
                self.chess[j] += chesses
                x, y = fps[j]
                # 在没有棋子的时候就不标注
                text_ = str(num) if num else ''
                bag_button = self.cv.create_text(x * m, y * m, text=text_, font=('楷体', 20))
                self.chess_bags.append(Chess_bag(fps[j], chesses, bag_button))
                sp += 0.86 + self.size_list[self.chess[0][i+1].size] * 2

    # 行列斜的胜利条件
    def init_winlist(self):
        winlist1 = [[i, i+1, i+2] for i in [0, 3, 6]]
        winlist2 = [[i, i+3, i+6] for i in range(3)]
        winlist3 = [[0, 4, 8], [2, 4, 6]]
        self.winlist = winlist1 + winlist2 + winlist3

    # 检查游戏是否出现胜者
    def check_win(self):
        red_point = 0
        blue_point = 0
        wholist = [grid.player for grid in self.grids]
        for winlist in self.winlist:
            whostat = [wholist[i] for i in winlist]
            if not -1 in whostat:
                if sum(whostat) == 0:
                    red_point += 1
                elif sum(whostat) == 3:
                    blue_point += 1
        win_matrix = [[-1, 1], [0, 2]]
        return win_matrix[red_point][blue_point]

    # 重启游戏
    def resetgame(self):
        for grid in self.grids:
            grid.reset()
        for i in range(2):
            for j, chess in enumerate(self.chess[i]):
                self.move_chess_gui(chess, chess.begin_pos)
                chess.reset()
        self.playernow = 0
        self.cv.itemconfig(self.show_now, text='红方', fill='red')
        self.label_text.set('游戏开始！请红方单击选取你想移动的棋子。')
        for i, chess_bag in enumerate(self.chess_bags):
            chess_bag.reset()
            btn = chess_bag.button
            self.cv.itemconfig(btn, text=str(len(chess_bag.chess)))
            self.cv.lift(btn)

    # 下一位玩家
    def set_nextplayer(self):
        self.playernow = 1 - self.playernow
        if self.game_stat:
            next_write = self.player_write[self.playernow]
            next_fill = self.player_list[self.playernow]
            self.label_text.set('到%s方行动，请%s方单击选取你想移动的棋子。' % (next_write, next_write))
            self.cv.itemconfig(self.show_now, text='%s方' % next_write, fill=next_fill)

    # 撤回
    def undo(self):
        if self.undolist:
            self.game_stat = 1
            self.chosen = 0
            chess, last_ingrid = self.undolist[-1]
            self.move_chess(chess, last_ingrid, addundo=False)
            self.set_nextplayer()
            self.undolist = self.undolist[:-1]

    # 图形界面移动棋子
    def move_chess_gui(self, chess, to_pos):
        button = chess.button
        x_change = to_pos[0] - chess.pos[0]
        y_change = to_pos[1] - chess.pos[1]
        self.cv.move(button, x_change*self.m, y_change*self.m)
        self.cv.lift(button)
        chess.set_pos(to_pos)

    # 移动棋子
    def move_chess(self, chess, to, addundo=True):
        if type(to) == int:
            grid = self.grids[to]
        else:
            grid = self.chess_bags[int(to)]
        if grid.add_chess(chess):
            self.move_chess_gui(chess, grid.pos)
            ingrid = chess.ingrid
            if addundo:
                self.undolist.append([chess, ingrid])
            if type(ingrid) == int:
                self.grids[ingrid].move_chess()
            else:
                chess_bag = self.chess_bags[int(ingrid)]
                chess_bag.move_chess()
                rn = len(chess_bag.chess)
                rn_btn = chess_bag.button
                text_ = str(rn) if rn else ''
                self.cv.itemconfig(rn_btn, text=text_)
                self.cv.lift(rn_btn)
            chess.set_ingrid(to)
            if type(to) == str:
                button = grid.button
                self.cv.itemconfig(button, text=str(len(grid.chess)))
                self.cv.lift(button)
            return True
        else:
            return False

    def play(self):
        self.chosen = 0
        def cancle(event):
            if self.game_stat:
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
                        if self.move_chess(chosen_chess, grid_ix):
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