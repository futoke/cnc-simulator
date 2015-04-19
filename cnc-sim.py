import time
import multiprocessing as mp

import gradient

from math import sqrt
from tkinter import *


MAIN_FREQUENCY = 1000
WIDTH, HEIGHT = 800, 600
STOP, MOVE = 0, 1
POSITIVE, NEGATIVE, ZERO = 0, 1, 2


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.create_widgets()

        self.colormap = gradient.generate('#0000ff', '#ff0000', n=40)

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

        if (self.motor_x.action.value == MOVE or
            self.motor_y.action.value == MOVE):
            if self.motor_x.steps.value == 0:
                velocity = int(self.motor_y.velocity.value)
            elif self.motor_y.steps.value == 0:
                velocity = int(self.motor_x.velocity.value)
            else :
                velocity = (
                    int(sqrt(
                            (self.motor_x.velocity.value)**2 + 
                            (self.motor_y.velocity.value)**2
                        )
                    )
                )

            if velocity < len(self.colormap):
                velocity_color = self.colormap[velocity]
            else:
                velocity_color = self.colormap[-1]

            self.img.put(velocity_color, (
                self.motor_x.pos.value, self.motor_y.pos.value)
            )

        self.label.configure(
            text='X: {}, Y: {}, V: {:.2f} ш/с'.format( 
                self.motor_x.pos.value, self.motor_y.pos.value, velocity
            )
        )
        # self.canvas.update()
        self.after(1, self.animate)

    def quit(self):
        self.motor_x.terminate()
        self.motor_y.terminate()
        self.master.destroy()

    def start(self):
        if (self.motor_x.action.value == STOP and
            self.motor_y.action.value == STOP):
            # self.img.blank() # Temporary blank the image.

            speed = 30 # steps per second
            accel = 20 # max accel steps per second per second

            num_steps_x = int(self.entry_coord_x.get()) - self.motor_x.pos.value
            num_steps_y = int(self.entry_coord_y.get()) - self.motor_y.pos.value

            print(num_steps_x, num_steps_y)

            move_time = (
                (2 * sqrt(abs(num_steps_x)**2 + abs(num_steps_y)**2)) / speed
            )

            print('move time: ', move_time)

            self.motor_x.accel.value = (2 * abs(num_steps_x)) / (move_time**2)
            self.motor_x.steps.value = num_steps_x
            
            print('accel x: ', self.motor_x.accel.value)
                
            self.motor_y.accel.value = (2 * abs(num_steps_y)) / (move_time**2)
            self.motor_y.steps.value = num_steps_y

            self.motor_x.action.value = MOVE
            self.motor_y.action.value = MOVE

            print('accel y: ', self.motor_y.accel.value)
    
    
class Motor(mp.Process):
    
    def __init__(self):
        mp.Process.__init__(self)
        
        self.step_counter = 0
        self.velocity = mp.Value('d', MAIN_FREQUENCY)
        self.pos = mp.Value('l', 0)
        self.steps = mp.Value('l', 0)
        self.action = mp.Value('b', STOP)
        self.velocity = mp.Value('d', 0)
        self.accel = mp.Value('d', 0)

    def run(self):

        while True:
            if (self.action.value == MOVE and 
                self.step_counter < abs(self.steps.value)):

                self.velocity.value = 1 / (
                    (sqrt((2) / self.accel.value)) *
                    (sqrt(self.step_counter + 1) - sqrt(self.step_counter))
                )
                self.step_counter += 1

                with self.pos.get_lock():
                    if self.steps.value > 0:
                        
                        self.pos.value += 1
                    else:
                        self.pos.value -= 1
            else:
                self.step_counter = 0
                self.velocity.value = MAIN_FREQUENCY

                self.action.value = STOP

            time.sleep(1 / self.velocity.value)

            
def main():
    root = Tk()
    app = App(master=root)
    root.mainloop()


if __name__ == '__main__':
    main()
