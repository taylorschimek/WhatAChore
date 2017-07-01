from datetime import date
from django_webtest import WebTest
from time import sleep
import webtest

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import TestCase, TransactionTestCase
from django.test.client import Client

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .forms import *
from .models import *
from useraccounts.models import User


def try_class_name(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None

def try_name(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None

def try_id(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None

def try_xpath(driver, delay, selector):
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, selector)))
        return myElem
    except TimeoutException:
        print('{} took too long'.format(selector))
        return None

def try_id_test(driver, selector):
    try:
        driver.find_element_by_xpath(selector)
    except NoSuchElementException:
        return False
    return True

class ChoreTests(WebTest):

    @classmethod
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('password1')
        self.user.save()

    @classmethod
    def tearDown(self):
        User.objects.all().delete()

    def create_chore(self, task='test task',
                           description='test description',
                           duration=20,
                           interval='Daily',
                           age_restriction=14,
                           chore_icon_location='/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/Icons/cream_icons/Chore_Broom.png'
    ):
        return Chore.objects.create(user_id=self.user.id,
                                    task=task,
                                    description=description,
                                    duration=duration,
                                    interval=interval,
                                    age_restriction=age_restriction,
                                    chore_icon_location=chore_icon_location
        )

    def test_chore_creation(self):
        """
            test creation of chore and all fields
        """
        self.assertTrue(self.user.is_authenticated())
        c = self.create_chore()
        self.assertTrue(isinstance(c, Chore))
        self.assertEqual(c.__str__(), c.task)

        actual_path = c.chore_icon_location.replace(settings.BASE_DIR + '/wac/static', '')
        self.assertEqual(c.chore_icon, actual_path)

    def test_chores_list_view(self):
        """
            test chore list view
        """
        c1 = self.create_chore(task='test task1')
        c2 = self.create_chore(task='test task2')
        # json_data = simplejson.dumps({stuff})

        # resp = self.client.post(reverse('chore-list'), json_data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.login(email='test@example.com', password='password1')
        resp = self.client.get(reverse('chore-list'))

        self.assertEqual(resp.status_code, 200) # we have  redirect here
        self.assertIn(c1.task, str(resp.content))
        self.assertIn(c2.task, str(resp.content))

    def test_chore_valid_form(self):
        """
            test form is valid
            then test form submission
        """
        c = self.create_chore()
        data = {'user_id': c.user_id,
                'task': c.task,
                'description': c.description,
                'duration': c.duration,
                'interval': c.interval,
                'age_restriction': c.age_restriction,
                'chore_icon_location': c.chore_icon_location}
        form = ChoreEditForm(data=data)
        self.assertTrue(form.is_valid())
        self.client.login(email='test@example.com', password='password1')
        chore = form.save(commit=False)
        chore.user_id = self.user.id
        chore.save()
        self.assertEqual(chore.task, 'test task')
        self.assertEqual(chore.description, 'test description')
        self.assertEqual(chore.duration, 20)
        self.assertEqual(chore.age_restriction, 14)

    def test_chore_invalid_form(self):
        """
            test form is invalid
        """
        c = self.create_chore()
        data = {'user_id': c.user_id,
                'task': c.task,
                'description': c.description,
                'duration': '',
                'interval': c.interval,
                'age_restriction': c.age_restriction,
                'chore_icon_location': c.chore_icon_location}
        form = ChoreEditForm(data=data)
        self.assertFalse(form.is_valid())

    def test_chore_form_success(self):
        resp = self.app.get(reverse('chore-create'), user=self.user)
        self.assertEqual(resp.status, '200 OK')
        form = resp.form
        form['task'] = 'form test task'
        form['description'] = 'form test description'
        form['duration'] = 20
        form['interval'] = 'Daily'
        form['age_restriction'] = 14
        resp = form.submit()
        self.assertEqual(resp.status, '200 OK')

class PersonTests(WebTest):

    @classmethod
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('password1')
        self.user.save()

    @classmethod
    def tearDown(self):
        User.objects.all().delete()

    def create_person(self, name='tester',
                            birthday=date(1977, 5, 22),
                            phone_number=5128675309,
                            email='person_test@example.com',
                            day_off='Thur'
    ):
        return Person.objects.create(user_id=self.user.id,
                                     name=name,
                                     birthday=birthday,
                                     phone_number=phone_number,
                                     email=email,
                                     day_off=day_off
        )

    def test_person_creation(self):
        """
        test creation of person and its fields
        """
        p = self.create_person()
        self.assertTrue(isinstance(p, Person))
        self.assertEqual(p.__str__(), p.name)
        self.assertEqual(p.age, 40)
        self.assertEqual(str(Person._meta.verbose_name_plural), 'people')
        self.assertEqual(self.user, p.user)

    def test_person_valid_form(self):
        """
            test form is valid
            then test form submission
        """
        p = self.create_person()
        data = {'user_id': p.user_id,
                'name': p.name,
                'birthday': p.birthday,
                'phone_number': p.phone_number,
                'email': p.email,
                'day_off': p.day_off}
        form = PersonEditForm(data=data)
        self.assertTrue(form.is_valid())
        self.client.login(email='test@example.com', password='password1')
        person = form.save(commit=False)
        person.user_id = self.user.id
        person.save()
        self.assertEqual(person.name, 'tester')
        self.assertEqual(person.email, 'person_test@example.com')
        self.assertEqual(person.day_off, 'Thur')



class SeleniumTestLogin(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestLogin, cls).setUpClass()
        cls.user = User.objects.create(email='test0@example.com')
        cls.user.set_password('password0')
        cls.user.save()
        cls.person = Person.objects.create(user=cls.user,
                                           name='Bing',
                                           birthday='1976-06-14',
                                           email='test0@example.com',
                                           day_off='Wed'
        )

        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTestLogin, cls).tearDownClass()

    def test_login(self):
        delay = 2
        driver = self.selenium

        driver.get('{}{}'.format(self.live_server_url, reverse('landing')))
        driver.find_element_by_id('nav-login').click()

        email_input = try_id(driver, 2, 'id_username')
        email_input.send_keys('test0@example.com')
        password_input = driver.find_element_by_id('id_password')
        password_input.send_keys('password0')
        driver.find_element_by_xpath('//input[@value="Login"]').click()
        sleep(1)
        name_on_page = driver.find_element_by_xpath('//section[@id="home"]/div/div/h1').text
        name = Person.objects.get(email='test0@example.com').name
        self.assertEqual(name_on_page, name)


class SeleniumTestViews(StaticLiveServerTestCase):

    fixtures = ['wac/fixtures/wac.json', 'useraccounts/fixtures/useraccounts.json']

    @classmethod
    def setUpClass(cls):
        super(SeleniumTestViews, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        # cls.kill_all_created_users(cls)
        cls.selenium.quit()
        super(SeleniumTestViews, cls).tearDownClass()

    # TESTS --------------
    def test_chore_detail_and_edit_views(self):
        delay = 2
        browser = self.selenium

        browser.get('{}{}'.format(self.live_server_url, reverse('landing')))
        browser.find_element_by_id('nav-login').click()

        email_input = try_id(browser, 2, 'id_username')
        email_input.send_keys('test1@example.com')
        password_input = browser.find_element_by_id('id_password')
        password_input.send_keys('password1')
        browser.find_element_by_xpath('//input[@value="Login"]').click()
        sleep(1)

        browser.get('{}{}'.format(self.live_server_url, reverse('chore-list')))
        # wait for page to load and then click on chore_30
        spec_chore = try_name(browser, delay, 'chore_30')
        spec_chore.click()

        # wait for modal to load then assert that it is Task 1
        task_elem = try_name(browser, delay, 'task')
        task = task_elem.get_attribute('value')
        self.assertEqual('Task Daily', task)

        # Change the duration of Task 1 to 120 minutes.
        duration = browser.find_element_by_name('duration')
        duration.clear()
        duration.send_keys('120')
        browser.find_element_by_xpath('//input[@value="Save"]').click()

        # Check to make sure the duration change was saved.
        spec_chore = try_name(browser, delay, 'chore_30')
        spec_chore.click()

        duration_elem = try_id(browser, delay, 'id_duration')
        duration = duration_elem.get_attribute('value')
        self.assertEqual('120', duration)

        browser.find_element_by_class_name('close').click()

    def test_person_detail_and_edit_views(self):
        delay = 2
        browser = self.selenium

        browser.get('{}{}'.format(self.live_server_url, reverse('landing')))
        browser.find_element_by_id('nav-login').click()

        email_input = try_id(browser, delay, 'id_username')
        email_input.send_keys('test2@example.com')
        password_input = browser.find_element_by_id('id_password')
        password_input.send_keys('password2')
        browser.find_element_by_xpath('//input[@value="Login"]').click()
        sleep(1)

        browser.get('{}{}'.format(self.live_server_url, reverse('people-list')))

        daysoff_elem = try_id(browser, delay, 'Floyd-daysoff')
        browser.find_element_by_id('Floyd-link').click()

        email_elem = try_id(browser, delay, 'id_email')
        email = email_elem.get_attribute('value')
        self.assertEqual('test2@example.com', email)

        # Change something in form to see if the changes stick
        daysoff = browser.find_element_by_id('id_day_off')
        browser.find_element_by_xpath("//select[@id='id_day_off']/option[text()='Thursday']").click()
        browser.find_element_by_xpath('//input[@value="Save"]').click()
        sleep(2)

        # Check to make sure the change stuck
        display_dayoff = browser.find_element_by_id('Floyd-daysoff').text
        self.assertEqual(display_dayoff, 'Thur')

    def test_person_image_selection(self):
        delay = 2
        browser = self.selenium

        browser.get('{}{}'.format(self.live_server_url, reverse('landing')))
        browser.find_element_by_id('nav-login').click()

        email_input = try_id(browser, delay, 'id_username')
        email_input.send_keys('test2@example.com')
        password_input = browser.find_element_by_id('id_password')
        password_input.send_keys('password2')
        browser.find_element_by_xpath('//input[@value="Login"]').click()
        sleep(1)

        browser.get('{}{}'.format(self.live_server_url, reverse('people-list')))

        newPerson_elem = try_id(browser, delay, 'newPerson')
        newPerson_elem.click()

        name_elem = try_id(browser, delay, 'id_name')
        name_elem.send_keys('Billy')
        bday = browser.find_element_by_id('id_birthday')
        bday.clear()
        bday.send_keys('1995-05-21')
        # browser.find_element_by_xpath("//select[@id='id_day_off']/option[text()='Thursday']").click()
        # file_location = '/Users/HOME/Developer/WAC/whatachore/wac/static/wac/styles/images/people/tito.png'
        # browser.find_element_by_xpath('//input[@name="mugshot"]').send_keys(file_location)
        browser.find_element_by_xpath('//input[@value="Save"]').click()
        sleep(1)
        new_name = browser.find_element_by_xpath('//a[@id="Billy-link"]//h3[@class="card-title"]').text
        self.assertEqual(new_name, 'Billy')

    def test_assignment_list_view(self):
        delay = 2
        browser = self.selenium

        browser.get('{}{}'.format(self.live_server_url, reverse('landing')))
        browser.find_element_by_id('nav-login').click()

        email_input = try_id(browser, delay, 'id_username')
        email_input.send_keys('test1@example.com')
        password_input = browser.find_element_by_id('id_password')
        password_input.send_keys('password1')
        browser.find_element_by_xpath('//input[@value="Login"]').click()
        sleep(1)

        now_asses = Assignment.objects.all()
        self.assertEqual(len(now_asses), 0)

        browser.find_element_by_xpath("//a[text()='Assignments']").click()
        myElem = try_class_name(browser, delay, 'myBorder')
        myElem.click()
        now_asses = Assignment.objects.all()
        self.assertGreater(len(now_asses), 9)

        # Navigate to a Task 3 and select it
        browser.find_element_by_xpath('//p[text()="Task 3Days"]').click()

        title_elem = try_class_name(browser, delay, 'modal-title')
        title = title_elem.text
        print('modal-title = {}'.format(title))
        self.assertIn('Task 3Days', title)

        who_field = Select(browser.find_element_by_id('id_who'))
        who = who_field.first_selected_option.text
        if who == 'Bob':
            who_field.select_by_visible_text('Barbara')
        else:
            who_field.select_by_visible_text('Bob')
        browser.find_element_by_xpath('//input[@value="Save"]').click()
        sleep(1)
        browser.find_element_by_xpath('//p[text()="Task 3Days"]').click()
        sleep(1)
        who_field = Select(browser.find_element_by_id('id_who'))
        who2 = who_field.first_selected_option.text
        self.assertNotEqual(who, who2)
        browser.find_element_by_xpath('//button[text()="Close"]').click()

        Assignment.objects.all().delete()

    def test_person_delete(self):
        delay = 2
        browser = self.selenium

        browser.get('{}{}'.format(self.live_server_url, reverse('landing')))
        browser.find_element_by_id('nav-login').click()

        email_input = try_id(browser, delay, 'id_username')
        email_input.send_keys('test1@example.com')
        password_input = browser.find_element_by_id('id_password')
        password_input.send_keys('password1')
        browser.find_element_by_xpath('//input[@value="Login"]').click()
        sleep(1)

        people_button = try_xpath(browser, delay, '//a[text()="People"]')
        people_button.click()

        barbara_button = try_id(browser, delay, 'Barbara-link')
        barbara_button.click()

        delete_button = try_xpath(browser, delay, '//button[text()="Delete Barbara"]')
        delete_button.click()

        confirm_button = try_xpath(browser, delay, '//input[@value="Yes"]')
        confirm_button.click()

        self.assertFalse(try_id_test(browser, 'Barbara-link'))
