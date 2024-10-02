from pynput import mouse

click_count = 0
last_position = None

CLICK_LIMIT = 10

print("Click detection started.....\n")
click_count = 0
last_position = 0

def on_click(x, y, button, pressed):
    global click_count, last_position

    if pressed:
        if last_position is None:
            last_position = (x, y)

        current_position = (x, y)
        if current_position == last_position:
            click_count += 1
        else:
            click_count = 1
            last_position = current_position

        if click_count > CLICK_LIMIT:
            print("Bot detection triggered (excessive clicks without movement)")
            click_count = 0

def on_move(x, y):
    global click_count, last_position
    last_position = (x, y)
    click_count = 0

with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
    listener.join()
