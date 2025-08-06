import time
from unittest import skip

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class GuiTestWithSelenium(TestCase):
    @skip
    def test_book_page(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/eshop/book_list/')
        time.sleep(2)
        assert "Kategorie" in driver.page_source

    @skip
    def test_detai_book_page(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/eshop/book_detail/4/')
        time.sleep(2)
        assert "Na skladě:" in driver.page_source

    @skip
    def test_signup(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/accounts/signup/')
        time.sleep(2)


        username_field = driver.find_element(By.ID, 'id_username')
        username_field.send_keys('tester1')
        time.sleep(2)
        first_name_field = driver.find_element(By.ID, 'id_first_name')
        first_name_field.send_keys('tester1')
        time.sleep(2)
        last_name_field = driver.find_element(By.ID, 'id_last_name')
        last_name_field.send_keys('test1')
        time.sleep(2)
        email_field = driver.find_element(By.ID, 'id_email')
        email_field.send_keys('test1@mail.cz')
        time.sleep(2)
        password1_field = driver.find_element(By.ID, 'id_password1')
        password1_field.send_keys('heslo1234')
        time.sleep(2)
        password2_field = driver.find_element(By.ID, 'id_password2')
        password2_field.send_keys('heslo1234')
        time.sleep(2)
        submit_button = driver.find_element(By.ID, 'id_submit')
        submit_button.send_keys(Keys.RETURN)
        time.sleep(2)

        assert('Username'
               or 'A user with that username already exists.'
               in driver.page_source)
    @skip
    def test_book_not_in_db(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/eshop/book_detail/1004/')
        time.sleep(2)

        assert 'Chyba 404: Stránka nenalezena' in driver.page_source