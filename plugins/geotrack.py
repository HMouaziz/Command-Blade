"""A bunch of goelocation based function using ipinfo.io"""
import socket as soc
import ipinfo as ipinfo
import pytz
import requests
from InquirerPy import inquirer
from InquirerPy.base import Choice
from prettytable import PrettyTable
from datetime import datetime

from core.interface import Interface


class Plugin:
    @staticmethod
    def process():
        print('GeoTrack Plugin Loaded Successfully')

    @staticmethod
    def get_hook():
        ui_hook = {'ID': '05', 'module': 'geotrack', 'class': 'GeoTrack',
                   'method': 'geotrack_ui', 'choice_name': 'GeoTrack'}
        return ui_hook


class GeoTrack:
    style = Interface.get_custom_style()
    ipinfo_key = "5797a08455b34c"
    weather_key = "c19850557a13982ddd1453d657fc1452"
    details = {}

    @classmethod
    def geotrack_ui(cls):
        message = ''
        select = inquirer.select(
            message=message,
            choices=[
                Choice(value=1, name="Get location details."),
                Choice(value=2, name="Get location weather."),
                Choice(value=2, name="Get location weather data."),
                Choice(value=3, name="Get location time."),
                Choice(value=None, name="Exit"),
            ],
            default=None,
            style=cls.style,
            qmark="≻≻",
            amark="≻≻"
        ).execute()
        if select == 1:
            cls.get_location()
            cls.print_details(cls.details)
            cls.geotrack_ui()
        if select == 2:
            cls.get_location()
            x = cls.get_weather_data(cls.details)
            cls.print_weather_data(x)
            cls.geotrack_ui()
        if select == 3:
            cls.geotrack_ui()
        if select == 4:
            cls.get_location()
            time = cls.get_time(cls.details["timezone"])
            cls.print_time(time)
            cls.geotrack_ui()
        elif select is None:
            choices, instruction_data = Interface.get_menu_list()
            Interface.main_menu(choices, instruction_data)

    @classmethod
    def get_location(cls, ip=None):
        handler = ipinfo.getHandler(cls.ipinfo_key)
        details = handler.getDetails(ip)
        cls.details = details.all

    @classmethod
    def print_details(cls, details):
        x = PrettyTable()
        x.field_names = ["", "Details"]
        x.add_rows(
            [
                ["ip", details["ip"]],
                ["city", details["city"]],
                ["region", details["region"]],
                ["country", details["country"]],
                ["loc", details["loc"]],
                ["org", details["org"]],
                ["postal", details["postal"]],
                ["timezone", details["timezone"]],
            ]
        )
        print(x)

    @classmethod
    def get_time(cls, timezone):
        time = datetime.now(pytz.timezone(timezone))
        return time

    @classmethod
    def print_time(cls, time):
        print(f'It is {time.strftime("%I:%M:%S %Z on %A the %d of %B %G")}')

    @classmethod
    def get_gps_location(cls, host):
        s = soc.socket()
        port = 12345
        s.setsockopt(soc.SOL_SOCKET, soc.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        c, addr = s.accept()
        while True:
            return c.recv(2048).decode('ascii')

    @classmethod
    def get_weather_data(cls, details):
        lat, lon = details["loc"].split(",")
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={cls.weather_key}"
        response = requests.get(url)
        x = response.json()
        y = x["current"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        return current_temperature, current_pressure, current_humidity

    @classmethod
    def print_weather_data(cls, x):
        if x == "404":
            print("Error: API returned a 404 error.")
        else:
            print(" Temperature (in kelvin unit) = " +
                  str(x[0]) +
                  "\n atmospheric pressure (in hPa unit) = " +
                  str(x[1]) +
                  "\n humidity (in percentage) = " +
                  str(x[2]) +
                  "\n description = " +
                  str(x))


