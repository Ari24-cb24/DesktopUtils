import tkinter as tk

class Widget:
    REFRESH = False
    RESIZE = [False, False]
    START_POS = [0, 0]
    SIZE = [200, 200]
    BAR_COLOR = "black"
    root: tk.Tk
    frame: tk.Frame
    windowX = None
    windowY = None

    def __init__(self, root):
        self.root = root

    def refresh(self):
        pass

    def run(self):
        pass

    def quit(self):
        self.root.destroy()

    def __button_release(self, _):
        self.windowX = None
        self.windowY = None

    def __button_press(self, event):
        self.windowX = event.x
        self.windowY = event.y

    def __move_window(self, event):
        if not self.windowX or not self.windowY:
            return

        deltax = event.x - self.windowX
        deltay = event.y - self.windowY
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry("+%s+%s" % (x, y))