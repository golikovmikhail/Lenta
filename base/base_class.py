from datetime import datetime

class Base:

    def __init__(self, driver):
        self.driver = driver

    """Метод получения URL"""
    def get_current_url(self):
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        return current_url

    """Метод проверки соответствия текста"""
    def assert_word(self, element, expected_text):
        actual_text = element.text.strip()
        assert actual_text == expected_text, f"❌ Expected: '{expected_text}', Got: '{actual_text}'"
        print(f"✅ Correct text: '{actual_text}'")

    """Метод создания скриншота"""
    def get_screenshot(self):
        now_date = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = f"C:\\Users\\golik\\PycharmProjects\\main_Project\\screen\\screenshot_{now_date}.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

    """Метод проверки соответствия URL"""
    def assert_url(self, expected_url):
        current_url = self.get_current_url()
        assert current_url == expected_url, f"❌ Expected URL: '{expected_url}', Got: '{current_url}'"
        print(f"✅ Correct URL: {current_url}")
