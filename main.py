import smtplib
import time

import requests
from datetime import datetime
from email.mime.text import MIMEText

my_email = ""
send_to = ""
MY_LAT = 39.960491 # Your latitude
MY_LONG = -75.262779 # Your longitude
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}
#---------------------ISS location---------------------------------------------------
def iss_over_head():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT -5 <= iss_latitude <= MY_LAT +5 and MY_LONG +5 <= iss_longitude <= MY_LONG: #CHECKING MY DIRECTIONS WITH THE ISS
            return True

#-----------------NightTime----------------------------------------------------
def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True
#-----------------Send Email---------------------------------------------------
while True:
    time.sleep(60)
    if iss_over_head() and is_night():
        msg = MIMEText("Check the sky the ISS is near your location")
        msg['Subject'] = 'Location of ISS'
        msg['From'] = my_email
        msg['To'] = send_to
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
         connection.starttls()
         connection.login(my_email, "vecjkbgzfbsufymx")
         connection.sendmail(my_email,send_to, msg.as_string())








