import sys
import time
import random
import threading
import multiprocessing

import numpy as np
import matplotlib.pyplot as plt

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

        speed = 40 # steps per second
        accel = 20 # steps per second per second
        num_steps_x = 100
        num_steps_y = 500

        path_len = sqrt(num_steps_x * num_steps_x + num_steps_y * num_steps_y)
        print('path_len: ', path_len)
        move_time = sqrt((2 * path_len) / accel)
        # move_time = path_len / speed

        print('move_time: ', move_time)
        if num_steps_x > 0:
            speed_x =  (2 * num_steps_x) / move_time
            # speed_x = num_steps_x / move_time
        print('speed_x: ', speed_x)
        if num_steps_y > 0:
            speed_y = (2 * num_steps_y) / move_time
            # speed_y = num_steps_y / move_time
        print('speed_y: ', speed_y)

        self.timer_x = Timer(
            speed=speed_x,
            steps=num_steps_x,
            time=move_time
        )
        self.timer_y = Timer(
            speed=speed_y,
            steps=num_steps_y,
            time=move_time
        )

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

        def get_curr_speed (timer):
            if timer.move_time > 0:
                return timer.ticks / timer.move_time
            else:
                return 0


        self.img.put('#000000', (self.timer_x.ticks, self.timer_y.ticks))

        tmpl = (
            'X: {}, Y: {}, '
            'Vx: {:.2f} шаг./с, Vy: {:.2f} шаг./с, V: {:.2f} шаг./с, '
            't: {:.2f} c'
        )

        curr_speed_x = get_curr_speed(self.timer_x)
        curr_speed_y = get_curr_speed(self.timer_y)
        curr_speed = sqrt(curr_speed_x*curr_speed_x + curr_speed_y*curr_speed_y)


        self.label.configure(
            text=tmpl.format(
                self.timer_x.ticks,
                self.timer_y.ticks,
                curr_speed_x,
                curr_speed_y,
                curr_speed,
                self.timer_x.move_time
            )
        )
        self.canvas.update()
        self.after(1, self.animate)

    def quit(self):
        self.timer_x.kill()
        self.timer_y.kill()
        # self.timer_x.terminate()
        # self.timer_y.terminate()
        self.master.destroy()

    def start(self):
        self.timer_x.ticks = 0
        self.timer_y.ticks = 0
        self.timer_x.delay = 0
        self.timer_y.delay = 0
        self.timer_x.steps = int(self.entry_coord_x.get())
        self.timer_y.steps = int(self.entry_coord_y.get())
        self.img.blank()

    
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
    
    def __init__(self, speed, steps, time):
        KillableThread.__init__(self)
        self.speed = speed
        self.steps = steps
        self.accel = speed / time

        self.ticks = 0
        self.delay = 0
        self.move_time = 0
        

    def run(self):

        while True:
            if self.ticks < self.steps:
                self.delay = (
                    (sqrt((2) / self.accel)) *
                    (sqrt(self.ticks + 5) - sqrt(self.ticks))
                )
                # self.delay = 1 / self.speed
                
                time.sleep(self.delay)

                self.move_time += self.delay
                self.ticks += 5
                # print(self)
            else:
                self.ticks = 0
                self.steps = 0


# class Timer(multiprocessing.Process):
    
#     def __init__(self, speed, steps, time):
#         multiprocessing.Process.__init__(self)
#         self.daemon = True

#         self.speed = speed
#         self.steps = steps
#         self.accel = speed / time

#         self.ticks = 0
#         self.delay = 0
#         self.move_time = 0
        

#     def run(self):

#         while self.ticks < self.steps:
#             self.delay = (
#                 (sqrt((2) / self.accel)) *
#                 (sqrt(self.ticks + 1) - sqrt(self.ticks))
#             )
#             # self.delay = 1 / self.speed
            
#             time.sleep(self.delay)

#             self.move_time += self.delay
#             self.ticks += 1  
#             print(self)

            
def main():
    
    root = Tk()
    app = App(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
