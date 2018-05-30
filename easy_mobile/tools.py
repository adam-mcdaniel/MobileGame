import os
import sys
import time
from .sprite import *

def path(arg):
    # return os.path.join(os.path.dirname(sys.argv[0]), arg)
    return arg


class TimedAction:
	def __init__(self, time_difference, function):
		self.start = time.time()
		self.time_difference = time_difference
		self.function = function

	def update(self, screen):
		if (time.time() - self.start) > self.time_difference:
			self.start = time.time()
			self.function(screen)
		else:
			pass


