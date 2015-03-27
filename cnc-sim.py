import sys
import time
import math
import threading

import pylab as plt
import numpy as np

from tkinter import *


WIDTH, HEIGHT = 800, 600


class App(object):

	def __init__(self, master):
		frame = Frame(master)
		frame.pack()
		
		self.canvas = Canvas(frame, width=WIDTH, height=HEIGHT, bg="#ffffff")
		self.canvas.pack()
		
		self.img = PhotoImage(width=WIDTH, height=HEIGHT)
		self.canvas.create_image(
			(WIDTH/2, HEIGHT/2), image=self.img, state="normal"
		)
		
		self.button = Button(frame,text="QUIT", fg="red", command=frame.quit)
		self.button.pack(side=LEFT)
		self.slogan = Button(frame, text="Hello", command=self.write_slogan)
		self.slogan.pack(side=LEFT)
		
	def write_slogan(self, slogan):
		print (slogan)

	
class KillableThread(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.kill_received = False
		
	def run(self):
		while not self.kill_received:
			self.action()
			
	def action(self):
		pass
			
	def kill(self):
		self.kill_received = True
	
	
class Timer(KillableThread):
	
	def __init__(self, frequency=1, acceleration=0):
		KillableThread.__init__(self)
		self.frequency = frequency
		self.acceleration = acceleration
		self.time = 0
		self.ticks = 0
		self.current_frequency = (math.sqrt((9.55 * 2) / self.acceleration))*(math.sqrt(self.ticks + 1) - math.sqrt(self.ticks))
		

	def action(self):
		
		self.ticks += 1
		#if (self.current_frequency > self.frequency):
		self.current_frequency = (math.sqrt((9.55 * 2) / self.acceleration))*(math.sqrt(self.ticks + 1) - math.sqrt(self.ticks))
		#else:
			#self.current_frequency = self.frequency
		time.sleep(self.current_frequency)
		
		self.time += self.current_frequency
		#print(self, 1 / self.current_frequency, self.time)
		
			
class Drawer(KillableThread):
	
	def __init__(self, app, x, y):
		KillableThread.__init__(self)
		self.app = app
		self.img = app.img
		self.canvas = app.canvas
		self.x = x
		self.y = y

	def action(self):
		try:
			if (self.x.ticks < 800 and self.y.ticks < 600):
				self.img.put("#000000", (self.x.ticks, self.y.ticks))
				self.canvas.update()
				#canvas.after(50)
		except:
			sys.exit()


def start_threads(*threads):
	for trd in threads:
		trd.start()
			
			
def main():
	
	# root = Tk()
	# app = App(root)
	
	timer_x = Timer(1/100, acceleration=100)
	timer_y = Timer(1/50, acceleration=200)
	# drawer = Drawer(app, timer_x, timer_y)

	# start_threads(timer_x, timer_y, drawer)

	# root.mainloop()
	
	plt.ion()
	graph, = plt.plot(timer_x.ticks, timer_y.ticks)
	while True:
		graph.set_ydata(timer_x.ticks)
		graph.set_ydata(timer_y.ticks)
		plt.draw()

	timer_x.kill()
	timer_y.kill()
	drawer.kill()
	
if __name__ == '__main__':
	main()
