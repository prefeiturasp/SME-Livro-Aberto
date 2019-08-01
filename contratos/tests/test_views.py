from django.shortcuts import render
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase


class TestHomeView(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:home')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/home.html')


class TestSobreView(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:sobre')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/sobre.html')
