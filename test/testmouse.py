from pynput import keyboard

from key_event_factory import KeyEventFactory
kf=KeyEventFactory()

def on_press(key):
    try:
        print("name:  "+str(key.name))
    except Exception as e:
        print("char    "+str(key.char))
    finally:
        if 'value' in dir(key):
            vk=key.value.vk
        else:
            vk=key.vk

        print("finally"+str(key)+"\tvk:  "+str(vk)+"\n\n\n")

def on_release(key):
    print("---------------------------------------")
    print(kf.input(key))
    print("-------------------------------")


    if key == keyboard.Key.esc:
        # Stop listener
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