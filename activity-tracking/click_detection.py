from pynput import mouse

click_count = 0
last_position = None

CLICK_LIMIT = 10

print("Click detection started.....\n")
click_count = 0
last_position = 0

def on_click(x, y, button, pressed):
    return

def on_move(x, y):
    global click_count, last_position
    last_position = (x, y)
    click_count = 0

with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
    listener.join()
