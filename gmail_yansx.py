import imaplib
import email
import re

    
EMAIL = "sophalda0001@gmail.com"
PASSWORD = "ejkpiyiklewwvhvq"
IMAP_SERVER = "imap.gmail.com"

EMAIL_YANDEX = "nonosophal@yandex.com"  # ឈ្មោះអ៊ីមែល Yandex របស់អ្នក
PASSWORD_YANDEX = "ymhywnpiimzmlwpo"  # ពាក្យសម្ងាត់ Yandex
IMAP_SERVER_YANDEX = "imap.yandex.com"


def fetch_yandex_headers(name_to_search="nonosophal+1210942@yandex.com"):  # កំណត់ឈ្មោះដែលត្រូវស្វែងរក
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    for mail_id in reversed(mail_ids[-10:]):  # ស្វែងរកអ៊ីមែលចុងក្រោយ 10 ក្បាល
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # ចាប់យក "To" ហើយពិនិត្យឈ្មោះ
        to_field = msg.get("To")
        if to_field and name_to_search in to_field:  # ប្រើឈ្មោះដែលបានកំណត់
            # បើបានរកឃើញឈ្មោះដូចតម្រូវ
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                except:
                    pass

            # ស្វែងរក OTP
            otp_match = re.search(r"FB-(\d{5,6})", body)
            if otp_match:
                print(f"Found OTP: {otp_match.group()}")
            else:
                print("No OTP code found.")
            break  # បញ្ចប់ក្រោយស្វែងរកជោគជ័យ

    mail.logout()

if __name__ == "__main__":
    rrr=fetch_yandex_headers()
    print(rrr)




def yandex_OTp(name_gmail="nonosophal+43545345@yandex.com"):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    for mail_id in reversed(mail_ids[-10:]):  # Search the last 10 messages
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        to_field = msg.get("To")
        if to_field and name_gmail in to_field:  # Match only the name in 'To' header
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                except:
                    pass

            otp_match = re.search(r"FB-(\d{5,6})", body)
            if otp_match:
                print(f"Found OTP Code: {otp_match.group()}")
            else:
                print("No OTP code found.")
            break  # Stop after finding the first match

    mail.logout()


def fetch_gmail_headers(name_gmail="Dylan", first_gmail="Martin"):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    for mail_id in reversed(mail_ids[-10:]):
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        to_field = msg.get("To")
        if to_field and f"{name_gmail} {first_gmail}" in to_field:
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                except:
                    pass

            otp_match = re.search(r"FB-(\d{5,6})", body)
            mail.logout()
            if otp_match:
                return otp_match.group()
            else:
                return "No OTP code found."

    mail.logout()
    return "No matching email found."

def fetch_yandex_headers(name_gmail="Albert", first_gmail="Jones"):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER_YANDEX)
    mail.login(EMAIL_YANDEX, PASSWORD_YANDEX)
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    mail_ids = messages[0].split()

    for mail_id in reversed(mail_ids[-10:]):  # ស្វែងរកអ៊ីមែលចុងក្រោយ 10 ក្បាល
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # ចាប់យក "To" ហើយពិនិត្យឈ្មោះ
        to_field = msg.get("To")
        if to_field and f"{name_gmail} {first_gmail}" in to_field:
            # បើបានរកឃើញឈ្មោះដូចតម្រូវ
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                except:
                    pass

            # ស្វែងរក OTP
            otp_match = re.search(r"FB-(\d{5,6})", body)
            if otp_match:
                print(f"Found OTP: {otp_match.group()}")
            else:
                print("No OTP code found.")
            break  # បញ្ចប់ក្រោយស្វែងរកជោគជ័យ

    mail.logout()
