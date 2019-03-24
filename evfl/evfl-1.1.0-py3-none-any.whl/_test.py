import evfl.evfl
from evfl.util import nth
import io
import sys

def write(flow) -> None:
    with open('/home/leo/tmp/test.bfevfl', 'wb') as f:
        flow.write(f)

def test_blank() -> None:
    flow = evfl.evfl.EventFlow()
    flow.name = 'GanonQuest'
    flow.flowchart = evfl.evfl.Flowchart()
    flow.flowchart.name = 'GanonQuest'
    write(flow)

def test_readback() -> None:
    flow = evfl.evfl.EventFlow()
    # flow.read(open('/home/leo/botw/wiiu-view/Event/GanonQuest.sbeventpack/EventFlow/GanonQuest.bfevfl', 'rb').read())
    # flow.read(open('/home/leo/botw/wiiu-view/Event/CompleteDungeon.sbeventpack/EventFlow/CompleteDungeon.bfevfl', 'rb').read())
    # flow.read(open('/home/leo/botw/wiiu-view/Event/Npc_SouthHateru007.sbeventpack/EventFlow/Npc_SouthHateru007.bfevfl', 'rb').read())
    orig = open(sys.argv[1], 'rb').read()
    flow.read(orig)
    write(flow)
    buf = io.BytesIO()
    flow.write(buf)
    if buf.getbuffer() != orig:
        sys.stderr.write('different\n')
        sys.exit(1)

def handleNextEvent(actors, events, event, visited, join_stack, next_idx) -> None:
    if next_idx == 0xffff:
        if join_stack:
            print(f'"{event.name}" -> "{nth(events, join_stack[-1]).name}";')
        return

    nxt = nth(events, next_idx)
    print(f'"{event.name}" -> "{nxt.name}";')
    traverse_event(actors, events, nxt, visited, join_stack)

def traverse_event(actors, events, event: evfl.event.Event, visited, join_stack) -> None:
    if event in visited:
        return
    visited.add(event)

    data = event.data

    if isinstance(data, evfl.event.ActionEvent):
        actor = nth(actors,data.actor_idx)
        actor_name = f'{actor.identifier}'
        action_name = f'{actor.actions[data.actor_action_idx]}'
        print(f'"{event.name}" [label="{event.name} - Action\\n{actor_name}::{action_name}"];')
        handleNextEvent(actors, events, event, visited, join_stack, data.next_idx)

    elif isinstance(data, evfl.event.SwitchEvent):
        actor = nth(actors,data.actor_idx)
        actor_name = f'{actor.identifier}'
        query_name = f'{actor.queries[data.actor_query_idx]}'
        print(f'"{event.name}" [label="{event.name} - Switch\\n{actor_name}::{query_name}"];')
        for value, case in data.cases.items():
            n = nth(events, case)
            print(f'"{event.name}" -> "{n.name}" [label="{value}"];')
            traverse_event(actors, events, n, visited, join_stack)
        if join_stack and not (len(data.cases) == 2 and 0 in data.cases and 1 in data.cases):
            print(f'"{event.name}" -> "{nth(events, join_stack[-1]).name}" [label="<default>"];')

    elif isinstance(data, evfl.event.ForkEvent):
        print(f'"{event.name}" [label="{event.name} - Fork"];')
        join_stack.append(data.join_idx)
        for fork in data.forks:
            n = nth(events, fork)
            print(f'"{event.name}" -> "{n.name}";')
            traverse_event(actors, events, n, visited, join_stack)
        traverse_event(actors, events, nth(events, data.join_idx), visited, join_stack)
    elif isinstance(data, evfl.event.JoinEvent):
        join_stack.pop()
        print(f'"{event.name}" [label="{event.name} - Join"];')
        handleNextEvent(actors, events, event, visited, join_stack, data.next_idx)
    elif isinstance(data, evfl.event.SubFlowEvent):
        print(f'"{event.name}" [label="{event.name} - Sub flow\\n{data.res_flowchart_name}<{data.entry_point_name}>"];')
        handleNextEvent(actors, events, event, visited, join_stack, data.next_idx)

flow = None
def show_graph() -> None:
    global flow
    flow = evfl.evfl.EventFlow()
    orig = open(sys.argv[1], 'rb').read()
    flow.read(orig)
    assert flow.flowchart
    for name, entry in flow.flowchart.entry_points.items():
        if name != 'Ready_Npc_Zora025_Call2':
            continue

        # print(name, entry.main_event_idx)
        # print('digraph {')
        entry_event = nth(flow.flowchart.events.values(), entry.main_event_idx)
        print(f'"{name}" [label="<ENTRY POINT: {name}>"];')
        print(f'"{name}" -> "{entry_event.name}";')
        visited = set() # type: ignore
        traverse_event(flow.flowchart.actors.values(), flow.flowchart.events.values(), entry_event, visited, [])
        # print('}')
        # print('-'*72)
    print(len(flow.flowchart.events))
# test_blank()
# test_readback()
show_graph()
