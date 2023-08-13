from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import CHROME_PROFILE_PATH

# Function to set up the WebDriver
def setup_driver():
    # Set up Chrome driver with the specified profile path
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)

    # Implicit wait to handle page loading delays
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com/")
    return driver

# Function to wait for QR code scan
def wait_for_qr_scan(driver):
    # Wait for QR code to be scanned only once
    qr_scanned = False
    while not qr_scanned:
        user_input = input("Scan the QR code and press Enter when ready (or type 'done' if already scanned): ").strip().lower()
        if user_input == 'done':
            qr_scanned = True


# Function to add participants to the group
def add_participants(driver,participants):
    # Locate the search box
    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/span/div/div/div[1]/div/div/div[2]/input')))

    for participant in participants:
        try:
            #Clear the search box
            search_box.clear()
            #Enter participant name
            search_box.send_keys(participant)
            search_box.send_keys(Keys.RETURN)

            # Wait for a brief moment before the next participant
            time.sleep(5)

            not_found_message = f"No contacts found"
            if not_found_message in driver.page_source:
               print(f"Participant '{participant}' not found.")


        except Exception as e:
            print(f"Error adding participant {participant}:{e}")

# Function to create a WhatsApp group
def create_group(driver,participants,group_name="Group"):
    #Locate and click the new chat button
    new_chat_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[4]/header/div[2]/div/span/div[3]/div/span')
    new_chat_btn.click()
    time.sleep(5)

    # Click on the new group option
    new_group_option= driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div[1]/div[2]')
    new_group_option.click()
    time.sleep(5)

    # Add participants using the add_participants function
    add_participants(driver,participants)

    # Click the arrow
    arrow_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/span/div/div/span/div/span')))
    arrow_button.click()
    time.sleep(5)

    # Enter the group name
    group_name_input = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/span/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div[1]/p')
    group_name_input.send_keys(group_name)
    time.sleep(5)

    # Click the create button
    create_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[1]/span/div/span/span/div/div/span/div/div')
    create_button.click()
    time.sleep(10)

# Function to send a message to a group
def send_message(driver,group_name,message):
    try:
        search_box = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/p')
        # Clear the search box
        search_box.clear()
        search_box.send_keys(group_name)
        search_box.send_keys(Keys.RETURN)

        chat_box_xpath = '/html/body/div[1]/div/div/div[4]/div/div[2]/div[1]/div/div/div[8]/div/div'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, chat_box_xpath))).click()

        message_box_xpath = '/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, message_box_xpath))).send_keys(message, Keys.ENTER)

        print(f'"{message}" sent to {group_name}')

        # Wait for a few seconds after sending the message
        time.sleep(5)
    except Exception as e:
        print("An error occurred while sending the message:", str(e))
