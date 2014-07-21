#encoding: utf8
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test.testcases import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

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
        create_user('john','john@john.com','johnpassword')
        steps_to_login(self.browser,self.live_server_url,'john','johnpassword')
        
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
        
    def go_to_x_without_login_and_check_title(self, page, page_title):
        open_page(self.browser, page, self.live_server_url)
        self.assertIn(page_title, self.browser.title)
        
    def go_to_x_with_login_and_check_title(self,page, page_title):
        create_user('john','john@john.com','johnpassword')
        steps_to_login(self.browser, self.live_server_url, 'john', 'johnpassword')
        open_page(self.browser, page, self.live_server_url)
        self.assertIn(page_title, self.browser.title)
        
    def test_go_to_index_without_login(self):
        self.go_to_x_without_login_and_check_title('/index/', 'Login')
        
    def test_go_to_index_with_login(self):
        self.go_to_x_with_login_and_check_title('/index/', 'Index')
        
    def test_go_to_opticalSheet_without_login(self):
        self.go_to_x_without_login_and_check_title('/opticalSheet/', 'Login')
        
    def test_go_to_opticalSheet_with_login(self):
        self.go_to_x_with_login_and_check_title('/opticalSheet/', 'OpticalSheet')
        
    def test_go_to_datafile_without_login(self):
        self.go_to_x_without_login_and_check_title('/datafile/', 'Login')
    
    def test_go_to_datafile_with_login(self):
        self.go_to_x_with_login_and_check_title('/datafile/', 'Datafile')
    
    def test_go_to_generator_without_login(self):
        self.go_to_x_without_login_and_check_title('/generator/', 'Login')
    
    def test_go_to_generator_with_login(self):
        self.go_to_x_with_login_and_check_title('/generator/', u'Gerador de Relatórios')
        
    def test_go_to_control_without_login(self):
        self.go_to_x_without_login_and_check_title('/control/', 'Login')
    
    def test_go_to_control_with_login(self):
        self.go_to_x_with_login_and_check_title('/control/', 'Control')
    
    def test_go_to_encoder_without_login(self):
        self.go_to_x_without_login_and_check_title('/encoder/', 'Login')
    
    def test_go_to_encoder_with_login(self):
        self.go_to_x_with_login_and_check_title('/encoder/', 'Encoder')
        
    def test_go_to_presentation_without_login(self):
        self.go_to_x_without_login_and_check_title('/presentation/', 'Login')
    
    def test_go_to_presentation_with_login(self):
        self.go_to_x_with_login_and_check_title('/presentation/', 'Presentation')
        
    def test_go_to_register_without_login(self):
        self.go_to_x_without_login_and_check_title('/register/', 'Login')
    
    def test_go_to_register_with_login(self):
        self.go_to_x_with_login_and_check_title('/register/', 'Register')
        
    def test_go_to_lerJupiter_without_login(self):
        self.go_to_x_without_login_and_check_title('/lerJupiter/', 'Login')
    
    def test_go_to_lerJupiter_with_login(self):
        self.go_to_x_with_login_and_check_title('/lerJupiter/', 'Ler Jupiter')
        
    def test_go_to_algeLin_without_login(self):
        self.go_to_x_without_login_and_check_title('/algeLin/', 'Algebra Linear')

    def test_go_to_login_with_login(self):
        self.go_to_x_with_login_and_check_title('/login/', 'Index')
