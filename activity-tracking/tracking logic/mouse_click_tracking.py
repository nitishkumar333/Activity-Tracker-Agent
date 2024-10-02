from pynput import mouse

# Initialize variables to track clicks and position
click_count = 0
last_position = None

# Define the limit for clicks without movement
CLICK_LIMIT = 10

# Function to detect clicks and detect bots
def detect_clicks():
    print("Click detection started.....\n")
    global click_count, last_position

    # Function to handle mouse clicks
    def on_click(x, y, button, pressed):
        global click_count, last_position

        if pressed:
            # If it's the first click, store the position
            if last_position is None:
                last_position = (x, y)

            # Check if the mouse position has changed
            current_position = (x, y)
            if current_position == last_position:
                # Increment the click count if position hasn't changed
                click_count += 1
            else:
                # Reset if the mouse has moved
                click_count = 1
                last_position = current_position

            # Check if the click count exceeds the limit
            if click_count > CLICK_LIMIT:
                print("Bot detected !")
                # Reset click count after detection
                click_count = 0

    # Function to handle mouse movement
    def on_move(x, y):
        global click_count, last_position
        last_position = (x, y)
        click_count = 0

    # Set up the mouse listener
    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        listener.join()

if __name__ == "__main__":
    detect_clicks()