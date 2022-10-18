import pynput


with pynput.mouse.Events() as events:
    # Block at most one second
    for event in events:
        print(dir(event))