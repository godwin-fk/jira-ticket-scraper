import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Define your Google credentials

GOOGLE_USERNAME = ''
GOOGLE_PASSWORD = ''
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (without a browser window)
driver = webdriver.Chrome(service=service, options=options)

def take_screenshot(step_name):
    driver.save_screenshot(f'screenshot_{step_name}.png')

try:
    logging.info('Navigating to Jira login page')
    driver.get('https://id.atlassian.com/login')
    take_screenshot('jira_login_page')

    logging.info('Clicking "Continue with Google" button')
    # google_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="google-sign-in-button"]'))
    # )
    # google_button.click()
    google_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'google-auth-button'))
    )
    google_button.click()

    take_screenshot('google_signin_button_clicked')

    logging.info('Switching to Google Sign-In window')
    driver.switch_to.window(driver.window_handles[-1])

    logging.info('Entering Google username')
    google_username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'identifierId'))
    )
    google_username_input.send_keys(GOOGLE_USERNAME)
    google_username_input.send_keys(Keys.RETURN)
    take_screenshot('Google_username_entered')
    
    logging.info('Entering okta username')
    google_username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'okta-signin-username'))
    )
    google_username_input.send_keys(GOOGLE_USERNAME)
    google_username_input.send_keys(Keys.RETURN)
    take_screenshot('okta_username_entered')

    logging.info('Entering okta password')
    google_password_input = WebDriverWait(driver, 10).until(
        # EC.element_to_be_clickable((By.NAME, 'password'))
        EC.element_to_be_clickable((By.ID, 'okta-signin-password'))
    )
    google_password_input.send_keys(GOOGLE_PASSWORD)
    google_password_input.send_keys(Keys.RETURN)
    take_screenshot('okta_password_entered')
    
    # submit_button = driver.find_element_by_css_selector('input[value="Send Push"]')
    # submit_button.click()
    wait = WebDriverWait(driver, 50)
    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Send Push"]'))
    )
    
    # Click the button
    submit_button.click()

    logging.info('Waiting for Jira page to load after Google Sign-In')
    time.sleep(20)
    take_screenshot('jira_logged_in')

    logging.info('Navigating to the desired Jira issue page')
    driver.get('https://fourkites.atlassian.net/browse/CCT-3477')
    time.sleep(50)
    take_screenshot('jira_issue_page')
    logging.info('Getting page source and parsing with BeautifulSoup')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    logging.info('Extracting titles')
    titles = [title.get_text() for title in soup.find_all(['h1'])]

    for idx, title in enumerate(titles, start=1):
        print(f"{idx}. {title}")
    
    logging.info('Extracting paragraphs')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    
    for idx, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {idx}: {paragraph}")

except Exception as e:
    logging.error(f'An error occurred: {e}')
    take_screenshot('error_occurred')

finally:
    logging.info('Closing the Selenium WebDriver')
    driver.quit()
