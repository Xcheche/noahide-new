from django.test import Client, TestCase
from blog.models import Post  # Import the Post model
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.urls import reverse
# Create your tests here.

        
        
#Database test for the blog post model
#Testing if authenticated user can create a post
class TestModels(TestCase):
    def setUp(self):
        """
        Runs before each test.
        """
        User = get_user_model() 
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user.save()
        
        
        
    def test_model_blog_post(self):
        #setupcode
        #logic
        #assertion
        
        
        # Create a post instance
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user
           
        )
        # Save the post instance to the database
        post.save()
        # Check if the post was created successfully
        self.assertEqual(Post.objects.count(), 1)
        # Check if the post's attributes are correct
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post.')
        self.assertEqual(post.author, self.user)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 
# Test for the homepage/Views



class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # creating a user so that we can login
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        
        # Separate URLs for each view
        self.home_url = reverse('home')
        self.post_detail_url = reverse('post_detail', kwargs={'pk': 1})
        #self.post_create_url = reverse('post_create')
        self.profile_url = reverse('profile', kwargs={'pk': self.user.pk})
        self.signin_url = reverse('signin')
        self.signup_url = reverse('signup')
# home 
    def test_homepage_status_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        
        
# post detail
    def test_post_detail_GET(self):
        # Create a post instance for testing
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user
        )
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, post.title)
        self.assertContains(response, post.content)
        self.assertContains(response, post.author.username)
        # Check if the post is in the context
        self.assertIn('post', response.context)  # Check if the post is in the context
        
        
        
# profile
    def test_profile_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        
 # signin       
    def test_signin_GET(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signin.html')
        
# signin post
    # This test assumes that the user is already created in setUp        
    def test_signin_POST(self):
        response = self.client.post(self.signin_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)  
        
 # signup       
    def test_signup_GET(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
# signup post
    def test_signup_POST(self):
        response = self.client.post(self.signup_url, {
            'fullname': 'New User',
            'email': 'newuser@example.com',
            'gender': 'M',
            'username': 'newuser',
            'password': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signin_url)
        # Check if the user was created
        user = get_user_model().objects.get(username='newuser')
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password('newpassword'))

        self.assertEqual(user.fullname, 'New User')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.gender, 'M')
        
        
# logout
    def test_logout_GET(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.signin_url)
        # Check if the user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)        
