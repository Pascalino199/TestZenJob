# -*- coding: cp1252 -*-
##
## PythonRegisterTest by Pascal VH 20-09-18
## version 0.1
## unittest used to run the tests
## Firefox as browser
## test_case 1 : happy flow correct email and pwd
## test_case 2 : happy flow correct email and pwd with max len
## test_case 4 : register not ok : no email no pwd entered
## test_case 5 : register not ok : no @ in the email address
## test_case 7 : register not ok : wrong password repeat
## test_case 11 : happy flow with common symbols

import unittest,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException



class PythonRegisterTest(unittest.TestCase):
    domain = "https://www.check24.de/"
    start_registering = '/html/body/div[3]/div[2]/div/header/div[1]/div/div[1]/div/div[1]/div/div[2]/a'
    menu = "/html/body/div[3]/div[2]/div/header/div[1]/div/div[1]/div/div[1]/span/span[2]/span"
    email_elem = '//*[@id="email"]'
    pwd_elem='//*[@id="password"]'
    pwd_r_elem='//*[@id="passwordrepetition"]'
    correct_email_1="aisea.shamari@lndex.org"
    correct_email_2="kavion.ronan@lndex.org"
    correct_email_3="trentyn.lochlen@lndex.org"
    incorrect_email="abcef.com"
    correct_pwd="pwd*123"
    correct_pwd_max="BfCaxhazWgvwruVJnEzvdsW1wvfZdXKgAgC60f3UfvC4Nn*123"
    correct_pwd_symb=u'²&é"' + u"'(§è!çà)-/*-+123.^$ù,;:=µ<aB"
    submit_button = '//*[@id="c24-kb-btn"]'
    cookie_animation = '/html/body/div[2]/div/a'
    bonus = "/html/body/div[3]/div[3]/div/div/div/div[2]/div/div[3]/section[1]/div/header/button"
    

    def setUp(self):
        self.driver = webdriver.Firefox()

    def register(self,email,pwd,pwd_r):
        driver = self.driver
        driver.get(self.domain)
        self.assertIn("CHECK24", driver.title)
        #move the mouse over the menu to make it appear
        elem = driver.find_element_by_xpath(self.menu)
        hover = ActionChains(driver).move_to_element(elem)
        hover.perform()
        time.sleep(1)
        #click on the register link
        elem = driver.find_element_by_xpath(self.start_registering).click()
        #filling proper areas
        elem = driver.find_element_by_xpath(self.email_elem)
        elem.send_keys(email)
        elem = driver.find_element_by_xpath(self.pwd_elem)
        elem.send_keys(pwd)
        elem = driver.find_element_by_xpath(self.pwd_r_elem)
        elem.send_keys(pwd_r)
        #in case of the 'accept' cookie area shadows the register button, close it
        try:
            driver.find_element_by_xpath(self.cookie_animation).click()
        except NoSuchElementException as e:
            print(e)
        elem = driver.find_element_by_xpath(self.submit_button).click()
        time.sleep(5)

    def test_case_1_new_client_register(self):
        self.register(self.correct_email_1,self.correct_pwd,self.correct_pwd)
        #in case of a bonus pop-up close it
        try:
            elem=self.driver.find_element_by_xpath(self.bonus)
            elem.click()
        except NoSuchElementException as e:
            print(e)
        #test if we got into our account page 
        assert "Sie sind angemeldet als "+self.correct_email_1 in self.driver.page_source

    def test_case_2_new_client_register_max_len_pwd(self):
        self.register(self.correct_email_2,self.correct_pwd_max,self.correct_pwd_max)
        #in case of a bonus pop-up close it
        try:
            elem=self.driver.find_element_by_xpath(self.bonus)
            elem.click()
        except NoSuchElementException as e:
            print(e)
        #test if we got into our account page 
        assert "Sie sind angemeldet als "+self.correct_email_2 in self.driver.page_source

    def test_case_4_new_client_register_no_fields_entered(self):
        self.register('','','')
        #test if we got the right error messages
        assert "Bitte E-Mail-Adresse angeben." in self.driver.page_source
        assert "Bitte geben Sie Ihr Passwort ein." in self.driver.page_source

    def test_case_5_new_client_register_incorrect_email(self):
        self.register(self.incorrect_email,self.correct_pwd,self.correct_pwd)
        #test if we got the right error messages
        assert u"Ungültige E-Mail-Adresse." in self.driver.page_source

    def test_case_7_new_client_register_wrong_pwd_repeat(self):
        self.register(self.correct_email_3,self.correct_pwd,self.correct_pwd_max)
        #test if we got the right error messages
        assert u"Die Passwörter stimmen nicht überein." in self.driver.page_source

    def test_case_11_new_client_register_with_common_symboles(self):
        self.register(self.correct_email_3,self.correct_pwd_symb,self.correct_pwd_symb)
        #in case of a bonus pop-up close it
        try:
            elem=self.driver.find_element_by_xpath(self.bonus)
            elem.click()
        except NoSuchElementException as e:
            print(e)
        #test if we got into our account page 
        assert "Sie sind angemeldet als "+self.correct_email_3 in self.driver.page_source
        
    def tearDown(self):
        self.driver.close()
        pass

if __name__ == "__main__":
    unittest.main()
