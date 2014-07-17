"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test.testcases import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
import unittest

def open_page(browser, url, live_server_url):
    browser.get('%s%s' % (live_server_url,url))

def steps_to_login(browser,live_server_url,username,password):
    open_page(browser, '/login/', live_server_url)
    username_input = browser.find_element_by_name('username')
    username_input.send_keys(username)
    password_input = browser.find_element_by_name('password')
    password_input.send_keys(password)
    button_register = browser.find_element_by_name('submit')
    button_register.click()

def create_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()

class LoginTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        open_page(self.browser, '/login/', self.live_server_url)
        self.assertIn('Login Supernova', self.browser.title)
        
    def test_login_correct(self):
        create_user('john','john@john.com','johnpassword')
        steps_to_login(self.browser,self.live_server_url,'john','johnpassword')
        self.assertIn('Index', self.browser.title)
    
    def test_login_incorrect(self):
        create_user('john','john@john.com','johnpassword')
        steps_to_login(self.browser,self.live_server_url,'john1','johnpassword1')
        login_incorrect = self.browser.find_element_by_tag_name('body')
        self.assertIn('Invalid login details supplied.', login_incorrect.text)
        
    def test_login_and_logout(self): 
        create_user('john','john@john.com','johnpassword')
        steps_to_login(self.browser,self.live_server_url,'john','johnpassword')
        login_successful = self.browser.find_element_by_tag_name('strong')
        self.assertIn('Welcome to Supernova', login_successful.text)
        link_logout = self.browser.find_element_by_link_text('Logout')
        link_logout.click()
        logout_sucessful = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Login to Supernova',logout_sucessful.text)
    
    def test_login_logout_and_login(self): 
        create_user('john','john@john.com','johnpassword')
        steps_to_login(self.browser,self.live_server_url,'john','johnpassword')
        login_successful = self.browser.find_element_by_tag_name('strong')
        self.assertIn('Welcome to Supernova', login_successful.text)
        link_logout = self.browser.find_element_by_link_text('Logout')
        link_logout.click()
        logout_sucessful = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Login to Supernova',logout_sucessful.text)
        steps_to_login(self.browser,self.live_server_url,'john','johnpassword')
        login_successful = self.browser.find_element_by_tag_name('strong')
        self.assertIn('Welcome to Supernova', login_successful.text)
        
class RegisterTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()
           
    def test_title(self):
        open_page(self.browser, '/register/', self.live_server_url)
        self.assertIn('Register Supernova', self.browser.title)
    
    def steps_to_create_user(self,username,email,password):
        open_page(self.browser, '/register/', self.live_server_url)
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys(username)
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys(email)
        password_input = self.browser.find_element_by_name('password')
        password_input.send_keys(password)
        button_register = self.browser.find_element_by_name('submit')
        button_register.click()
    
    def test_register_correct(self):
        self.steps_to_create_user('teste_django','teste_django@testedjango.com','teste_django')
        register_correct_message = self.browser.find_element_by_tag_name('strong')
        self.assertIn('thank you for registering!', register_correct_message.text)
        
    def test_register_repeated_user(self):
        self.steps_to_create_user('testedjangorepeated','testedjangorepeated@testedjango.com','testedjangorepeated')
        self.steps_to_create_user('testedjangorepeated','testedjangorepeated@testedjango.com','testedjangorepeated')
        register_repeated_message = self.browser.find_element_by_tag_name('li')
        self.assertIn('User with this Username already exists.', register_repeated_message.text)
    
class PermissionsTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()
    
    def test_go_to_index_without_login(self):
        open_page(self.browser, '/index/', self.live_server_url)
        login_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Login to Supernova',login_text.text)
        self.assertIn('/login/',self.browser.current_url)
        
    def test_go_to_index_with_login(self):
        create_user('john','john@john.com','johnpassword')
        open_page(self.browser, '/login/', self.live_server_url)
        steps_to_login(self.browser, self.live_server_url, 'john', 'johnpassword')
        open_page(self.browser, '/index/', self.live_server_url)
        login_successful = self.browser.find_element_by_tag_name('strong')
        self.assertIn('Welcome to Supernova', login_successful.text)
 
if (__name__ == '__main__'):
    unittest.main()


