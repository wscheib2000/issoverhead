import requests
from datetime import datetime
import config
import smtplib

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

def is_overhead(iss_lat, iss_long):
    """Returns whether or not the ISS is overhead

    Args:
        iss_lat (float): Current latitude of ISS
        iss_long (float): Current longitude of ISS

    Returns:
        bool: True if ISS is overhead, False otherwise
    """
    return abs(iss_lat-config.MY_LAT) < 5 and abs(iss_long-config.MY_LONG) < 5

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

time_now = datetime.now()

if is_overhead(iss_latitude, iss_longitude):
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                connection.starttls() # Makes connection secure

                connection.login(user=config.EMAIL, password=config.PASSWORD)
                connection.sendmail(
                    from_addr=config.EMAIL,
                    to_addrs=config.EMAIL,
                    msg=f'Subject:Look Up!\n\n\nThe ISS is passing!'
                )

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



