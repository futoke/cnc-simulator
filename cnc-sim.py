import sys
import time
import random
import threading

from math import sqrt
from tkinter import *


WIDTH, HEIGHT = 800, 600


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.anim_stop = False

        self.timer_x = Timer()
        self.timer_y = Timer()

        self.timer_x.start()
        self.timer_y.start()

        self.animate()

    def create_widgets(self):
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg='#ffffff')
        self.img = PhotoImage(width=WIDTH, height=HEIGHT)
        self.canvas.create_image(
            (WIDTH / 2, HEIGHT / 2), image=self.img, state='normal'
        )
        self.canvas.pack()
        
        self.btn_quit = Button(self, text='QUIT', fg='red', command=self.quit)
        self.btn_quit.pack(side=LEFT)

        self.btn_reset = Button(self, text='START', command=self.start)
        self.btn_reset.pack(side=LEFT)

        self.entry_coord_x = Entry()
        self.entry_coord_x.pack(side=LEFT)

        self.entry_coord_y = Entry()
        self.entry_coord_y.pack(side=LEFT)

        self.label = Label(text='')
        self.label.pack()


    def animate(self):
        # if not self.anim_stop:

        # def get_curr_speed (timer):
        #     if timer.move_time > 0:
        #         return timer.ticks / timer.move_time
        #     else:
        #         return 0


        self.img.put('#000000', (self.timer_x.ticks, self.timer_y.ticks))

        # tmpl = (
        #     'X: {}, Y: {}, '
        #     'Vx: {:.2f} шаг./с, Vy: {:.2f} шаг./с, V: {:.2f} шаг./с'
        # )

        # curr_speed_x = get_curr_speed(self.timer_x)
        # curr_speed_y = get_curr_speed(self.timer_y)
        # curr_speed = sqrt(curr_speed_x*curr_speed_x + curr_speed_y*curr_speed_y)


        # self.label.configure(
        #     text=tmpl.format(
        #         self.timer_x.ticks,
        #         self.timer_y.ticks,
        #         curr_speed_x,
        #         curr_speed_y,
        #         curr_speed,
        #     )
        # )
        velocity = 0
        if self.timer_x.delay != 0 and self.timer_x.delay != 0:
            velocity = sqrt((1 / self.timer_x.delay)**2 + (1 / self.timer_y.delay)**2)
        print(velocity)
        
        self.label.configure(text='X: {}, Y: {}, V: {:.2f} ш/с'.format(self.timer_x.ticks, self.timer_y.ticks, velocity))
        self.canvas.update()
        self.after(1, self.animate)

    def quit(self):
        self.timer_x.kill()
        self.timer_y.kill()
        self.master.destroy()

    def start(self):
        self.img.blank() # Temporary blank the image.

        speed = 40 # steps per second
        accel = 20 # max accel steps per second per second
        num_steps_x = int(self.entry_coord_x.get())
        num_steps_y = int(self.entry_coord_y.get())

        move_time = (2 * sqrt(num_steps_x**2 + num_steps_y**2)) / speed

        self.timer_x.accel = (2 * num_steps_x) / (move_time**2)
        self.timer_y.accel = (2 * num_steps_y) / (move_time**2)
   
        self.timer_x.steps = num_steps_x
        self.timer_y.steps = num_steps_y


class KillableThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.kill_received = False
        
    def run(self):
        while not self.kill_received:
            self.action()
            
    def action(self):
        pass
            
    def kill(self):
        self.kill_received = True
    
    
class Timer(KillableThread):
    
    def __init__(self, steps=0, speed=0, accel=0):
        KillableThread.__init__(self)
        
        self.ticks = 0
        self.move_time = 0
        self.delay = 0.0001
        self.steps = steps
        self.speed = speed
        self.accel = accel

    def run(self):

        while True:
            if self.ticks < self.steps:
                # print(self)
                self.delay = (
                    (sqrt((2) / self.accel)) *
                    (sqrt(self.ticks + 1) - sqrt(self.ticks))
                )
                # self.delay = 1 / self.speed

                self.ticks += 1
                self.move_time += self.delay
            else:
                self.ticks = 0
                self.steps = 0
                self.move_time = 0
                self.delay = 0.0001

            time.sleep(self.delay)

            
def main():
    
    root = Tk()
    app = App(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
