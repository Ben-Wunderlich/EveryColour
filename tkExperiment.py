from tkinter import *
import time


class boots(object):
     def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=400, height = 400)
        self.canvas.pack()
        # self.alien1 = self.canvas.create_oval(20, 260, 120, 360, outline='white',         fill='blue')
        # self.alien2 = self.canvas.create_oval(2, 2, 40, 40, outline='white', fill='red')

        width = 400
        height = 400
        self.img = PhotoImage(width=width, height=height)
        self.canvas.create_image((width, height), image=self.img, state="normal")

        self.canvas.pack()
        self.root.after(0, self.animation)
        self.root.mainloop()

     def animation(self):

        for i in range(0,100):
            time.sleep(0.025)

            # self.canvas.move(self.alien1, x, y)
            # self.canvas.move(self.alien2, x, y)
            self.img.put("#4287f5", (10, i))
            self.img.put("#4287f5", (11, i))

            self.canvas.update()
        track = 1
        print("check")

        print(track)

boots()