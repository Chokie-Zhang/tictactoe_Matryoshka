# （旧版本，最新版本见 master 分支）
# 井字过三关（套娃版）

目前游戏以 `Python` 的 `turtle` 模块提供简陋的前端图形，行动则以命令行的交互执行。

## 游戏规则：

1. 红蓝双方初始均拥有大中小棋子各 2 个；

2. 在井字棋盘的 9 个格子中红蓝双方轮流行动下棋，红方为先手方；

3. 每回合玩家可以选择两种行动：

   - 选择手中剩余的棋子放到棋盘中；
   - 将棋盘中任一己方棋子移动到棋盘的另外一处地方；

   且不允许玩家不行动；

4. 井字棋盘的每一格不限棋子数目，但只能以较大的棋子覆盖较小的棋子（同种大小的棋子不允许覆盖），且被覆盖的棋子无法被看见；

5. 被覆盖的棋子无法移动，即只能移动最上层的棋子，移动后，次层棋子将露出；

6. 每回合玩家行动过后，结算胜负（是否某一列或某一行或某一斜线达成三色相同）；

7. 若一方移动棋子后造成双方同时达成胜利条件，判定为对方胜利（考虑为拿起棋子的瞬间对方就达成了胜利条件）。

## 更新日志

### 2020/11/10：

修正了游戏结束时无法重新游戏而闪退的 bug，增加了游戏结束时返回上一步的功能，增加了在游戏过程通过输入`Ctrl+C` 重新游戏的功能。

### 2020/11/09：

修正了移动棋子失败的 bug，修正了悔棋失败的 bug。

## 游玩感受

一个人尝试多次的游戏以及和同伴尝试，按目前的规则来看，只要按特定模式下开局的几手，似乎都能做到先手必胜。

