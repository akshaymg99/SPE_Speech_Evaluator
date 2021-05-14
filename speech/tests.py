from django.test import Client
from django.test import TestCase
import unittest

class TestApp(TestCase):
    ##  Checking if all webpages are retrieved successfully (status code-> 200 should specify the success)
    def test_home_page(self):
        self.c = Client()
        csrf_client = Client(enforce_csrf_checks=True)  ## enforcing CSRF Checks
        self.response = self.c.get('')          ## home page retrieval
        print(self.response.status_code)        ## output = 200 specifies the page was retrieved successfully
        self.assertEqual(self.response.status_code, 200, msg='Home page retrieved successfully')

    def test_record_page(self):
        self.c = Client()
        csrf_client = Client(enforce_csrf_checks=True)  ## enforcing CSRF Checks
        self.response = self.c.get('/record')    ## record.html page retrieval
        print(self.response.status_code)         ## output = 200 specifies the page was retrieved successfully
        self.assertEqual(self.response.status_code, 200, msg='Recording page retrieved successfully')

    def test_result_page(self):
        self.c = Client()
        csrf_client = Client(enforce_csrf_checks=True)  ## enforcing CSRF Checks
        self.response = self.c.get('/result')     ## result.html page retrieval
        print(self.response.status_code)          ## output = 200 specifies the page was retrieved successfully
        self.assertEqual(self.response.status_code, 200, msg='Result page retrieved successfully')
        print(self.response.content)                  ## checking content of the webpage

    def test_Analysis_logic(self):
        self.c = Client()
        self.table_1 = []
        self.temp = {}
        self.temp['Sentence'] = "Hi, My name is Akshay, I am pursing Masters from IIITB"
        self.temp['Analysis'] = "Correct"
        self.table_1.append(self.temp)
        self.res = []
        self.res.append(0)
        self.res.append(340)
        self.res.append(50)
        self.vocab_analysis = "Average. Your knowledge of english vocabulary words is average. There is room for improvement"
        self.data = {'table_1': self.table_1, 'vocab_strength': self.res[1], 'vocab_analysis': self.vocab_analysis, 'unique_words': self.res[2]}
        self.response = self.c.post('/record', self.data)
        print(self.response.status_code)


if __name__ == '__main__':
    unittest.main()







