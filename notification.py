import smtplib


def send_mail(
    from_gmail: str,
    to_gmail: str,
    gmail_password: str,
    meet_hour: float,
    time_until_meeting: int,
    first_name: str,
    last_name: str,
):
    message = f"Dear {first_name} {last_name}. You have scheduled a meeting for today at {meet_hour} o'clock, the meeting will start in {time_until_meeting} hours."
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(from_gmail, gmail_password)
        smtp.sendmail(from_gmail, to_gmail, message)



