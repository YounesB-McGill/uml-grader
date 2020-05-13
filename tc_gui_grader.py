#!/usr/bin/env python3

import time
import pyautogui

# emergency exit program if mouse moved to upper-left
pyautogui.FAILSAFE = True

# all delays in seconds
INITIAL_DELAY = 12
SHORT_DELAY = 0.3
LONG_DELAY = 1
LONGER_DELAY = 4
CLICK_AND_HOLD_DELAY = 1.5

C = "click"
DC = "double_click"
H = "click-and-hold"

# in format x, y, action, delay after action
COORD_ACTIONS = [
    [1445, 325, C, SHORT_DELAY],
    [710, 416, C, SHORT_DELAY],
    [710, 416, C, SHORT_DELAY],
    [710, 416, C, SHORT_DELAY],
    [710, 416, C, SHORT_DELAY],
    [760, 670, DC, SHORT_DELAY],
    [760, 480, DC, LONG_DELAY],
    [866, 332, H, SHORT_DELAY],
    [856, 244, C, LONGER_DELAY],
    [1338, 218, C, SHORT_DELAY],
    [1190, 218, C, SHORT_DELAY],
    [1444, 322, C, SHORT_DELAY],
    [1070, 580, C, LONG_DELAY],
    [480, 216, C, LONG_DELAY],
    [1066, 332, H, SHORT_DELAY],
    [1054, 242, C, LONGER_DELAY],
    [1446, 624, C, LONG_DELAY],
]

def show_mouse_position():
    """
    Show mouse (x, y) coordiantes forever. From pyautogui documentation.
    """
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')


def main():
    time.sleep(INITIAL_DELAY)
    for e in COORD_ACTIONS:
        if e[2] == C:
            pyautogui.click(e[0], e[1])
        elif e[2] == DC:
            pyautogui.click(e[0], e[1], clicks=2)
        elif e[2] == H:
            pyautogui.mouseDown(e[0], e[1])
            time.sleep(CLICK_AND_HOLD_DELAY)
            pyautogui.mouseUp()
        time.sleep(e[3])
        


if __name__ == "__main__":
    main()

