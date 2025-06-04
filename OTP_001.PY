import email
from email.header import decode_header
import imaplib
import random
import re
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




options = Options()
options.add_argument("--incognito")
options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 9; Mobile) AppleWebKit/537.36 Chrome/91.0.4472.77 Mobile Safari/537.36")
options.add_argument('--disable-gpu')
options.add_argument("--lang=en")
options.add_argument('--no-sandbox')
options.add_argument("--enable-unsafe-swiftshader")
options.add_argument('--app=https://m.facebook.com/reg')
options.add_argument('window-size=300,500')
driver = webdriver.Chrome(options=options)
#driver.get("https://accounts.google.com/signup")
# បញ្ចូល field តាម xpath ឬ css selectors (បន្ថែម code simulate human-like)
# Clear cookies, handle waits, និង CAPTCHA ត្រូវដោះស្រាយ manually ឬ OCR បន្ថែម
username = "sophalda0001@gmail.com"
password = "kchmmejykiodtixo"
yandex = "nonosophal"

# ចុងក្រោយបិទ driver
# driver.quit()
wait = WebDriverWait(driver, 15)


try:
    create_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Create new account"]')))
    create_button.click()

    first_names = ["Sophal", "Dara", "Maly", "Rithy", "Srey"]
    last_names = ["Chhoeun", "Sovann", "Kim", "Phan", "Nary"]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    first_name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="First name"]')))
    for char in first_name:
        first_name_input.send_keys(char)
        time.sleep(0.3)

    last_name_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Last name"]')))
    for char in last_name:
        last_name_input.send_keys(char)
        time.sleep(0.3)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

    birthday_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Birthday (0 year old)"]')))
    birthday_input.clear()
    birthday_input.send_keys("11112000")

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

    gender = 'Female'
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[aria-label="{gender}"]'))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

    mobile_prefixes = ['12', '15', '17', '77', '92', '93', '98', '99']
    prefix = random.choice(mobile_prefixes)  
    subscriber_number = random.randint(100000, 999999)  
    phone_number = f"+855{prefix}{subscriber_number}"
    phone_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Mobile number"]')))
    for digit in phone_number:
        phone_field.send_keys(digit)
        time.sleep(0.3)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

    try:
        continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Continue creating account"]')))
        continue_button.click()
    except:
        pass

    length = 12
    characters = string.ascii_uppercase + string.digits + "$#%&"
    password_fb = ''.join(random.choice(characters) for _ in range(length))

    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Password"]')))
    for char in password_fb:
        password_field.send_keys(char)
        time.sleep(0.3)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Not now"]'))).click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="I agree"]'))).click()

    time.sleep(30)

    driver.get('https://m.facebook.com/changeemail/')
    time.sleep(5)

    yandex_email = f"{yandex}+{subscriber_number}@yandex.com"

    email_input = driver.find_element(By.XPATH, "//input[@name='new' and @type='email']")
    for char in yandex_email:
        email_input.send_keys(char)
        time.sleep(0.4)

    time.sleep(5)
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit" and @value="Add"]')
    submit_button.click()

    time.sleep(10)

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select("INBOX")

    status, messages = imap.search(None, '(FROM "facebookmail.com")')
    email_ids = messages[0].split()
    max_emails = 10
    email_ids = email_ids[-max_emails:]

    found = False

    for email_id in reversed(email_ids):
        res, msg = imap.fetch(email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg_email = email.message_from_bytes(response[1])
                to_raw = msg_email.get("To")
                subject_raw = msg_email.get("Subject")

                if isinstance(to_raw, bytes):
                    to_clean = to_raw.decode('utf-8', errors='ignore')
                else:
                    to_clean = to_raw

                if isinstance(subject_raw, bytes):
                    parts = decode_header(subject_raw)
                    subject_clean = ''
                    for part, enc in parts:
                        if isinstance(part, bytes):
                            subject_clean += part.decode(enc or 'utf-8', errors='ignore')
                        else:
                            subject_clean += part
                    subject_clean = subject_clean.strip()
                else:
                    subject_clean = subject_raw.strip()

                match = re.match(r'(.*)<.*>', to_clean)
                if match:
                    raw_name = match.group(1).strip().strip('"')
                    parts = decode_header(raw_name)
                    full_name = ''
                    for part, enc in parts:
                        if isinstance(part, bytes):
                            full_name += part.decode(enc or 'utf-8', errors='ignore')
                        else:
                            full_name += part
                    full_name = full_name.strip()

                    parts = full_name.split()
                    if len(parts) >= 2:
                        first_name_mail = " ".join(parts[:-1])
                        last_name_mail = parts[-1]
                    else:
                        first_name_mail = full_name
                        last_name_mail = ""
                else:
                    first_name_mail = ""
                    last_name_mail = ""

                if first_name_mail == first_name and last_name_mail == last_name:
                    digits = re.findall(r'\d+', subject_clean)
                    if digits:
                        code = digits[-1]
                        print(f"Match: {first_name_mail} {last_name_mail} |mail OTP {code}")

                        last_5_chars = code[-5:]

                        input_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="m_conf_cliff_root_id"]/div/div/form/div/input')))
                        for char in last_5_chars:
                            input_element.send_keys(char)
                            time.sleep(0.1)

                        confirm_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Confirm')]")))
                        confirm_link.click()
                        time.sleep(15)
                        found = True
                        break
                    else:
                        print(f"No digits found in subject: {subject_clean}")
                else:
                    print(f"Skipped: {first_name_mail} {last_name_mail}")
        if found:
            break

    imap.logout()

except Exception as e:
    print("Error:", e)

driver.quit()
