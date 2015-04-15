import time
import threading

import gradient

from math import sqrt
from tkinter import *


WIDTH, HEIGHT = 800, 600
POSITIVE, NEGATIVE, ZERO = 0, 1, 2


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.anim_stop = False
        self.colormap = gradient.generate('#00ff00', '#ff0000', n=40)

        self.motor_x = Motor()
        self.motor_y = Motor()

        self.motor_x.start()
        self.motor_y.start()

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
        self.entry_coord_x.insert(0, '100')
        self.entry_coord_x.pack(side=LEFT)

        self.entry_coord_y = Entry()
        self.entry_coord_y.insert(0, '500')
        self.entry_coord_y.pack(side=LEFT)

        self.label = Label(text='')
        self.label.pack()

    def animate(self):
        velocity = 0

        if self.motor_x.move or self.motor_y.move:
            if self.motor_x.steps == 0:
                velocity = int(1 / self.motor_y.delay)
            elif self.motor_y.steps == 0:
                velocity = int(1 / self.motor_x.delay)
            else :
                velocity = (
                    int(sqrt(
                        (1/self.motor_x.delay)**2 + (1/self.motor_y.delay)**2)
                    )
                )

            if velocity < len(self.colormap):
                velocity_color = self.colormap[velocity]
            else:
                velocity_color = self.colormap[-1]

            self.img.put(velocity_color, (self.motor_x.pos, self.motor_y.pos))

        self.label.configure(
            text='X: {}, Y: {}, V: {:.2f} ш/с'.format( 
                self.motor_x.pos, self.motor_y.pos, velocity
            )
        )
        self.canvas.update()
        self.after(1, self.animate)

    def quit(self):
        self.motor_x.kill()
        self.motor_y.kill()
        self.master.destroy()

    def start(self):
        if not self.motor_x.move and not self.motor_y.move:
            # self.img.blank() # Temporary blank the image.

            speed = 40 # steps per second
            accel = 20 # max accel steps per second per second

            num_steps_x = int(self.entry_coord_x.get()) - self.motor_x.pos
            num_steps_y = int(self.entry_coord_y.get()) - self.motor_y.pos

            print(num_steps_x, num_steps_y)

            move_time = (
                (2 * sqrt(abs(num_steps_x)**2 + abs(num_steps_y)**2)) / speed
            )

            print('move time: ', move_time)

            self.motor_x.accel = (2 * abs(num_steps_x)) / (move_time**2)
            self.motor_x.steps = num_steps_x
            
            print('accel x: ', self.motor_x.accel)
                
            self.motor_y.accel = (2 * abs(num_steps_y)) / (move_time**2)
            self.motor_y.steps = num_steps_y

            self.motor_x.move = True
            self.motor_y.move = True

            print('accel y: ', self.motor_y.accel)


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
    
    
class Motor(KillableThread):
    
    def __init__(self, steps=0, speed=0, accel=0):
        KillableThread.__init__(self)
        
        self.pos = 0
        self.step_counter = 0
        self.steps = steps
        self.delay = 0.01
        self.move = False
        self.speed = speed
        self.accel = accel

    def action(self):
        while True:
            if self.move and self.step_counter < abs(self.steps):
                self.delay = (
                    (sqrt((2) / self.accel)) *
                    (sqrt(self.step_counter + 1) - sqrt(self.step_counter))
                )
                self.step_counter += 1

                if self.steps > 0:
                    self.pos += 1
                else:
                    self.pos -= 1
            else:
                self.step_counter = 0
                self.delay = 0.01
                self.move = False

            time.sleep(self.delay)

            
def main():
    root = Tk()
    app = App(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
