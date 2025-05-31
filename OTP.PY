import random
import string
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import imaplib
import email
from email.header import decode_header
import re

# បញ្ជីឈ្មោះ និងត្រកូល
first_names = ["Sophal", "Dara", "Maly", "Rithy", "Srey"]
last_names = ["Chhoeun", "Sovann", "Kim", "Phan", "Nary"]

def random_name():
    return random.choice(first_names), random.choice(last_names)

def clean_text(text):
    return text.decode('utf-8', errors='ignore') if isinstance(text, bytes) else text

def decode_field(text):
    parts = decode_header(text)
    return ''.join(
        part.decode(enc or 'utf-8', errors='ignore') if isinstance(part, bytes) else part
        for part, enc in parts
    ).strip()

def parse_to_name(to_header):
    match = re.match(r'(.*)<.*>', to_header)
    if match:
        full_name = decode_field(match.group(1).strip().strip('"'))
        parts = full_name.split()
        if len(parts) >= 2:
            return " ".join(parts[:-1]), parts[-1]
        else:
            return full_name, ""
    return "", ""

def fetch_and_confirm_code(username, password, input_first, input_last, driver, max_emails=10):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select("INBOX")

    status, messages = imap.search(None, '(FROM "facebookmail.com")')
    email_ids = messages[0].split()[-max_emails:]

    for email_id in reversed(email_ids):
        res, msg = imap.fetch(email_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg_email = email.message_from_bytes(response[1])
                to_raw = msg_email.get("To")
                subject_raw = msg_email.get("Subject")

                to_clean = clean_text(to_raw)
                subject_clean = decode_field(clean_text(subject_raw))

                first_name, last_name = parse_to_name(to_clean)

                if first_name == input_first and last_name == input_last:
                    digits = re.findall(r'\d+', subject_clean)
                    if digits:
                        code = digits[-1]
                        print(f"Match: {first_name} {last_name} | Code: {code}")

                        last_5_chars = code[-5:]
                        input_element = driver.find_element(By.XPATH, '//*[@id="m_conf_cliff_root_id"]/div/div/form/div/input')
                        for char in last_5_chars:
                            input_element.send_keys(char)
                            time.sleep(0.1)

                        confirm_link = driver.find_element(By.XPATH, "//a[contains(text(),'Confirm')]")
                        confirm_link.click()
                        time.sleep(15)
                        imap.logout()
                        return True
                    else:
                        print(f"No digits found in subject: {subject_clean}")
                else:
                    print(f"Skipped: {first_name} {last_name}")

    imap.logout()
    return False

def generate_random_phone_number():
    return random.choice(['096', '097', '088', '071']) + str(random.randint(1000000, 9999999))

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + random.choice(['@', '#']) + str(random.randint(1000, 9999))

def create_account(driver, username, password):
    wait = WebDriverWait(driver, 15)
    try:
        create_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Create new account"]')))
        create_button.click()

        first_name, last_name = random_name()
        birthday = "11112000"

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
        birthday_input.send_keys(birthday)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

        gender = 'Female'
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[aria-label="{gender}"]'))).click()

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

        phone_number = generate_random_phone_number()
        phone_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Mobile number"]')))
        for digit in phone_number:
            phone_field.send_keys(digit)
            time.sleep(0.3)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()

        try:
            continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Continue creating account"]')))
            continue_button.click()
        except TimeoutException:
            pass

        password_str = generate_random_password()
        password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Password"]')))
        for char in password_str:
            password_field.send_keys(char)
            time.sleep(0.3)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Next"]'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Not now"]'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="I agree"]'))).click()

        time.sleep(10)

        # Example Yandex email input - can be adjusted or removed
        id_thread = random.randint(1000000, 9999999)
        yandex_email = f"nonosophal+{id_thread}@yandex.com"
        print(f"Using email: {yandex_email}")

        email_input = driver.find_element(By.XPATH, "//input[@name='new' and @type='email']")
        for char in yandex_email:
            email_input.send_keys(char)
            time.sleep(0.4)

        time.sleep(5)
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit" and @value="Add"]')
        submit_button.click()

        time.sleep(10)

        # Confirm code from email
        success = fetch_and_confirm_code(username, password, first_name, last_name, driver, max_emails=10)

        if success:
            print("Code confirmed successfully.")
        else:
            print("No matching email found or no code to confirm.")

        driver.quit()
        print("Account created successfully")

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error in create_account: {e}")
    except Exception as e:
        print(f"Unexpected error in create_account: {e}")

def Open_in_a_row(instance_num, username, password):
    print(f"Thread {instance_num} started")

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument("--lang=en")
    options.add_argument('--no-sandbox')
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument('--app=https://m.facebook.com/reg')
    options.add_argument('window-size=300,450')
    options.add_argument(f'--window-position={instance_num * 350},0')
    options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 8.1.0; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36')

    service = Service(executable_path="webdriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    time.sleep(random.randint(2, 6))

    create_account(driver, username, password)

    driver.quit()
    print(f"Thread {instance_num} finished")

# Main thread loop
Number_range = 3  # Parallel browsers
loop_count = 2    # Loops
username = "your_email@gmail.com"  # Gmail for confirmation
password = "your_password"

for loop in range(loop_count):
    print(f"Starting loop {loop + 1}")
    threads = []

    for N in range(Number_range):
        thread = threading.Thread(target=Open_in_a_row, args=(N, username, password))
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for thread in threads:
        thread.join()

print("All loops completed.")
