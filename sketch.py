from tkinter import *
import math
from PIL import ImageGrab, ImageTk
import cv2

master = Tk()

canvas_width = 512
canvas_height = 512


def roundup_10(x):
    return int(math.ceil(x / 10.0)) * 10
def rounddown_10(x):
    return int(math.floor(x / 10.0)) * 10

w = Canvas(master,width=canvas_width,height=canvas_height, cursor="none", background="white")

w.pack()

y = int(canvas_height / 2)
#w.create_rectangle(0,y,canvas_width,y, fill="#476042")
cursor = None #w.create_oval(100, 100, 120, 120, fill="red")

draw = True



s = Scale(master, from_=5, to=50, orient=HORIZONTAL, label="linethickness")
s.pack()



def erase_btn_click(event=None):
    print("erase")
    print(w.winfo_rootx())
    w.delete("all")

def save_canvas(event=None):

    x1 = w.winfo_rootx() + w.winfo_x()
    y1 = w.winfo_rooty() + w.winfo_y()
    x2 = x1 + w.winfo_width()
    y2 = y1 + w.winfo_height()

    ImageGrab.grab(bbox=(x1,y1,x2,y2)).save("out_snapsave.jpg")
    img = cv2.imread("out_snapsave.jpg")

    print(x1,x2,y1,y2)


erase_button = Button(master, text="clear", command=erase_btn_click)
erase_button.pack()
save_button = Button(master, text="save", command=save_canvas)
save_button.pack()

# def moveCursor(event):
#     # (x1,y1,x2,y2) = w.coords(cursor)
#     # x = (x1 + x2) // 2
#     # y = (y1 + y2) // 2
#     x1 = event.x
#     y2 = event.y
#     # delta_x = x - x1 if x1 < x else x1 - x
#     # delta_y = y - y1 if y1 < y else y1 - y
#     # w.move(cursor, delta_x, delta_y)
#     cursor = w.create_oval(x1, y2, x1+5, y2+5, fill="red")

#def update_cursor():

def drawLine(event):
    #print(event.x, event.y)
    #w.config(cursor="plus")
    x1 = event.x
    y1 = event.y
    x2 = x1
    y2 = y1
    if w.prev_coords:
        x2 = event.x
        y2 = event.y
        x1 = w.prev_coords[0]
        y1 = w.prev_coords[1]
        w.create_line(x1, y1, x2, y2, width = s.get(), fill = "black", smooth="true")

    delta = s.get() // 2
    w.create_oval(x1-delta,y1-delta,x1+delta,y1+delta, width=0, fill="black")


    # w.create_oval(x1, y1, x1, y1, width = 5, fill = "black")
    x = event.x
    y = event.y
    delta = s.get() // 2
    w.prev_coords = (x2,y2)
    if w.circle == None:
        w.circle = w.create_oval(x-delta, y-delta, x+delta, y+delta, outline='black')
    else:
        w.coords(w.circle, x-delta, y-delta, x+delta, y+delta)
    w.tag_raise(w.circle)
    w.itemconfig(w.circle, outline="red")


def eraseLine(event):
    #print(event.x, event.y)
    #w.config(cursor="circle")
    x1 = event.x
    y1 = event.y
    x2 = x1
    y2 = y1
    if w.prev_coords:
        x2 = event.x
        y2 = event.y
        x1 = w.prev_coords[0]
        y1 = w.prev_coords[1]
        w.create_line(x1, y1, x2, y2, width = s.get(), fill = "white", smooth="true")

    delta = s.get() // 2
    w.create_oval(x1-delta,y1-delta,x1+delta,y1+delta, width=0, fill="white")
    w.prev_coords = (x2,y2)
    x = event.x
    y = event.y
    delta = s.get() // 2

    if w.circle == None:
        w.circle = w.create_oval(x-delta, y-delta, x+delta, y+delta, outline='black')
    else:
        w.coords(w.circle, x-delta, y-delta, x+delta, y+delta)
    w.tag_raise(w.circle)
    w.itemconfig(w.circle, outline="red")

def endLine_draw(event):
    w.prev_coords = None
    w.itemconfig(w.circle, outline="blue")


w.circle = None

def move_cursor(event):
    x = event.x
    y = event.y
    delta = s.get() // 2

    if w.circle == None:
        w.circle = w.create_oval(x-delta, y-delta, x+delta, y+delta, outline='blue')
    else:
        w.coords(w.circle, x-delta, y-delta, x+delta, y+delta)
    w.tag_raise(w.circle)



w.prev_coords = None
def brush_size_up(event):
    if s.get() == 50:
        return
    if s.get() % 10 == 0:
        s.set(roundup_10(s.get() + 1))
    else:
        s.set(roundup_10(s.get()))


def brush_size_down(event):

    if s.get() < 10:
        s.set(5)
        return
    if s.get() % 10 == 0:
        s.set(rounddown_10(s.get() - 1))
    else:
        s.set(rounddown_10(s.get()))

w.bind('<Button-1>',drawLine)
w.bind('<B1-Motion>',drawLine)
w.bind('<Button-2>',eraseLine)
w.bind('<B2-Motion>',eraseLine)
w.bind('<Button-3>',eraseLine)
w.bind('<B3-Motion>',eraseLine)
w.bind('<Motion>', move_cursor)
w.bind('<ButtonRelease-1>',endLine_draw)
w.bind('<ButtonRelease-2>',endLine_draw)
w.bind('<Shift-Button-1>', eraseLine)
w.bind('<Shift-B1-Motion>', eraseLine)
master.bind('<Up>', brush_size_up)
master.bind('<Down>', brush_size_down)




mainloop()
