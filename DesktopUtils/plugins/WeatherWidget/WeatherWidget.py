import tkinter as tk
import tkinter.font
import os
import requests
import datetime
import io
from PIL import Image, ImageTk
from Widget import Widget

class WeatherWidget(Widget):
    REFRESH = True

    iconLabel: tk.Label
    temperature: tk.Label
    description: tk.Label
    cloudPercent: tk.Label

    def __init__(self, root):
        super().__init__(root)
        self.frame = tk.Frame(root, width=200, height=200)
        self.api_key = os.environ["WEATHER_API_KEY"]
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/"
        self.lang = os.environ["LANG"]
        self.city = os.environ["CITY"]
        self.data = {
            "city_name": self.city,
            "appid": self.api_key
        }
        self.fmt = "%d.%m.%Y|%H:%M:%S"

    def __make_request(self):
        r = requests.get(self.BASE_URL + "weather?q={city_name}&appid={appid}&lang={lang}&units=metric"
                         .replace("{city_name}", self.data["city_name"])
                         .replace("{appid}", self.data["appid"])
                         .replace("{lang}", self.lang))

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
        self.root.mainloop()