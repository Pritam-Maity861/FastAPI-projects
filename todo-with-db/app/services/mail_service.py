import mailtrap as mt

from app.config.settings import settings

mailtrap_client = mt.MailtrapClient(
    token=settings.MAILTRAP_TOKEN, sandbox=True, inbox_id=settings.MAILTRAP_INBOX
)


def send_todo_welcome_mail(recipient: str):
    mail = mt.Mail(
        sender=mt.Address(email=settings.MAILTRAP_SENDER),
        to=[mt.Address(email=recipient),],
        subject="welcome to my todo world!!",
        text="You can manage todo from here for free. ",
    )
    mailtrap_client.send(mail)
