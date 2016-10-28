# !/usr/bin/python
#  -*- coding: utf-8 -*-
from tkinter import *
from tkinter.simpledialog import *
import random


class snake(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # 蛇身保存它占的方格的坐标
        self.body = [(0,0)]
        # 蛇身由一个个矩形组成,这个矩形的id保存在这里.
        # 这些id在列表里的索引和sefl.body的元素的下标是一一对应的
        self.bodyid = []
        # 新生成的食物的坐标
        self.food = [ -1, -1 ]
        # 新生成的食物的坐标,初始化为-1
        self.foodid = -1
        # 方格的个数
        self.gridcount = 10
        # 窗口的大小
        self.size = 500
        # 蛇的运动方向
        self.di = 3
        # 蛇的运动速度.其实是窗口的更新速度. 数值越大则越慢
        self.speed = 500

        # 取得顶级窗口以设置窗口大小不可变
        self.top = self.winfo_toplevel()
        self.top.resizable(False, False)
        # 显示窗口
        self.grid()
        # 创建画布. 所有代表蛇身的矩形都只能画在画布上
        self.canvas = Canvas(self)
        # 显示画布
        self.canvas.grid()
        # 设置画布大小
        self.canvas.config(width=self.size, height=self.size,relief=RIDGE)

        # 画格子
        self.drawgrid()
        # 计算每个方格的大小
        s = self.size/self.gridcount
        # 初始时,蛇身只有这一个方格
        id = self.canvas.create_rectangle(
                self.body[0][0]*s,self.body[0][1]*s, 
                (self.body[0][0]+1)*s, (self.body[0][1]+1)*s,
                fill="yellow")
        # 这个id对应初始时蛇身的方格
        self.bodyid.insert(0, id)
        # 绑定键盘事件的处理
        self.bind_all('<KeyRelease>', self.keyrelease)
        # 画第一块食物
        self.drawfood()
        # 设定开始更新窗口
        self.after(self.speed, self.drawsnake)

    # 画方格的函数
    def drawgrid(self):
        # 计算每个方格的大小
        s = self.size/self.gridcount
        # 画方格
        for i in range(0, self.gridcount+1):
                self.canvas.create_line(i*s, 0, i*s, self.size)
                self.canvas.create_line(0, i*s, self.size, i*s)

    # 画蛇的函数
    def drawsnake(self):
        # 计算每个方格的大小
        s = self.size/self.gridcount
        # 蛇头
        head = self.body[0]
        # 蛇下一个要移到的方格. 因为保存在self.body的是tuple,不可变,
        # 而这里,位置还有待计算,所以先用list来保存
        new = [head[0], head[1]]
        # 如果蛇的移动方向向上,则蛇下一个要移到的方格的y坐标要减小
        if self.di == 1:
                new[1] = (head[1]-1) % self.gridcount
        # 如果蛇的移动方向向右,则蛇下一个要移到的方格的x坐标要增加
        elif self.di == 2:
                new[0] = (head[0]+1) % self.gridcount
        # 如果蛇的移动方向向下,则蛇下一个要移到的方格的y坐标要增加
        elif self.di == 3:
                new[1] = (head[1]+1) % self.gridcount
        # 如果蛇的移动方向向左,则蛇下一个要移到的方格的x坐标要减小
        else:
                new[0] = (head[0]-1) % self.gridcount
        # 将new转换为tuple
        next = ( new[0], new[1] )
        # 如果下一位置已经是蛇身,则游戏结束
        if next in self.body:
                dlg = SimpleDialog(self, text="Game Over", buttons=['Ok'])
                dlg.go()
                exit()
        # 如果下一位置是食物
        elif next == (self.food[0], self.food[1]):
                # 将食物添加到蛇头
                self.body.insert(0, next)
                # 相应的矩形id也要添加到蛇头
                self.bodyid.insert(0, self.foodid)
                # 画下一个食物
                self.drawfood()
        # 下一位置是普通的空方格
        else:
                # 取蛇尾
                tail = self.body.pop()
                id = self.bodyid.pop()
                # 将蛇尾移到蛇头
                self.canvas.move(id, (next[0]-tail[0])*s, (next[1]-tail[1])*s)
                self.body.insert(0, next)
                self.bodyid.insert(0, id)
        # 递归调用sefl.drawsnake画蛇身,更新窗口
        self.after(self.speed, self.drawsnake)


    # 画食物的函数
    def drawfood(self):
        # 计算方格的大小
        s = self.size/self.gridcount
        # 计算食物的随机位置
        x = random.randrange(0, self.gridcount)
        y = random.randrange(0, self.gridcount)
        # 循环计算食物的位置,直到随机生成的位置不属于蛇身
        while (x, y) in self.body:
                x = random.randrange(0, self.gridcount)
                y = random.randrange(0, self.gridcount)
        # 画食物
        id = self.canvas.create_rectangle(x*s,y*s, (x+1)*s, (y+1)*s, fill="yellow")
        # 保存食物的坐标和id
        self.food[0] = x
        self.food[1] = y
        self.foodid = id


    # 键盘处理函数
    def keyrelease(self, event):
        # 如果近了向上,且现在不是向下
        if event.keysym == "Up" and self.di != 3:
                self.di = 1
        # 如果近了向右,且现在不是向左
        elif event.keysym == "Right" and self.di !=4:
                self.di = 2
        # 如果近了向下,且现在不是向上
        elif event.keysym == "Down" and self.di != 1:
                self.di = 3
        # 如果近了向左,且现在不是向右
        elif event.keysym == "Left" and self.di != 2:
                self.di = 4
                
if __name__ == "__main__":
    app = snake()
    app.master.title("Greedy Snake")
    app.mainloop()