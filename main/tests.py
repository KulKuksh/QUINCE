from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Category, Dish, CartItem, Order, Review
from main.utils import calculate_delivery_cost
from decimal import Decimal

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            phone='+71234567890',
            email='test@example.com'
        )
        self.category = Category.objects.create(name='Салаты')
        # Принудительно задаём slug, так как авто-генерация не работает
        self.category.slug = 'salaty'
        self.category.save()

        self.dish = Dish.objects.create(
            name='Цезарь',
            price=Decimal('350.00'),
            category=self.category,
            composition='Курица, сыр, салат, сухарики',
            nutrition='350 ккал'
        )
        self.dish.slug = 'cezar'
        self.dish.save()

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.role, 'user')
        self.assertTrue(self.user.check_password('12345'))


    def test_cart_item_get_total(self):
        item = CartItem.objects.create(user=self.user, dish=self.dish, quantity=2)
        self.assertEqual(item.get_total(), Decimal('700.00'))

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            address='ул. Ленина, 1',
            phone='+71234567890',
            total_amount=Decimal('550.00'),
            delivery_cost=Decimal('200.00')
        )
        self.assertEqual(order.status, 'принят')

    def test_review_creation(self):
        review = Review.objects.create(user=self.user, text='Отлично!', rating=5)
        self.assertEqual(review.status, 'pending')


class DeliveryCostTests(TestCase):
    def test_delivery_pickup(self):
        self.assertEqual(calculate_delivery_cost(Decimal('500'), 'pickup'), 0)

    def test_delivery_inside_ge_above_1200(self):
        result = calculate_delivery_cost(Decimal('1500'), 'delivery_inside', True)
        self.assertEqual(result, 0)

    def test_delivery_inside_ge_below_1200(self):
        result = calculate_delivery_cost(Decimal('800'), 'delivery_inside', True)
        self.assertEqual(result, 200)

    def test_delivery_outside_ge_any_amount(self):
        result = calculate_delivery_cost(Decimal('500'), 'delivery_outside')
        self.assertEqual(result, 200)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            phone='+71234567890'
        )
        self.category = Category.objects.create(name='Пицца')
        self.category.slug = 'pizza'
        self.category.save()

        self.dish = Dish.objects.create(
            name='Маргарита',
            price=Decimal('450.00'),
            category=self.category
        )
        self.dish.slug = 'margarita'
        self.dish.save()

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_menu_page_status(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)

    

    def test_cart_requires_login(self):
        response = self.client.get(reverse('cart'))
        expected_url = f'{reverse("login")}?next={reverse("cart")}'
        self.assertRedirects(response, expected_url)

    def test_add_to_cart_requires_login(self):
        response = self.client.get(reverse('add_to_cart', args=[self.dish.id]))
        expected_url = f'{reverse("login")}?next={reverse("add_to_cart", args=[self.dish.id])}'
        self.assertRedirects(response, expected_url)

    def test_add_to_cart_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_to_cart', args=[self.dish.id]))
        self.assertRedirects(response, reverse('menu'))
        self.assertTrue(CartItem.objects.filter(user=self.user, dish=self.dish).exists())

    def test_cart_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        CartItem.objects.create(user=self.user, dish=self.dish, quantity=2)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_order_history_requires_login(self):
        response = self.client.get(reverse('order_history'))
        expected_url = f'{reverse("login")}?next={reverse("order_history")}'
        self.assertRedirects(response, expected_url)

    def test_add_review_requires_login(self):
        response = self.client.get(reverse('add_review'))
        expected_url = f'{reverse("login")}?next={reverse("add_review")}'
        self.assertRedirects(response, expected_url)

    def test_add_review_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_review'), {'text': 'Отлично!', 'rating': 5})
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Review.objects.filter(user=self.user, text='Отлично!').exists())

    def test_register_page_status(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_valid_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone': '+71234567890',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_invalid_registration_phone(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'email': 'new2@example.com',
            'phone': '12345',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser2').exists())

    def test_login_page_status(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('home'))


class IntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            phone='+71234567890'
        )
        self.category = Category.objects.create(name='Десерты')
        

        self.dish = Dish.objects.create(
            name='Тирамису',
            price=Decimal('320.00'),
            category=self.category
        )
        

    def test_full_order_flow(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.get(reverse('add_to_cart', args=[self.dish.id]))
        self.client.post(reverse('checkout'), {
            'address': 'ул. Тестовая, 10',
            'phone': '+71234567890',
            'delivery_type': 'delivery_inside',
            'comment': 'До 20:00'
        })
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        self.client.post(reverse('add_review'), {'text': 'Отличный сервис!', 'rating': 5})
        self.assertTrue(Review.objects.filter(user=self.user, text='Отличный сервис!').exists())