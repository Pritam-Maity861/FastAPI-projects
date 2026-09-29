import base64

import mailtrap as mt

from app.config.settings import settings

mailtrap_client = mt.MailtrapClient(
    token=settings.MAILTRAP_TOKEN, sandbox=True, inbox_id=settings.MAILTRAP_INBOX
)


def send_todo_welcome_mail(recipient: str):
    mail = mt.Mail(
        sender=mt.Address(email=settings.MAILTRAP_SENDER),
        to=[
            mt.Address(email=recipient),
        ],
        subject="welcome to my todo world!!",
        text="You can manage todo from here for free. ",
    )
    mailtrap_client.send(mail)


def send_todo_export_mail(
    recipient: str,
    file_data: bytes,
    filename: str,
):
    encoded_content = base64.b64encode(file_data).decode("utf-8")

    mail = mt.Mail(
        sender=mt.Address(email=settings.MAILTRAP_SENDER),
        to=[mt.Address(email=recipient)],
        subject="Your Todo list",
        text="Please find your todo export list attached.",
        attachments=[
            mt.Attachment(
                content=encoded_content,
                filename=filename,
                mimetype="application/json",
            )
        ],
    )

    mailtrap_client.send(mail)
