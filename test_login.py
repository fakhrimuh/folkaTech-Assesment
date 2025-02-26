import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from login_page import LoginPage
import os

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Setup browser dengan mode incognito sebelum pengujian dimulai."""
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # Mode penyamaran
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://lapor.folkatech.com/")  # Ganti dengan URL login yang diuji

    def test_valid_login(self):
        print('Running Test Login Valid')
        login_page = LoginPage(self.driver)
        login_page.login("admin@example.com", "password")

        # Verifikasi apakah login berhasil dengan mengecek URL dashboard
        self.assertIn("dashboard", self.driver.current_url)

    def test_login_empty_fields(self):
        print('Running Test Login Empty Fields')
        login_page = LoginPage(self.driver)
        login_page.login("","")

        # Ambil pesan error dari halaman
        error_messages = login_page.get_error_messages()
        
        # Harus sesuai dengan UI (pesan pertama tanpa *, lainnya pakai *)
        expected_errors = [
            "Email harus diisi.",
            "* Email harus diisi.",
            "* Kata Sandi harus diisi."
        ]

        self.assertListEqual(error_messages, expected_errors, f"Pesan error tidak sesuai: {error_messages}")

    def test_login_with_only_email(self):
        print('Running Test Login Only Email')
        login_page = LoginPage(self.driver)
        login_page.login("admin@example.com", "")

        error_messages = login_page.get_error_messages()
        expected_errors = [
            "Kata Sandi harus diisi.",
            "* Kata Sandi harus diisi."
        ]

        self.assertListEqual(error_messages, expected_errors, f"Pesan error tidak sesuai: {error_messages}")

    def test_login_with_only_password(self):
        print('Running Test Login Only Password')
        login_page = LoginPage(self.driver)
        login_page.login("", "password")

        error_messages = login_page.get_error_messages()
        expected_errors = [
            "Email harus diisi.",
            "* Email harus diisi."
        ]

        self.assertListEqual(error_messages, expected_errors, f"Pesan error tidak sesuai: {error_messages}")

    def test_login_with_wrong_password(self):
        print('Running Test Login Wrong Password')
        login_page = LoginPage(self.driver)
        login_page.login("admin@example.com", "password1")


        error_messages = login_page.get_error_messages()
        expected_errors = "Login Gagal! Kata sandi salah."

        self.assertIn(expected_errors, error_messages, f"Pesan error tidak sesuai: {error_messages}")

    def test_login_with_wrong_email(self):
        print('Running Test Wrong Email')
        login_page = LoginPage(self.driver)
        login_page.login("admin1@example.com", "password")


        error_messages = login_page.get_error_messages()
        expected_errors = "Login Gagal! Akun tidak ada."

        self.assertIn(expected_errors, error_messages, f"Pesan error tidak sesuai: {error_messages}")

    def test_login_with_unregistered_account(self):
        print('Running Test Login With Unregistered Account')
        login_page = LoginPage(self.driver)
        login_page.login("LambdaAdminLongtitude@example.com", "password1")


        error_messages = login_page.get_error_messages()
        expected_errors = "Login Gagal! Akun tidak ada."

        self.assertIn(expected_errors, error_messages, f"Pesan error tidak sesuai: {error_messages}")

    def test_login_with_case_sensitive_password(self):
        print('Running Test Login With Unregistered Account')
        login_page = LoginPage(self.driver)
        login_page.login("admin@example.com", "passWorD")


        error_messages = login_page.get_error_messages()
        expected_errors = "Login Gagal! Kata sandi salah."


        self.assertIn(expected_errors, error_messages, f"Pesan error tidak sesuai: {error_messages}")

    def tearDown(self):
        outcome = self._outcome.result
        if outcome.errors or outcome.failures:
            test_method = self._testMethodName
            screenshot_dir = "screenshots"

            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            screenshot_path = os.path.join(screenshot_dir, f"{test_method}.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")

        self.driver.quit()

def suite():
    test_suite = unittest.TestSuite()
    # test_suite.addTest(TestLogin("test_valid_login"))  
    # test_suite.addTest(TestLogin("test_login_empty_fields")) 
    # test_suite.addTest(TestLogin("test_login_with_only_email"))
    # test_suite.addTest(TestLogin("test_login_with_only_password"))
    # test_suite.addTest(TestLogin("test_login_with_wrong_password"))
    # test_suite.addTest(TestLogin("test_login_with_wrong_email"))
    # test_suite.addTest(TestLogin("test_login_with_unregistered_account"))
    test_suite.addTest(TestLogin("test_login_with_case_sensitive_password"))

    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
