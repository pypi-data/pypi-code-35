#! /usr/bin/env python3
import random
import pendulum


clients = ['Client A', 'Client B', 'Client C', 'Client D', 'Client E']

projects = {
    'Client A': ['Project A', 'Project B', 'Project C'],
    'Client B': ['Project a', 'Project b', 'Project c'],
    'Client C': ['Project 1', 'Project 2', 'Project 3'],
    'Client D': ['Project j', 'Project k', 'Project l'],
    'Client E': ['Project x', 'Project y', 'Project z'],
        }


items = []
for month in [1, 2, 3]:
    for i in range(15):
        day = random.choice(range(1, 29))
        hour = random.choice(range(10, 18))
        dt = pendulum.datetime(2019, month, day, hour).format("YYYY-MM-DD h:mmA")
        dur = pendulum.duration(minutes=random.choice(range(20, 125, 5)))
        client = random.choice(clients)
        project = random.choice(projects[client])
        # items.append(f"% {client} @i {client}:{project} @u {dur.hours}h{dur.minutes}m: {dt}")
        items.append(f"% {client} @i {client}:{project} @u {dur.in_minutes()}m: {dt}")

for item in items:
    print(item)


