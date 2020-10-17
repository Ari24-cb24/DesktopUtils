import os
import tkinter as tk
import tkinter.font
import requests
import datetime
import io

from PIL import Image, ImageTk
from dotenv import load_dotenv
load_dotenv()

class Widget:
    REFRESH = False
    RESIZE = [False, False]
    BAR_COLOR = "black"
    ROOT: tk.Tk
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
        self.x = None
        self.y = None

    def __button_press(self, event):
        self.x = event.x
        self.y = event.y

    def __move_window(self, event):
        if not self.windowX or not self.windowY:
            return

        deltax = event.x - self.windowX
        deltay = event.y - self.windowY
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry("+%s+%s" % (x, y))

class WeatherWidget:
    REFRESH = True

    iconLabel: tk.Label
    temperature: tk.Label
    description: tk.Label
    cloudPercent: tk.Label

    def __init__(self, root):
        self.frame = tk.Frame(root, width=200, height=200)
        self.api_key = os.environ["WEATHER_API_KEY"]
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/"
        self.data = {
            "city_name": "Offenbach",
            "appid": self.api_key
        }
        self.fmt = "%d.%m.%Y|%H:%M:%S"

    def __make_request(self):
        r = requests.get(self.BASE_URL + "weather?q={city_name}&appid={appid}&lang=DE&units=metric"
                         .replace("{city_name}", self.data["city_name"])
                         .replace("{appid}", self.data["appid"]))

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

    def refresh(self):
        result = self.__make_request()

        icon = io.BytesIO(requests.get(result["weather"]["icon"]).content)
        icon = Image.open(icon)
        icon = ImageTk.PhotoImage(icon)
        icon = icon._PhotoImage__photo.zoom(2)

        self.iconLabel.configure(image=icon)
        self.iconLabel.photo = icon

        self.temperature.configure(text=str(round(result["main"]["temp"])) + "°C")
        self.description.configure(text=result["weather"]["description"], font=tk.font.Font(family="Courier", size=12 if len(result["weather"]["description"]) <= 22 else 10))
        self.cloudPercent.configure(text="WM: " + str(result["clouds"]["percent"]) + "%")

    def run(self):
        result = self.__make_request()

        icon = io.BytesIO(requests.get(result["weather"]["icon"]).content)
        icon = Image.open(icon)
        icon = ImageTk.PhotoImage(icon)
        icon = icon._PhotoImage__photo.zoom(2)

        self.iconLabel = tk.Label(self.frame, image=icon)
        self.iconLabel.photo = icon
        self.iconLabel.place(x=self.frame.winfo_width()//2+50, y=-10)

        self.temperature = tk.Label(self.frame, font=tk.font.Font(family="comicsansms", size=11), text=str(round(result["main"]["temp"])) + "°C")
        self.temperature.place(x=150, y=16)

        self.description = tk.Label(self.frame, font=tk.font.Font(family="Courier", size=12 if len(result["weather"]["description"]) <= 22 else 10), text=result["weather"]["description"])
        self.description.place(anchor="center", x=self.frame.winfo_width()//2+100, y=75)

        self.cloudPercent = tk.Label(self.frame, font=tk.font.Font(family="comicsansms", size=9), text="WM: " + str(result["clouds"]["percent"]) + "%")
        self.cloudPercent.place(x=1, y=10)

        self.frame.pack()

class DesktopUtils:
    def __init__(self):
        self.widgets = []

    def create_root(self, widget) -> tk.Tk:
        root = tk.Tk()
        root.overrideredirect(True)
        root.wm_resizable(widget.RESIZE)

        top_bar = tk.Frame(root, bg=widget.BAR_COLOR, height=25, width=200)

        xImage = tk.PhotoImage(file="./img/x.png")
        x = tk.Button(top_bar, image=xImage, borderwidth=0, highlightthickness=0, command=widget.quit)
        x.photo = xImage

        x.place(x=180, y=2)

        top_bar.bind("<ButtonRelease-1>", widget.__button_release)
        top_bar.bind("<ButtonPress-1>", widget.__button_press)
        top_bar.bind("<B1-Motion>", widget.__move_window)
        top_bar.pack(side=tk.TOP, anchor=tk.E)

        return root

    def add_widget(self, widget):
        self.widgets.append(widget)

    def refresh_widgets(self):
        for widget in self.widgets:
            if widget.REFRESH:
                widget.refresh()

        self.root.after(60*1000, self.refresh_widgets)

    def run(self):
        self.add_widget(WeatherWidget(self.root))

        for widget in self.widgets:
            widget.run()

        self.root.after(5000, self.refresh_widgets)

        self.root.mainloop()


if __name__ == '__main__':
    desktopUtils = DesktopUtils()
    desktopUtils.run()