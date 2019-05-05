from mailjet_rest import Client
from django.conf import settings
from django.template.loader import render_to_string
from home.models import ContactPage, ReceiverEmails


def send_email(send_message_dict):
    contact_page = ContactPage.objects.live().in_menu().first()
    receivers = ReceiverEmails.objects.filter(page=contact_page.pk).all()
    receiver_emails = []
    for receiver in receivers:
        receiver_emails.append(
            {
                "Email": receiver.email
            }
        )
    mailjet = Client(
        auth=(
            settings.MJ_APIKEY_PUBLIC,
            settings.MJ_APIKEY_PRIVATE
        )
    )
    message = render_to_string(
        'email_template.html',
        context={
            'name': send_message_dict.get('name'),
            'phone_number': send_message_dict.get('phone_number'),
            'email': send_message_dict.get('email'),
            'message': (
                send_message_dict.get(
                    'message'
                ).replace(
                    "\r\n", "<br />"
                ).replace(
                    "\n", "<br />"
                )
            )
        }
    )
    data = {
      'FromEmail': settings.EMAIL_FROM,
      'FromName': settings.EMAIL_NAME,
      'Subject': send_message_dict.get('subject'),
      'Html-part': message,
      'Recipients': receiver_emails
    }
    result = mailjet.send.create(data=data)

    return result.json()
