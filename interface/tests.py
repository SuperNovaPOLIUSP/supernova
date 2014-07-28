#coding: utf8
from django.contrib.auth.models import User
from django.test.testcases import LiveServerTestCase
from pulsarInterface.Course import Course
from pulsarInterface.Professor import Professor
from pulsarInterface.Schedule import Schedule
from pulsarInterface.TimePeriod import TimePeriod
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from tools.MySQLConnection import MySQLConnection


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
        self.browser.implicitly_wait(1)
        create_user_and_login(self.browser, self.live_server_url,'john','johnpassword','john@john.com')
        self.name_professor = 'teste'

    def tearDown(self):
        self.browser.quit()
        
    def create_professor(self,professor_name):
        open_page(self.browser, '/interface/professor', self.live_server_url)
        button_create_professor = self.browser.find_element_by_name('criar')
        button_create_professor.click()
        self.assertIn('Interface - Professor Create', self.browser.title)
        form_name = self.browser.find_element_by_id('id_name')
        form_name.send_keys(professor_name)
        form_memberId = self.browser.find_element_by_id('id_memberId')
        form_memberId.send_keys('00000')
        form_office = self.browser.find_element_by_id('id_office')
        form_office.send_keys('0')
        form_email = self.browser.find_element_by_id('id_email')
        form_email.send_keys('0')
        form_phoneNumber = self.browser.find_element_by_id('id_phoneNumber')
        form_phoneNumber.send_keys('0')
        form_cellphoneNumber = self.browser.find_element_by_id('id_cellphoneNumber')
        form_cellphoneNumber.send_keys('0')
        form_idDepartment = self.browser.find_element_by_id('id_idDepartment')
        form_idDepartment.send_keys('')
        button_submit = self.browser.find_element_by_name('Cadastrar')
        button_submit.click()

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
        
    def test_create_professor(self):
        self.create_professor(self.name_professor)
        open_page(self.browser, '/interface/professor', self.live_server_url)
        professor_name_link = self.browser.find_element_by_link_text(self.name_professor)
        self.assertIsNotNone(professor_name_link)
        
    def test_edit_professor(self):
        professor = Professor(self.name_professor)
        professor.store()
        open_page(self.browser, '/interface/professor', self.live_server_url)
        professor_name_link = self.browser.find_element_by_link_text(self.name_professor)
        professor_name_link.click()
        self.assertIn('Interface - Professor Detail', self.browser.title)
        button_edit = self.browser.find_element_by_name('editar')
        button_edit.click()
        self.assertIn('Interface - Professor Edit', self.browser.title)
        form_name = self.browser.find_element_by_id('id_name')
        form_name.send_keys('Edit')
        form_memberId = self.browser.find_element_by_id('id_memberId')
        form_memberId.send_keys('')
        form_office = self.browser.find_element_by_id('id_office')
        form_office.send_keys('')
        form_email = self.browser.find_element_by_id('id_email')
        form_email.send_keys('')
        form_phoneNumber = self.browser.find_element_by_id('id_phoneNumber')
        form_phoneNumber.send_keys('0')
        form_cellphoneNumber = self.browser.find_element_by_id('id_cellphoneNumber')
        form_cellphoneNumber.send_keys('0')
        form_idDepartment = self.browser.find_element_by_id('id_idDepartment')
        form_idDepartment.send_keys('')
        button_apply = self.browser.find_element_by_name('Aplicar')
        button_apply.click()
        open_page(self.browser, '/interface/professor', self.live_server_url)
        professor_name_link_after_edit = self.browser.find_element_by_link_text(self.name_professor + 'Edit')
        professor_name_link_after_edit.click()
        list_professor_info = self.browser.find_elements_by_tag_name('p')
        self.assertEqual(list_professor_info[1].text, 'Member ID: 0')
        self.assertEqual(list_professor_info[2].text, 'Office: None')
        self.assertEqual(list_professor_info[3].text, 'Email: None')
        self.assertEqual(list_professor_info[4].text, 'Phone Number: 0')
        self.assertEqual(list_professor_info[5].text, 'CellPhone Number: 0')
        self.assertEqual(list_professor_info[6].text, 'Id Department: None')
    
    def test_delete_professor(self):
        professor = Professor(self.name_professor)
        professor.store()
        open_page(self.browser, '/interface/professor', self.live_server_url)
        professor_name_link = self.browser.find_element_by_link_text(self.name_professor)
        professor_name_link.click()
        self.assertIn('Interface - Professor Detail', self.browser.title)
        button_delete = self.browser.find_element_by_name('deletar')
        button_delete.click()
        alert = self.browser.switch_to.alert
        alert.accept()
        self.assertIn('Interface - Professor', self.browser.title)
        professor_name_after_delete = self.browser.find_elements_by_tag_name('a')
        names = [link.text for link in professor_name_after_delete]
        self.assertNotIn(self.name_professor, names)
        
class OfferTest (LiveServerTestCase):
        
    def setUp(self):
        self.browser = WebDriver()
        self.create_timePeriod_and_course()
        self.create_professor_and_schedule()
        self.browser.implicitly_wait(10)
        create_user_and_login(self.browser, self.live_server_url,'john','johnpassword','john@john.com')
        self.name_professor = 'teste'
        
    def tearDown(self):
        self.browser.quit()
        
    def create_timePeriod_and_course(self):
        cursor = MySQLConnection()
        cursor.execute('INSERT INTO minitableLength (idLength, length) values (1, "Semestral")')
        self.course = Course('tst9999', 'teste9999', '0000-00-00')
        self.course.store()
        self.timePeriod = TimePeriod(1, 2014, 1)
        self.timePeriod.store()
    
    def create_professor_and_schedule(self):
        cursor = MySQLConnection()
        cursor.execute('INSERT INTO `minitableDayOfTheWeek` VALUES (1,"Domingo"), (2,"Segunda"), (3,"Terça"), (4,"Quarta"), (5,"Quinta"), (6,"Sexta"), (7,"Sabado")')
        self.schedule = Schedule('Domingo', '12:00:00', 'weekly', '14:00:00')
        self.schedule.store()
        self.schedule = Schedule('Segunda', '16:00:00', 'weekly', '19:00:00')
        self.schedule.store()
        self.schedule = Schedule('Quarta', '14:00:00', 'weekly', '16:00:00')
        self.schedule.store()
        self.professor = Professor('Professor Teste')
        self.professor.store()
                
    def login_to_offer_page(self):
        open_page(self.browser, '/interface/', self.live_server_url)
        dropdown_timePeriod = self.browser.find_element_by_id('id_dropDownTimePeriod')
        dropdown_course = self.browser.find_element_by_id('id_dropDownCourse')
        select_timePeriod = Select(dropdown_timePeriod)
        select_timePeriod.select_by_value(str(self.timePeriod.idTimePeriod))
        select_course = Select(dropdown_course)
        select_course.select_by_value(str(self.course.idCourse))
        professor_interface = self.browser.find_element_by_link_text('Offer')
        professor_interface.click()
        self.assertIn('Interface - Offer', self.browser.title)
        
    def test_create_offer(self):
        self.login_to_offer_page()
        button_create_offer = self.browser.find_element_by_name('criar')
        button_create_offer.click()
        self.assertIn('Interface - Offer Create', self.browser.title)
        dropdown_professor = self.browser.find_element_by_id('id_dropDownProfessor')
        select_professor = Select(dropdown_professor)
        select_professor.select_by_value(str(self.professor.idProfessor))
        input_classNumber = self.browser.find_element_by_id('id_classNumber')
        input_classNumber.send_keys('1')
        