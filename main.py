from datetime import datetime
import pandas
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_EMAIL = "ragzuris@gmail.com"
PASSWORD = "thbufcayqzcyvjyo"

today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"
    with open(file_path, encoding='utf-8') as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    message = MIMEMultipart()
    message["From"] = MY_EMAIL
    message["To"] = birthday_person["email"]
    message["Subject"] = "Mutlu Yıllar!"
    message.attach(MIMEText(contents, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=birthday_person["email"],
            msg=message.as_string()
        )
