import requests
from datetime import datetime, timezone
import config
import smtplib
import time

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

def is_overhead():
    """Returns whether or not the ISS is overhead

    Args:
        iss_lat (float): Current latitude of ISS
        iss_long (float): Current longitude of ISS

    Returns:
        bool: True if ISS is overhead, False otherwise
    """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_lat = float(data["iss_position"]["latitude"])
    iss_long = float(data["iss_position"]["longitude"])

    return abs(iss_lat-config.MY_LAT) < 5 and abs(iss_long-config.MY_LONG) < 5

def is_dark(sunrise_hour, sunset_hour, time_now):
    """Returns whether or not it is currently dark

    Args:
        sunrise_hour (int): The hour the sun rises at my location
        sunset_hour (int): The hour the sun sets at my location
        time_now (datetime): The current time

    Returns:
        bool: True if it is dark now, False otherwise
    """
    parameters = {
        "lat": config.MY_LAT,
        "lng": config.MY_LONG,
        "formatted": 0
    }
    
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc)

    return time_now.hour < sunrise_hour or time_now.hour > sunset_hour

while True:
    if is_overhead() and is_dark():
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                    connection.starttls() # Makes connection secure

                    connection.login(user=config.EMAIL, password=config.PASSWORD)
                    connection.sendmail(
                        from_addr=config.EMAIL,
                        to_addrs=config.EMAIL,
                        msg=f'Subject:Look Up!\n\n\nThe ISS is passing!'
                    )
    time.sleep(60)