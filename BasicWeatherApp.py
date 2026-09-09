import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
from collections import defaultdict

API_KEY = "a0b46f4bd14d56510d9c5bab911a313b"

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
IP_URL = "https://ipinfo.io/json"

unit = "metric"
current_data = None
current_icon = None


def get_weather(city=None):
    global current_data, current_icon

    if city is None:
        city = city_entry.get().strip()

    if not city:
        show_error("Please enter a city name or ZIP code.")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
}

    try:
        response = requests.get(CURRENT_URL, params=params, timeout=10)

        if response.status_code == 404:
            show_error("City not found.")
            return

        if response.status_code == 401:
            show_error("Invalid API key.")
            return

        response.raise_for_status()

        current_data = response.json()

        display_current_weather(current_data)
        get_forecast(city)

    except requests.exceptions.Timeout:
        show_error("Network timeout. Please try again.")

    except requests.exceptions.ConnectionError:
        show_error("No internet connection.")

    except requests.exceptions.RequestException:
        show_error("Unable to fetch weather data.")


def display_current_weather(data):
    global current_icon

    city_name = data["name"]
    country = data["sys"]["country"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    condition = data["weather"][0]["description"]
    icon_code = data["weather"][0]["icon"]

    if unit == "metric":
        temp_text = f"{temperature:.1f} °C"
        feels_text = f"Feels like: {feels_like:.1f} °C"
        wind_text = f"{wind:.1f} m/s"
    else:
        temp_text = f"{temperature:.1f} °F"
        feels_text = f"Feels like: {feels_like:.1f} °F"
        wind_text = f"{wind:.1f} mph"

    location_label.config(text=f"{city_name}, {country}")
    temperature_label.config(text=temp_text)
    feels_label.config(text=feels_text)
    condition_label.config(text=condition.title())
    humidity_label.config(text=f"Humidity: {humidity}%")
    wind_label.config(text=f"Wind: {wind_text}")
    error_label.config(text="")

    try:
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, timeout=10)
        image = Image.open(BytesIO(icon_response.content))
        image = image.resize((100, 100))
        current_icon = ImageTk.PhotoImage(image)
        icon_label.config(image=current_icon)

    except:
        icon_label.config(image="")


def get_forecast(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": unit
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)

        if response.status_code != 200:
            show_error("Unable to load forecast.")
            return

        data = response.json()
        forecast_list = data["list"]

        display_hourly_forecast(forecast_list)
        display_daily_forecast(forecast_list)

    except requests.exceptions.Timeout:
        show_error("Forecast request timed out.")

    except requests.exceptions.RequestException:
        show_error("Unable to load forecast.")


def display_hourly_forecast(forecast_list):
    for widget in hourly_frame.winfo_children():
        widget.destroy()

    for item in forecast_list[:2]:
        create_forecast_card(hourly_frame, item)


def display_daily_forecast(forecast_list):
    for widget in daily_frame.winfo_children():
        widget.destroy()

    daily_data = defaultdict(list)

    for item in forecast_list:
        date = item["dt_txt"].split(" ")[0]
        daily_data[date].append(item)

    count = 0

    for date, items in daily_data.items():
        if count >= 5:
            break

        temperatures = [item["main"]["temp"] for item in items]
        weather = items[len(items) // 2]["weather"][0]
        icon = weather["icon"]

        avg_temp = sum(temperatures) / len(temperatures)
        condition = weather["description"]

        card = tk.Frame(
            daily_frame,
            bg="#ffffff",
            bd=1,
            relief="solid",
            width=150,
            height=150
        )
        card.pack(side="left", padx=5, pady=5)
        card.pack_propagate(False)

        date_text = datetime.strptime(date, "%Y-%m-%d").strftime("%a\n%d %b")

        tk.Label(
            card,
            text=date_text,
            font=("Arial", 10, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        try:
            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
            response = requests.get(icon_url, timeout=5)
            image = Image.open(BytesIO(response.content))
            image = image.resize((50, 50))
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(card, image=photo, bg="#ffffff")
            label.image = photo
            label.pack()

        except:
            pass

        unit_symbol = "°C" if unit == "metric" else "°F"

        tk.Label(
            card,
            text=f"{avg_temp:.1f} {unit_symbol}",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack()

        tk.Label(
            card,
            text=condition.title(),
            font=("Arial", 8),
            bg="#ffffff"
        ).pack()

        count += 1


def create_forecast_card(parent, item):
    time = datetime.fromtimestamp(item["dt"]).strftime("%I:%M %p")
    temperature = item["main"]["temp"]
    condition = item["weather"][0]["description"]
    icon_code = item["weather"][0]["icon"]

    card = tk.Frame(
        parent,
        bg="#ffffff",
        bd=1,
        relief="solid",
        width=130,
        height=160
    )
    card.pack(side="left", padx=5, pady=5)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=time,
        font=("Arial", 10, "bold"),
        bg="#ffffff"
    ).pack(pady=5)

    try:
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(icon_url, timeout=5)
        image = Image.open(BytesIO(response.content))
        image = image.resize((50, 50))
        photo = ImageTk.PhotoImage(image)

        icon = tk.Label(card, image=photo, bg="#ffffff")
        icon.image = photo
        icon.pack()

    except:
        pass

    symbol = "°C" if unit == "metric" else "°F"

    tk.Label(
        card,
        text=f"{temperature:.1f} {symbol}",
        font=("Arial", 12, "bold"),
        bg="#ffffff"
    ).pack()

    tk.Label(
        card,
        text=condition.title(),
        font=("Arial", 8),
        bg="#ffffff",
        wraplength=110
    ).pack()


def toggle_unit():
    global unit

    if unit == "metric":
        unit = "imperial"
        unit_button.config(text="Switch to °C")
    else:
        unit = "metric"
        unit_button.config(text="Switch to °F")

    if current_data:
        city = current_data["name"]
        get_weather(city)


def auto_location():
    try:
        response = requests.get(IP_URL, timeout=10)
        response.raise_for_status()

        data = response.json()

        city = data.get("city")

        if city:
            city_entry.delete(0, tk.END)
            city_entry.insert(0, city)
            get_weather(city)
        else:
            show_error("Could not detect your location.")

    except requests.exceptions.Timeout:
        show_error("Location request timed out.")

    except requests.exceptions.RequestException:
        show_error("Could not detect your location.")


def show_error(message):
    error_label.config(text=message)
    location_label.config(text="Weather Information")
    temperature_label.config(text="--")
    feels_label.config(text="")
    condition_label.config(text="")
    humidity_label.config(text="")
    wind_label.config(text="")

    icon_label.config(image="")

    for widget in hourly_frame.winfo_children():
        widget.destroy()

    for widget in daily_frame.winfo_children():
        widget.destroy()


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Weather App")
root.geometry("900x750")
root.resizable(False, False)
root.configure(bg="#eaf4ff")

title = tk.Label(
    root,
    text="Weather App",
    font=("Arial", 28, "bold"),
    bg="#eaf4ff"
)
title.pack(pady=15)

search_frame = tk.Frame(root, bg="#eaf4ff")
search_frame.pack()

city_entry = tk.Entry(
    search_frame,
    font=("Arial", 14),
    width=30
)
city_entry.pack(side="left", padx=5)

weather_button = tk.Button(
    search_frame,
    text="Get Weather",
    font=("Arial", 11, "bold"),
    command=get_weather
)
weather_button.pack(side="left", padx=5)

location_button = tk.Button(
    search_frame,
    text="Use My Location",
    font=("Arial", 11),
    command=auto_location
)
location_button.pack(side="left", padx=5)

unit_button = tk.Button(
    root,
    text="Switch to °F",
    font=("Arial", 10),
    command=toggle_unit
)
unit_button.pack(pady=10)

error_label = tk.Label(
    root,
    text="",
    font=("Arial", 11),
    bg="#eaf4ff"
)
error_label.pack()

weather_box = tk.Frame(
    root,
    bg="#ffffff",
    bd=2,
    relief="groove",
    width=700,
    height=210
)
weather_box.pack(pady=10)
weather_box.pack_propagate(False)

location_label = tk.Label(
    weather_box,
    text="Weather Information",
    font=("Arial", 20, "bold"),
    bg="#ffffff"
)
location_label.pack(pady=5)

icon_label = tk.Label(
    weather_box,
    bg="#ffffff"
)
icon_label.pack()

temperature_label = tk.Label(
    weather_box,
    text="--",
    font=("Arial", 24, "bold"),
    bg="#ffffff"
)
temperature_label.pack()

feels_label = tk.Label(
    weather_box,
    text="",
    font=("Arial", 10),
    bg="#ffffff"
)
feels_label.pack()

condition_label = tk.Label(
    weather_box,
    text="",
    font=("Arial", 12),
    bg="#ffffff"
)
condition_label.pack()

humidity_label = tk.Label(
    weather_box,
    text="",
    font=("Arial", 10),
    bg="#ffffff"
)
humidity_label.pack()

wind_label = tk.Label(
    weather_box,
    text="",
    font=("Arial", 10),
    bg="#ffffff"
)
wind_label.pack()

# Hourly Forecast
tk.Label(
    root,
    text="Next 6 Hours",
    font=("Arial", 16, "bold"),
    bg="#eaf4ff"
).pack(pady=5)

hourly_frame = tk.Frame(root, bg="#eaf4ff")
hourly_frame.pack()

# Daily Forecast
tk.Label(
    root,
    text="5 Day Forecast",
    font=("Arial", 16, "bold"),
    bg="#eaf4ff"
).pack(pady=10)

daily_frame = tk.Frame(root, bg="#eaf4ff")
daily_frame.pack()

root.mainloop()