import os
import tkinter as tk
import tkinter.font
import json
import requests
import datetime
import io

from PIL import Image, ImageTk
from dotenv import load_dotenv
load_dotenv()

class WeatherWidget:
    def __init__(self, root):
        self.frame = tk.Frame(root, width=200, height=200)
        self.api_key = os.environ["WEATHER_API_KEY"]
        self.location = os.environ["CITY"]
        self.lang = os.environ["LANG"]
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/"
        self.data = {
            "city_name": self.location,
            "appid": self.api_key,
            "lang": self.lang
        }
        self.fmt = "%d.%m.%Y|%H:%M:%S"

    def __make_request(self):
        r = requests.get(self.BASE_URL + "weather?q={city_name}&appid={appid}&lang={lang}&units=metric"
                         .replace("{city_name}", self.data["city_name"])
                         .replace("{appid}", self.data["appid"])
                         .replace("{lang}", self.data["lang"]))

        data = r.json()

        del data["coord"]
        del data["base"]
        del data["dt"]
        del data["visibility"]
        del data["timezone"]
        del data["id"]
        del data["cod"]
        del data["main"]["temp_min"]
        del data["main"]["temp_max"]
        del data["main"]["pressure"]
        del data["sys"]["type"]
        del data["sys"]["id"]
        del data["wind"]["deg"]

        data["sys"]["sunrise"] = datetime.datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime(self.fmt)
        data["sys"]["sunset"] = datetime.datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime(self.fmt)
        data["clouds"]["percent"] = data["clouds"].pop("all")
        data["weather"] = data["weather"].pop(0)
        data["weather"]["icon"] = "http://openweathermap.org/img/w/" + data["weather"]["icon"] + ".png"
        data["sys"]["city"] = data.pop("name")

        del data["weather"]["id"]
        del data["weather"]["main"]

        return data

    def run(self):
        result = self.__make_request()
        
        icon = requests.get(result["weather"]["icon"])
        icon = icon.content
        icon = Image.open(io.BytesIO(icon))
        icon = ImageTk.PhotoImage(icon)
        icon = icon._PhotoImage__photo.zoom(2)

        iconLabel = tk.Label(self.frame, image=icon)
        iconLabel.photo = icon
        iconLabel.place(x=self.frame.winfo_width()//2+50, y=-10)

        tk.Label(self.frame, font=tk.font.Font(family="comicsansms", size=11), text=str(round(result["main"]["temp"])) + "°C")\
            .place(x=150, y=16)

        tk.Label(self.frame, font=tk.font.Font(family="Courier", size=12 if len(result["weather"]["description"]) <= 22 else 10), text=result["weather"]["description"])\
            .place(anchor="center", x=self.frame.winfo_width()//2+100, y=75)

        tk.Label(self.frame, font=tk.font.Font(family="comicsansms", size=9), text="WM: " + str(result["clouds"]["percent"]) + "%")\
            .place(x=1, y=10)

        self.frame.pack()

class DesktopUtils:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)

        with open("data.json", "r") as fh:
            d = json.load(fh)

        lastx, lasty = d["last_pos"]

        self.root.geometry(f"200x200+{lastx}+{lasty}")
        self.root.wm_resizable(False, False)

        self.top_bar = tk.Frame(self.root, bg="black", height=25, width=200)

        xImage = tk.PhotoImage(file="./img/x.png")
        x = tk.Button(self.top_bar, image=xImage, borderwidth=0, highlightthickness=0, command=self.quit)
        x.photo = xImage

        x.place(x=180, y=2)

        self.top_bar.bind("<ButtonRelease-1>", self._button_release)
        self.top_bar.bind("<ButtonPress-1>", self._button_press)
        self.top_bar.bind("<B1-Motion>", self.move_window)
        self.top_bar.pack(side=tk.TOP, anchor=tk.E)

        self.x = None
        self.y = None

        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def refresh_widgets(self):
        ow = self.widgets

        for widget in self.widgets:
            widget.frame.destroy()

        self.widgets = []
        for w in ow:
            self.add_widget(w)

    def quit(self):
        with open("data.json", "r") as fh:
            d = json.load(fh)

        d["last_pos"] = [self.root.winfo_x(), self.root.winfo_y()]

        with open("data.json", "w") as fh:
            json.dump(d, fh, indent=4)

        self.root.destroy()

    def move_window(self, event):
        if not self.x or not self.y:
            return

        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry("+%s+%s" % (x, y))

    def _button_press(self, event):
        self.x = event.x
        self.y = event.y

    def _button_release(self, _):
        self.x = None
        self.y = None

    def run(self):
        self.add_widget(WeatherWidget(self.root))

        for widget in self.widgets:
            widget.run()

        self.root.mainloop()


if __name__ == '__main__':
    desktopUtils = DesktopUtils()
    desktopUtils.run()
