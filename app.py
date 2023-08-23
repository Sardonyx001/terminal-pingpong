#!/usr/bin/env python3
import curses
import time

class Box:
    def __init__(self, shape="[ ]"):
        self.shapes = {True: shape, False:shape.replace(" ", "*")}
        self.shape = shape
        self.is_toggled = False

    def toggle(self):
        self.shape = self.shapes[self.is_toggled]
        self.is_toggled = not self.is_toggled

class Container:
    def __init__(self, boxes):
        self.boxes = boxes

    def move_up(self):
        if self.boxes:
            self.boxes[0].toggle()

    def move_down(self):
        if self.boxes:
            self.boxes[-1].toggle()

class TerminalAnimation:
    def __init__(self, num_boxes, boxes):
        self.num_boxes = num_boxes
        self.boxes = boxes
        self.position = 0
        self.direction = 1
        self.message = "Press q to quit."
        self.refresh_rate = 100

    def setup_curses(self):
        stdscr = curses.initscr()
        curses.curs_set(0)  # Hide the cursor
        stdscr.nodelay(1)  # Non-blocking input
        stdscr.timeout(self.refresh_rate)  # Refresh rate (milliseconds)
        return stdscr

    def calculate_start_x(self, screen_width, box_width):
        return (screen_width - (self.num_boxes * box_width)) // 2

    def display_message(self, stdscr):
        stdscr.addstr(0, 0, self.message)

    def display_boxes(self, stdscr, start_x, box_width):
        screen_height, screen_width = stdscr.getmaxyx()

        for i in range(self.num_boxes):
            box = self.boxes[i]
            stdscr.addstr(screen_height // 2, start_x + i * box_width, box.shape)

    def display_number(self, stdscr, number, start_x, box_width):
        screen_height = stdscr.getmaxyx()[0]
        stdscr.addstr(screen_height // 2 - 1, start_x + number * box_width + 1, str(number))

    def display_o(self, stdscr, start_x, box_width):
        screen_height = stdscr.getmaxyx()[0]
        stdscr.addstr(screen_height // 2, start_x + self.position * box_width + 1, "o")
    
    def adjust_refresh_rate(self, key):
        if key == curses.KEY_UP:
            self.refresh_rate -= 10  # Decrease refresh rate by 10 milliseconds
        elif key == curses.KEY_DOWN:
            self.refresh_rate += 10  # Increase refresh rate by 10 milliseconds

        # Set the minimum refresh rate to 10 milliseconds
        self.refresh_rate = max(self.refresh_rate, 10)
        if self.adjust_refresh_rate == 10:
            self.message = "Minimum Refresh Rate"

    def handle_keypress(self, key):
        if key == ord('q'):  # q key
            return False  # Exit the loop
        elif key in range(48, 58):  # Number keys 0-9
            box_index = key - 48
            box = self.boxes[box_index]

            # Toggle the box
            box.toggle()

            # Update the message with the pressed button and toggle status
            toggle_status = "toggled" if box.is_toggled else "untoggled"
            self.message = f"Box {box_index} {toggle_status}"

        elif key in [99, 67]:  # "c" or "C" key
            # Clear all toggled boxes
            for box in self.boxes:
                box.is_toggled = False

            # Update the message
            self.message = "Cleared all boxes"

        # Move the "o" to the next box or reverse direction if encountered a toggled box
        self.position += self.direction
        self.position %= self.num_boxes

        if self.boxes[(self.position+self.direction)%self.num_boxes].is_toggled:
            self.direction *= -1

        return True  # Continue the loop

    def main(self, stdscr):
        # Setup
        stdscr = self.setup_curses()

        # Calculate the starting x position for the boxes to be centered horizontally
        screen_width = stdscr.getmaxyx()[1]
        box_width = len(self.boxes[0].shape)
        start_x = self.calculate_start_x(screen_width, box_width)

        # Animation loop
        while True:
            stdscr.clear()

            # Display the message at the upper left corner
            self.display_message(stdscr)

            # Display the number and boxes
            for i in range(self.num_boxes):
                self.display_number(stdscr, i, start_x, box_width)
                self.display_boxes(stdscr, start_x, box_width)

            # Display the moving "o"
            self.display_o(stdscr, start_x, box_width)

            # Refresh the screen
            stdscr.refresh()

            # Check for keypress
            key = stdscr.getch()
            
            self.adjust_refresh_rate(key)

            if should_continue := self.handle_keypress(key):
                # Pause for a short duration
                time.sleep(0.1)
            else:
                break

if __name__ == "__main__":
    num_boxes = 10
    box_shapes = ["[ ]"] * num_boxes  # List of box shapes (e.g., "[ ]", "( )", "| |")
    boxes = [Box(shape) for shape in box_shapes]

    animation = TerminalAnimation(num_boxes, boxes)
    curses.wrapper(animation.main)
