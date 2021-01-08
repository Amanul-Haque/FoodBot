# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guCompanye on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
import smtplib
import pandas as pd
#


class SendInv(Action):

     def name(self) -> Text:
         return "action_send_inv"

     def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            to_mail = tracker.get_slot("email")
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            mail_content = '''Hi, Thankyou For shopping with us \n P.F.A. The Attached Invoce
            '''

#Setup the MIME
            message = MIMEMultipart()
            message['From'] = 'XYZEECompany'
            message['To'] = to_mail
            message['Subject'] = 'Invoice of your latest purchare from XYZEECompany.'
#The subject line
#The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            attach_file_name = 'D:\GoBaskt-Intern\Food CB\invoices\invoice.pdf'
            attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) #encode the attachment
#add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)


            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("sendergiftcard@gmail.com", "gift@123")
            text = message.as_string()
            s.sendmail("sendergiftcard@gmail.com", to_mail, text)
            s.quit()
            return []

class GenInv(Action):
    def name(self) -> Text:
        return "action_gen_inv"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        items = tracker.get_slot("dish")
        quant = tracker.get_slot("quant")
        id = tracker.get_slot("email")
        import os

        from tempfile import NamedTemporaryFile

        from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator

        os.environ["INVOICE_LANG"] = "en"

        client = Client('Valuable Customer')
        provider = Provider('XYZEE',bank_account='00000', bank_code='0000')
        creator = Creator('Amanul Haque')

        invoice = Invoice(client, provider, creator)
        invoice.currency_locale = 'en_US.UTF-8'
        for item, quantity in zip(items,quant):
            invoice.add_item(Item(quantity, 00, description=item))

        from InvoiceGenerator.pdf import SimpleInvoice

        pdf = SimpleInvoice(invoice)
        pdf.gen("D:\GoBaskt-Intern\Food CB\invoices\invoice.pdf", generate_qr_code=True)


        dispatcher.utter_message(text='Invoice Created')
        return []

class RepeatOrder(Action):
    def name(self) -> Text:
        return "action_repeat_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        items = tracker.get_slot("dish")
        quant = tracker.get_slot("quant")
        dispatcher.utter_message(text="Please confirm your order")
        for item, quantity in zip(items,quant):
                dispatcher.utter_message(text="\n {} X {}\n".format(item,quantity))



        return []
