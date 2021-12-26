from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class AuthUserTestCase(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'geekbrains'
    stop_word = 'Выйти'

    def setUp(self) -> None:
        self.client = Client()
        self.category = ProductCategory.objects.create(name='cat1')
        for i in range(10):
            Product.objects.create(
                name=f'prod-{i}',
                category=self.category,
                short_desc='shortdesc',
                description='description'
            )
        self.superuser = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password
        )

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, self.stop_word, status_code=self.status_ok)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)
        response = self.client.get('/')
        self.assertContains(response, self.stop_word, status_code=self.status_ok)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, self.status_redirect)

        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_redirect(self):
        product = Product.objects.first()
        response = self.client.get(f'/basket/add/{product.pk}/')
        self.assertEqual(response.status_code, self.status_redirect)

    def test_register(self):
        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)
        new_user_data = {
            'username': 'samuel',
            'first_name': 'Vincent',
            'last_name': 'Vega',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'v.vega@geekshop.local',
            'age': '21'}
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.status_redirect)
        new_user = ShopUser.objects.get(username=new_user_data['username'])
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{new_user_data['email']}/{new_user.activation_key}/"
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_ok)
        # данные нового пользователя
        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])
        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertFalse(response.context['user'].is_anonymous)
        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=self.status_ok)

    def test_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Sponge',
            'last_name': 'Bob',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'spongebob@geekshop.local',
            'age': '14'}
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.status_ok)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')
