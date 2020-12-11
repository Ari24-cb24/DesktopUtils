import tkinter as tk
from dotenv import load_dotenv
import os
import importlib
from infi.systray import SysTrayIcon
from win32_adapter import *
import threading
import sys
import time
load_dotenv()

class DesktopUtils:
    VERSION = "1.0"
    
    def __init__(self):
        self.widgets = {}
        self.running_gui = False
        self.refresh_thread = threading.Thread(target=self.refresh_widgets)

        menu = (
            ("Open", "./img/icon.ico", self._open_gui),
            ("Exit", "./img/x.ico", self.__shutdown),
        )

        self.stray = SysTrayIcon("./img/icon.ico", "DeskopUtils", menu_options=menu)

    def __shutdown(self, *_):
        def stop():
            DestroyWindow(self.stray._hwnd)

            for widget in self.widgets:
                instance = self.widgets[widget]["instance"]

                try:
                    instance.root.destroy()
                except RuntimeError:
                    pass

        t = threading.Thread(target=stop)
        t.start()

        self.refresh_thread.join()
        sys.exit(0)

    def _run_stray(self):
        self.stray.start()
    
    def _open_gui(self, _):
        if self.running_gui:
            return

        self.running_gui = True

        root = tk.Tk()
        root.geometry("500x500")
        root.title("DesktopUtils V" + self.VERSION)

        def close_win():
            root.destroy()
            self.running_gui = False
            self._run_stray()

        root.protocol("WM_DELETE_WINDOW", close_win)

        root.mainloop()
    
    def create_root(self, widget) -> tk.Tk:
        root = tk.Tk()
        root.overrideredirect(True)
        root.wm_resizable(*widget.RESIZE)
        root.geometry(f"{widget.SIZE[0]}x{widget.SIZE[1]}+{widget.START_POS[0]}+{widget.START_POS[1]}")

        return root

    def add_widget(self, info, widget):
        generalInfo = info.copy()
        generalInfo.pop("NAME")

        self.widgets[info["NAME"]] = {
            "information": generalInfo,
            "plugin": widget
        }

    def refresh_widgets(self):
        time.sleep(10)

        while True:
            for widget in self.widgets:
                if self.widgets[widget]["instance"].REFRESH:
                    self.widgets[widget]["instance"].refresh()

            time.sleep(20)

    def _create_bar(self, root, w_):
        top_bar = tk.Frame(root, bg=w_.BAR_COLOR, height=25, width=200)

        xImage = tk.PhotoImage(file="./img/x.png")
        x = tk.Button(top_bar, image=xImage, borderwidth=0, highlightthickness=0, command=w_.quit)
        x.photo = xImage

        x.place(x=180, y=2)

        top_bar.bind("<ButtonRelease-1>", getattr(w_, "_Widget__button_release"))
        top_bar.bind("<ButtonPress-1>", getattr(w_, "_Widget__button_press"))
        top_bar.bind("<B1-Motion>", getattr(w_, "_Widget__move_window"))
        top_bar.pack(side=tk.TOP, anchor=tk.E)

        return top_bar

    def run(self):
        pluginPaths = next(os.walk("./plugins/"))[1]
        for folderName in pluginPaths:
            path = "./plugins/" + folderName

            try:
                with open(path + "/info.meda", "r") as fh:
                    infoMeDa = fh.readlines()
            except FileNotFoundError:
                print("Could not load " + folderName + ". info.meda is missing!")
                continue

            pluginInfo = {
                "NAME": None,
                "AUTHOR": None,
                "DESCRIPTION": None,
                "VERSION": None,
                "MAIN": None,
                "CLASS": None
            }

            for line in infoMeDa:
                key, value = line.split("=")

                if key in pluginInfo:
                    pluginInfo[key] = value.replace("\n", "").replace(" ", "_")

            assert pluginInfo["MAIN"] is not None

            path = path[2:].replace("/", ".")
            main_filename = pluginInfo["MAIN"].replace(".py", "")
            main_ = importlib.import_module(".." + main_filename, path)

            class_ = getattr(main_, pluginInfo["CLASS"])

            self.add_widget(pluginInfo, class_)

        self._run_stray()

        self.refresh_thread.start()

        for widget in self.widgets:
            root = self.create_root(self.widgets[widget]["plugin"])
            w = self.widgets[widget]["plugin"](root)
            self.widgets[widget]["instance"] = w

            self._create_bar(root, w)

            w.run()


if __name__ == '__main__':
    desktopUtils = DesktopUtils()
    desktopUtils.run()