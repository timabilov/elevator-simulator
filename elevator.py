import queue
from time import sleep

import math
import sys


class Elevator:

    def __init__(self, max_floor=20,  floor_height=2, meter_per_sec=1.0, oc_time=0.5, curr_floor=1):
        self.oc_time = oc_time  # open/close time
        self.meter_per_sec = meter_per_sec  # speed
        self.curr_floor = curr_floor
        self.max_floor = max_floor
        self.floor_height = floor_height  # considering in meter
        self.tasks = queue.Queue(maxsize=0)  # just in case, arch if considering multi-threading - prod/cons
        print('Elevator in %s floor ' % self.curr_floor)
        self.action('CALL')
        self._consume()

    def _produce(self, action):
        self.tasks.put(action)

    def _consume(self):

        while True:
            to, state = self.tasks.get()
            if to is None:
                break
            self._process_request(self.curr_floor, to)

    def _process_request(self, _from, to):

        def _move():
            delta = to - _from
            direction = int(math.copysign(1, delta))  # however for zero delta - it is not return 0

            # + direction,  for skip current floor
            for floor in range(_from + direction, to,  direction):
                print('Passing through %s floor..' % floor)
                sleep(self.floor_height / self.meter_per_sec)  # plain t = s/v

            self.curr_floor = to

        _move()

        print("The doors are opened.")
        sleep(self.oc_time)
        print("The doors are closed.")

        self.action('PRESS')

    def action(self, operation):

        to = -1
        while not 1 <= to < self.max_floor:
            to = int(input('%s:' % operation.lower().title()))
        if to != 0:
            self._produce((to, operation))
        return self

    def __str__(self):
        return 'Elevator, current floor %s. ' % self.curr_floor


max_floor = int(sys.argv[1])
floor_height = int(sys.argv[2])
meter_per_sec = float(sys.argv[3])
oc_time = float(sys.argv[4])

e = Elevator(max_floor=max_floor, floor_height=floor_height, meter_per_sec=meter_per_sec, oc_time=oc_time)
