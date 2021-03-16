from core.mailing import send_gmail

def announce_if_winner():
    # If End Time of a Campaign <= 1:00 and Campaign Not Closed (campaign_closed: boolean field) do:
    # If no winner, choose winner
    # Send a mail to the winner
    send_gmail("Cron Job", "This is a django cron job", "pro.ajibolaojo@gmail.com")