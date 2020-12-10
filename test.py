import tkinter as tk
root = tk.Tk()
w = 800
h = 600
cv = tk.Canvas(root, bg='white', width=w, height=h)
l = 450
x1, y1 = (w-l)/2, (h-l)/2
x2, y2 = x1 + l, y1 + l
cv.create_rectangle(x1, y1, x2, y2)
for i in range(1,3):
    cv.create_line(x1, y1+l/3*i, x2, y1+l/3*i)
    cv.create_line(x1+l/3*i, y1, x1+l/3*i, y2)
r1,r2,r3 = 0.3 * l / 6, 0.55 * l / 6, 0.8 * l / 6
btn = cv.create_oval(x1 + l / 3 / 2 - r1, y1 + l / 3 / 2 - r1, x1 + l / 3 / 2  + r1, y1 + l / 3 / 2 + r1, fill='blue')
# btn2 = cv.create_oval(x1 + l / 3 / 2 - r2, y1 + l / 3 / 2 - r2, x1 + l / 3 / 2  + r2, y1 + l / 3 / 2 + r2, fill='blue')
print(x1 + l / 3 / 2 - r1)
cx = x1 + l / 6
cy = y1 + l / 6
now = [cx, cy]
def xFunc1(event):
    cv.move(btn, event.x - now[0], event.y - now[1])
    now[0] = event.x
    now[1] = event.y
cv.bind('<B1-Motion>', xFunc1)
cv.pack()

root.mainloop()

# import tkinter
# from tkinter import ttk
 
 
# def xFunc1(event):
#     print(f"鼠标左键滑动坐标是:x={event.x},y={event.y}")
 
 
# win = tkinter.Tk()
# win.title("Kahn Software v1")    # #窗口标题
# win.geometry("600x500+200+20")   # #窗口位置500后面是字母x
# '''
# 鼠标移动事件
# <B1-Motion>   鼠标左键滑动
# <B2-Motion>   鼠标滚轮移动
# <B3-Motion>   鼠标右键滑动
# '''
# xLabel = tkinter.Label(win, text="KAHN Hello world")
# xLabel.pack()
# xLabel.bind("<B1-Motion>", xFunc1)
 
# win.mainloop()   # #窗口持久