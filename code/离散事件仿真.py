"""
    Des：用于Section16 离散事件仿真建模，使用协程管理并发操作，
    Date: 2021.06.21
    Author：Laurent Lo
"""
import random
import math
from collections import namedtuple
from queue import PriorityQueue
Event = namedtuple("Event","time proc action")
START_INTERVAL = 6

def taxi_pro(id, trips, start_time=0):
    sim_time = yield Event(start_time, id, "leaving garage")
    for i in range(trips):
        sim_time = yield Event(sim_time, id, "picking passenger")
        sim_time = yield Event(sim_time, id, "dropping passenger")
    yield Event(sim_time, id , "going home")

def init_taxipro(num_taxi):
    return {i:taxi_pro(i, random.choice(range(2,6)), START_INTERVAL*i) for i in range(1,num_taxi)}



def get_randomtime():
    return random.randint(1,6)

class Simulator:
    def __init__(self, num_taxis):
        self.pro = dict(init_taxipro(num_taxis))
        self.events = PriorityQueue()
    def run(self, end_time):

        for k,v in sorted(self.pro.items()):
            event = next(v)
            self.events.put(event)

        sim_clock = 0
        while(sim_clock < end_time):
            if self.events.empty():
                break
            current_event = self.events.get()
            sim_clock, id, action = current_event
            print("taxt: ", id, id*"  ", current_event)
            current_taxi = self.pro[id]     #获取当前的generator
            next_time= sim_clock + get_randomtime()
            try:
                next_event = current_taxi.send(next_time)
            except StopIteration:
                # trips 用完了，出租车该回家了
                del self.pro[id]
            else:
                self.events.put(next_event)

        else:
            # 到达时间正常退出
            fmt = "reach end time ,{} events pending, exit"
            print(fmt.format(self.events.qsize()))


sim = Simulator(6)
sim.run(100)