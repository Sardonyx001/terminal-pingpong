#!/usr/bin/env python3

import curses
import time

def main(stdscr):
    # Setup
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(1)  # Refresh rate (milliseconds)

    # Number of boxes
    num_boxes = 10

    # Create the initial list of boxes
    boxes = ["[ ]"] * num_boxes

    # Calculate the starting x position for the boxes to be centered horizontally
    screen_height, screen_width = stdscr.getmaxyx()
    box_width = len(boxes[0])
    start_x = (screen_width - (num_boxes * box_width)) // 2

    # Initial position of the moving "o"
    position = 0

    # Initial direction of movement
    direction = 1

    # Initialize the message
    message = "Press a button"

    # Animation loop
    while True:
        stdscr.clear()

        # Display the message at the upper left corner
        stdscr.addstr(0, 0, message)

        # Display the boxes
        for i in range(num_boxes):
            stdscr.addstr(screen_height // 2 - 1, start_x + i * box_width + 1, str(i))
            stdscr.addstr(screen_height // 2, start_x + i * box_width, boxes[i])

        # Display the moving "o"
        stdscr.addstr(screen_height // 2, start_x + position * box_width + 1, "o")

        # Refresh the screen
        stdscr.refresh()

        # Check for keypress
        key = stdscr.getch()

        if key == 10:  # Enter key
            break

        elif key in range(48, 58):  # Number keys 0-9
            box_index = key - 48
            toggled = ""
            # Toggle the box between "[ ]" and "[*]"
            if boxes[box_index] == "[ ]":
                boxes[box_index] = "[*]"
                toggled = "toggled"
            else:
                boxes[box_index] = "[ ]"
                toggled = "untoggled"
            # Update the message with the pressed button
            message = f"Button {box_index} {toggled}"

        elif key in [99, 67]:  # "c" or "C" key
            # Clear all toggled boxes
            boxes = ["[ ]"] * num_boxes
            # Update the message
            message = "Cleared all boxes"

        # Move the "*" to the next box or reverse direction if encountered a "*"
        position += direction

        # Wrap the position around using the remainder operator
        position = (position + num_boxes) % num_boxes

        if boxes[(position+direction)%num_boxes] == "[*]":
            direction *= -1

        # Pause for a short duration
        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
