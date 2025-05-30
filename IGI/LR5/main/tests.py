from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client, Service, ServiceType, Master, MasterSpecialization, CarType, SparePart, SparePartType, Order, OrderItem, Coupon, Contact, Review, FAQ
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.test import APIClient

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client_obj = Client.objects.create(
            user=self.user,
            phone_number='+375(29)123-45-67',
            address='Test Address',
            role='customer',
            age=25
        )
        self.service_type = ServiceType.objects.create(name='Diagnostics', description='Car diagnostics')
        self.service = Service.objects.create(
            name='Oil Change',
            description='Engine oil change service',
            price=50.00,
            service_type=self.service_type
        )
        self.master_specialization = MasterSpecialization.objects.create(name='Mechanic', description='General mechanic')
        self.master = Master.objects.create(
            user=self.user,
            specialization=self.master_specialization,
            phone_number='+375(29)123-45-67',
            hire_date=datetime.now()
        )
        self.car_type = CarType.objects.create(name='Sedan', description='Standard sedan car')
        self.spare_part_type = SparePartType.objects.create(name='Oil Filter', description='Engine oil filters')
        self.spare_part = SparePart.objects.create(
            name='Oil Filter X',
            description='High-quality oil filter',
            price=20.00,
            spare_part_type=self.spare_part_type
        )
        self.order = Order.objects.create(
            user=self.user,
            car_type=self.car_type,
            master=self.master,
            address='Test Address',
            total_price=70.00
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            service=self.service,
            quantity=1
        )
        self.coupon = Coupon.objects.create(
            title='Test Coupon',
            description='Test Description',
            number='12345',
            active=True
        )
        self.contact = Contact.objects.create(
            title='Test Contact',
            description='Test Description',
            phone_number='+375(29)123-45-67',
            email='test@example.com'
        )
        self.review = Review.objects.create(
            user=self.user,
            rating=5,
            text='Test Review'
        )
        self.faq = FAQ.objects.create(
            question='Test Question',
            answer='Test Answer'
        )

    def test_client_creation(self):
        self.assertEqual(self.client_obj.phone_number, '+375(29)123-45-67')
        self.assertEqual(self.client_obj.address, 'Test Address')
        self.assertEqual(self.client_obj.role, 'customer')
        self.assertEqual(self.client_obj.age, 25)

    def test_service_creation(self):
        self.assertEqual(self.service.name, 'Oil Change')
        self.assertEqual(self.service.description, 'Engine oil change service')
        self.assertEqual(self.service.price, 50.00)
        self.assertEqual(self.service.service_type, self.service_type)

    def test_master_creation(self):
        self.assertEqual(self.master.user, self.user)
        self.assertEqual(self.master.specialization, self.master_specialization)

    def test_car_type_creation(self):
        self.assertEqual(self.car_type.name, 'Sedan')
        self.assertEqual(self.car_type.description, 'Standard sedan car')

    def test_spare_part_creation(self):
        self.assertEqual(self.spare_part.name, 'Oil Filter X')
        self.assertEqual(self.spare_part.description, 'High-quality oil filter')
        self.assertEqual(self.spare_part.price, 20.00)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.car_type, self.car_type)
        self.assertEqual(self.order.master, self.master)
        self.assertEqual(self.order.total_price, 70.00)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.service, self.service)
        self.assertEqual(self.order_item.quantity, 1)

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.title, 'Test Coupon')
        self.assertEqual(self.coupon.number, '12345')
        self.assertTrue(self.coupon.active)

    def test_contact_creation(self):
        self.assertEqual(self.contact.title, 'Test Contact')
        self.assertEqual(self.contact.email, 'test@example.com')

    def test_review_creation(self):
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.text, 'Test Review')

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, 'Test Question')
        self.assertEqual(self.faq.answer, 'Test Answer')

class ViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.service_type = ServiceType.objects.create(name='Diagnostics')
        self.service = Service.objects.create(name='Oil Change', description='Test', price=50.00, service_type=self.service_type)
        self.spare_part_type = SparePartType.objects.create(name='Oil Filter')
        self.spare_part = SparePart.objects.create(name='Oil Filter X', description='Test', price=20.00, spare_part_type=self.spare_part_type)
        self.car_type = CarType.objects.create(name='Sedan')
        self.master_specialization = MasterSpecialization.objects.create(name='Mechanic')
        self.master = Master.objects.create(user=self.user, specialization=self.master_specialization, phone_number='+375(29)123-45-67')
        self.order = Order.objects.create(user=self.user, car_type=self.car_type, master=self.master, address='Test Address', total_price=70.00)
        self.order_item = OrderItem.objects.create(order=self.order, service=self.service, quantity=1)
        self.coupon = Coupon.objects.create(title='Test Coupon', description='Test', number='12345', active=True)
        self.contact = Contact.objects.create(title='Test Contact', description='Test', phone_number='+375(29)123-45-67', email='test@example.com')
        self.review = Review.objects.create(user=self.user, rating=5, text='Test Review')
        self.faq = FAQ.objects.create(question='Test Question', answer='Test Answer')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')
        self.api_client = APIClient()

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_services_view(self):
        response = self.client.get('/services/?search=Oil')
        self.assertEqual(response.status_code, 200)

    def test_spare_parts_view(self):
        response = self.client.get('/spare_parts/?search=Filter')
        self.assertEqual(response.status_code, 200)

    def test_view_orders_view(self):
        response = self.client.get('/view_orders/?search=testuser')
        self.assertEqual(response.status_code, 200)

    def test_master_schedule_view(self):
        response = self.client.get('/master_schedule/?search=testuser')
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/admin_dashboard/?search=Oil')
        self.assertEqual(response.status_code, 200)

    def test_statistics_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get('/statistics/')
        self.assertEqual(response.status_code, 200)

    def test_api_service_list_authenticated(self):
        self.api_client.login(username='testuser', password='testpassword')
        response = self.api_client.get('/api/services/')
        self.assertEqual(response.status_code, 200)

    def test_api_service_list_unauthenticated(self):
        response = self.api_client.get('/api/services/')
        self.assertEqual(response.status_code, 401)

    def test_add_to_order_service_view(self):
        response = self.client.get(f'/add_to_order/service/{self.service.id}/')
        self.assertEqual(response.status_code, 302)

    def test_add_to_order_spare_part_view(self):
        response = self.client.get(f'/add_to_order/spare_part/{self.spare_part.id}/')
        self.assertEqual(response.status_code, 302)

    def test_complete_order_view(self):
        response = self.client.post('/complete_order/', {
            'address': 'Test Address',
            'scheduled_at': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'car_type': self.car_type.id,
            'master': self.master.id
        })
        self.assertEqual(response.status_code, 302)

    def test_contacts_view(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_coupons_view(self):
        response = self.client.get('/coupons/')
        self.assertEqual(response.status_code, 200)

    def test_faq_view(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)

    def test_review_list_view(self):
        response = self.client.get('/review_list/')
        self.assertEqual(response.status_code, 200)

    def test_create_review_view(self):
        response = self.client.get('/review_list/create_review/')
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_settings_view(self):
        response = self.client.get('/settings/')
        self.assertEqual(response.status_code, 200)