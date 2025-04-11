from django.test import TestCase
from blog.models import Post  # Import the Post model

# Create your tests here.

# class HomePageTests(TestCase):
    
    
#     def test_home_page_status_code(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
from django.urls import reverse

class HomePageTest(TestCase):

    def test_homepage_status_code(self):
        response = self.client.get(reverse('home')) # 'home' is the name of your url pattern.
        self.assertEqual(response.status_code, 200)

    def test_homepage_contains_correct_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Noahide Wisdom')

    def test_homepage_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'blog/home.html') 
        
  