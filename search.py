# -*- coding: cp1252 -*-
##
## PythonSearchTest by Pascal VH 20-09-18
## version 0.1
## unittest used to run the tests
## Firefox as browser
## test_case 1 : test search with results
## test_case 2 : test search with no results
import unittest,time
from selenium import webdriver

class PythonSearchTest(unittest.TestCase):
    domain = "https://www.check24.de/"
    search_elem = '//*[@id="c24-search-header"]'
    search_item_ok = "rtx 2080 ti"
    search_item_nok = "iojfdjljhfdsjhjcd"

    def setUp(self):
        self.driver = webdriver.Firefox()

    def search(self, item):
        driver = self.driver
        driver.get(self.domain)
        self.assertIn("CHECK24", driver.title)
        elem = driver.find_element_by_xpath(self.search_elem)
        elem.send_keys(item)
        elem.submit()
        time.sleep(1)

    def test_case_1_search_ok(self):
        self.search(self.search_item_ok)     
        assert "Keine Ergebnisse" not in self.driver.page_source

    def test_case_2_search_no_result(self):
        self.search(self.search_item_nok)     
        assert u"Keine Ergebnisse für " in self.driver.page_source

        
    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
