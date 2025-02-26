from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class LoginPage:

    # Page Object
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[text()='Sign in']")
        self.error_labels = (By.XPATH, "//label[@role='alert' and contains(@class, 'text-danger')]")

    def login(self, email, password):
        # Input email
        self.driver.find_element(*self.email_field).clear()
        self.driver.find_element(*self.email_field).send_keys(email)
        
        # Input Password
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(password)
        
        # Klik Button Login
        self.driver.find_element(*self.login_button).click()

    # Get error Messages
    def get_error_messages(self):
        error_elements = self.driver.find_elements(*self.error_labels)
        return [error.text for error in error_elements]
