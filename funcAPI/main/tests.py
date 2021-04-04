from django.shortcuts import resolve_url
from rest_framework.test import APITestCase


class MainAPITest(APITestCase):
    def test_func_view_test(self):
        data = [1, 2, 3, 4, 5]
        rules = ['a', 'b', 'c', 'd', 'e', 'f']
        response = self.client.get(resolve_url('main:index'), {'data': data, 'rules': rules})
        self.assertEquals(response.json(), {'data': [5.1, 5.4, 5.9, 6.6, 7.5]})

    def test_func_invalud_rule(self):
        data = [1, 2, 3, 4, 5]
        rules = ['aewfwef']
        response = self.client.get(resolve_url('main:index'), {'data': data, 'rules': rules})
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.json(), {'rules': ['function with name fun_aewfwef not found in module main.functions']})

    def test_func(self):
        data = [2, 2, 2, 2]
        rules = ['a', ]
        response = self.client.get(resolve_url('main:index'), {'data': data, 'rules': rules})
        self.assertEquals(response.json(), {'data': [4, 4, 4, 4]})

    def test_func_few_times(self):
        data = [2, 2, 2, 2]
        rules = ['a'] * 5
        response = self.client.get(resolve_url('main:index'), {'data': data, 'rules': rules})
        self.assertEquals(response.json(), {'data': [i**2**5 for i in data]})

    def test_specific_func_a(self):
        data = [1, 2, 3, 4]
        response = self.client.get(resolve_url('main:detail', name='a'), {'data': data})
        self.assertEquals(response.json(), {'data': [1, 4, 9, 16]})

    def test_specific_func_d(self):
        data = [1, 2, 3, 4]
        response = self.client.get(resolve_url('main:detail', name='d'), {'data': data})
        self.assertEquals(response.json(), {'data': [0.1, 0.2, 0.3, 0.4]})

    def test_invalid_func_name(self):
        data = [1, 2, 3, 4]
        response = self.client.get(resolve_url('main:detail', name='mmmmmmmmm'), {'data': data})
        self.assertEquals(response.status_code, 404)