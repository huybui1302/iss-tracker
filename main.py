import requests
import smtplib
from datetime import datetime

longitude = ""
latitude = ""
password = ""

def is_iss_near():
    global longitude, latitude
    response1 = requests.get("http://api.open-notify.org/iss-now.json")
    response1.raise_for_status()
    data1 = response1.json()

    longitude = float(data1["iss_position"]["longitude"])
    latitude = float(data1["iss_position"]["latitude"])
    # iss_position = (longitude, latitude)
    if longitude in range(-75, -70) and latitude in range(40, 50):
        return True


parameters = {"lat": 45.501690, "lng": -73.567253, "formatted": 0}
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise = data["results"]["sunrise"]
sunset = data["results"]["sunset"]
sunrise_hour = int(sunrise.split("T")[1].split(":")[0])
sunset_hour = int(sunset.split("T")[1].split(":")[0])

now = datetime.now()

if is_iss_near() and sunset_hour <= now.hour or now.hour <= sunrise_hour:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="landerbui13@gmail.com", password=password)
        connection.sendmail(from_addr="landerbui13@gmail.com", to_addrs="huy.130297@gmail.com",
                            msg=f"Subject:ISS Tracker\n\nThe ISS is in the sky right now.\n"
                                f"Longitude: {longitude} and latitude: {latitude}.")
