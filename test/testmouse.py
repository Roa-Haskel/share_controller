from pynput import keyboard

def on_press(key):
    try:
        name=key.name
        if not name:
            name=key.char
        print("name is "+name)
    except:
        print("char is {}".format(key.char))
        print(key)
    print('------------------\n')
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listeneraa1
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()