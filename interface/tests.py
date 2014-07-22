from django.contrib.auth.models import User
from django.test import TestCase
from django.test.testcases import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

def open_page(browser, url, live_server_url):
    browser.get('%s%s' % (live_server_url,url))

def create_user_and_login(browser,live_server_url,username,password,email):
    user = User.objects.create_user(username, email, password)
    user.save()
    open_page(browser, '/login/', live_server_url)
    username_input = browser.find_element_by_name('username')
    username_input.send_keys(username)
    password_input = browser.find_element_by_name('password')
    password_input.send_keys(password)
    button_register = browser.find_element_by_name('submit')
    button_register.click()

class ProfessorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)
        create_user_and_login(self.browser, self.live_server_url,'john','johnpassword','john@john.com')

    def tearDown(self):
        self.browser.quit()

    def test_login_to_interface_page(self):
        self.assertIn('Index', self.browser.title)
        link_interface = self.browser.find_element_by_link_text('Interface')
        link_interface.click()
        self.assertIn('Interface', self.browser.title)
        
    def test_login_to_professor_page(self):
        open_page(self.browser, '/interface/', self.live_server_url)
        professor_interface = self.browser.find_element_by_link_text('Professor')
        professor_interface.click()
        self.assertIn('Interface - Professor', self.browser.title)
        
        
        