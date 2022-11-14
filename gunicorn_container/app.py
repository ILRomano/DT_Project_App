from flask import Flask, request, render_template, redirect, url_for
from pathlib import Path
import os
import requests
import json

app = Flask(__name__)
global parsed_data
api_key = 'PMMS7MKLUALC9RQDGGY9ADMW6'
os.environ["BG_IMAGE"] = "wallpaper.jpg"


@app.route('/', methods=["GET", "POST"])
def main():
    global parsed_data
    if request.method == "GET":
        return render_template('home.html', bg_image=os.environ['BG_IMAGE'])
    else:
        city = request.form["city"]
        url = build_url(city)
        data = None  # deal with assignment warning
        try:
            data = requests.get(url)
            data.raise_for_status()

        except requests.exceptions.HTTPError:
            if 400 <= data.status_code < 500:
                return render_template("error.html", status="user_error")
            elif 500 <= data.status_code < 600:
                return render_template("error.html", status="server_error")
            else:
                return render_template("error.html", status="unknown_error")

        parsed_data = prepare(data.json())
        save_data(parsed_data, city)
        return render_template("weather.html", data=parsed_data, bg_image=os.environ['BG_IMAGE'])


@app.route('/history', methods=["GET", "POST"])
def history_download():
    data_folder = Path(__file__).parent.joinpath("static/history")
    file_paths = [f for f in os.listdir(data_folder)]
    return render_template("history.html", paths=file_paths, bg_image=os.environ['BG_IMAGE'])


def save_data(weather_data, city):
    # create data folder if it doesnt exist
    data_folder = Path(__file__).parent.joinpath("static/history")
    if not data_folder.exists():
        data_folder.mkdir()
    with open("static/history/{}-{}".format(weather_data["date"][0], city) + '.txt', "w") as f:
        json.dump(weather_data, f, indent=4, ensure_ascii=False)


def build_url(city):
    return "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" \
           + str(city) + "/next7days?unitGroup=metric&include=hours&key=" + api_key + "&contentType=json"


def prepare(data):
    """
    turns the received data into a dictionary of weather information
    :param data: json string to be parsed
    :return: dictionary of the parsed data
    """
    date = []
    night_temp = []
    day_temp = []
    humidity = []
    location = data["resolvedAddress"]

    for i in range(7):
        day_temp.append(data["days"][i]["hours"][12]["temp"])
        night_temp.append(data["days"][i]["hours"][0]["temp"])
        humidity.append(data["days"][i]["humidity"])
        date.append(data["days"][i]["datetime"])

    d = {"location": location, "date": date, "day_temp": day_temp, "night_temp": night_temp, "humidity": humidity}

    return d


if __name__ == "__main__":
    app.run(host="0.0.0.0")
