🌦️ Weather App

A real-time Weather Application developed in Python as part of my Oasis Infobyte Internship – Task 4.

The application uses the OpenWeatherMap API to fetch and display current weather information, along with hourly and daily forecasts through a user-friendly Tkinter GUI.

🚀 Features

🌍 Search weather by city name or ZIP code

🌡️ Display current temperature

🔄 Switch between Celsius (°C) and Fahrenheit (°F)

💧 Display humidity percentage

💨 Display wind speed

☁️ Display current weather condition

🖼️ Weather icons based on current conditions

🕐 Next 6 hours weather forecast

📅 5-day weather forecast

📍 Automatic location detection using IP address

⚠️ Handles invalid city, API key, network, timeout, and empty-input errors

🖥️ All error messages are displayed inside the GUI


🛠️ Tech Stack

Python

Tkinter – GUI

Requests – API requests

Pillow (PIL) – Weather icons

OpenWeatherMap API – Weather data

ipinfo.io API – Automatic location detection


📁 Project Structure

Weather-App/
│
├── weather_app.py
└── README.md

🔑 API Configuration

Before running the application, add your OpenWeatherMap API key in weather_app.py:

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

Get your API key from [OpenWeatherMap](https://openweathermap.org/?utm_source=chatgpt.com).

💻 Installation

Install the required Python libraries:

pip install requests pillow

Then run:

python weather_app.py

📸 Application

The application provides a graphical interface where users can enter a location, retrieve real-time weather information, view forecasts, and change temperature units.

🎯 Internship Task

Organization: Oasis Infobyte
Task: Task 4 – Basic Weather App
Project: Weather App
Domain: Python Development

👨‍💻 Author

Sumit Kumar Patel

Developed as part of the Oasis Infobyte Internship Program.
