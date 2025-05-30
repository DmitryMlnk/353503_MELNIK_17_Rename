import json
import os
from functools import wraps
import requests
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now
from datetime import timedelta, timezone
from django.db.models import Count, Sum
from statistics import mean, median, mode
from main.models import Client, Service, ServiceType, Master, SparePart, SparePartType, \
    Order, OrderItem, Coupon, Contact, Review, FAQ, News
from main.forms import CustomUserCreationForm, ReviewForm, OrderForm
import logging

logger = logging.getLogger(__name__)


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'client') and request.user.client.role in roles:
                return view_func(request, *args, **kwargs)
            logger.warning(
                f"Unauthorized access attempt by {request.user.username if request.user.is_authenticated else 'anonymous'}")
            return redirect('/')

        return _wrapped_view

    return decorator


@login_required
def add_to_order(request, service_id=None, spare_part_id=None):
    logger.info(f"User {request.user.username} adding item to order")
    if service_id:
        item = get_object_or_404(Service, id=service_id)
        order, created = Order.objects.get_or_create(user=request.user, total_price=0)
        order_item, created = OrderItem.objects.get_or_create(order=order, service=item)
        if not created:
            order_item.quantity += 1
            order_item.save()
        logger.debug(f"Added service {item.name} to order {order.id}")
    elif spare_part_id:
        item = get_object_or_404(SparePart, id=spare_part_id)
        order, created = Order.objects.get_or_create(user=request.user, total_price=0)
        order_item, created = OrderItem.objects.get_or_create(order=order, spare_part=item)
        if not created:
            order_item.quantity += 1
            order_item.save()
        logger.debug(f"Added spare part {item.name} to order {order.id}")
    return redirect('services')


@login_required
def complete_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(user=request.user, total_price=0)
            order_items = OrderItem.objects.filter(order=order)
            total_price = 0
            for item in order_items:
                price = item.service.price if item.service else item.spare_part.price
                total_price += price * item.quantity
            order.total_price = total_price
            order.address = form.cleaned_data['address']
            order.scheduled_at = form.cleaned_data['scheduled_at']
            order.car_type = form.cleaned_data['car_type']
            order.master = form.cleaned_data['master']
            order.save()
            logger.info(f"Order {order.id} completed by {request.user.username}")
            return redirect('/')
        else:
            logger.error(f"Order form validation failed for {request.user.username}: {form.errors}")
    return redirect('/')


@login_required
def view_orders(request):
    user_role = request.user.client.role
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'created_at')
    orders = Order.objects.all() if user_role in ['admin', 'master'] else Order.objects.filter(user=request.user)
    if search_query:
        orders = orders.filter(user__username__icontains=search_query) | orders.filter(address__icontains=search_query)
    orders = orders.order_by(sort_by)
    logger.info(f"User {request.user.username} viewed orders with search '{search_query}' and sort '{sort_by}'")
    return render(request, 'view_orders.html', {'orders': orders, 'user_role': user_role})


@login_required
@role_required(['master', 'admin'])
def master_schedule(request):
    master = get_object_or_404(Master, user=request.user)
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'scheduled_at')
    orders = Order.objects.filter(master=master)
    if search_query:
        orders = orders.filter(user__username__icontains=search_query)
    orders = orders.order_by(sort_by)
    logger.info(f"Master {request.user.username} viewed schedule with search '{search_query}' and sort '{sort_by}'")
    return render(request, 'master_schedule.html', {'orders': orders})



def services(request, service_type=None):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    services = Service.objects.all()
    if service_type:
        services = services.filter(service_type__name=service_type)
    if search_query:
        services = services.filter(name__icontains=search_query) | services.filter(description__icontains=search_query)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)
    services = services.order_by(sort_by)
    service_types = ServiceType.objects.all()
    logger.info(f"User {request.user.username} viewed services with search '{search_query}' and sort '{sort_by}'")
    return render(request, 'services.html', {'services': services, 'service_types': service_types})


def spare_parts(request, spare_part_type=None):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    spare_parts = SparePart.objects.all()
    if spare_part_type:
        spare_parts = spare_parts.filter(spare_part_type__name=spare_part_type)
    if search_query:
        spare_parts = spare_parts.filter(name__icontains=search_query) | spare_parts.filter(
            description__icontains=search_query)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        spare_parts = spare_parts.filter(price__gte=min_price)
    if max_price:
        spare_parts = spare_parts.filter(price__lte=max_price)
    spare_parts = spare_parts.order_by(sort_by)
    spare_part_types = SparePartType.objects.all()
    logger.info(f"User {request.user.username} viewed spare parts with search '{search_query}' and sort '{sort_by}'")
    return render(request, 'spare_parts.html', {'spare_parts': spare_parts, 'spare_part_types': spare_part_types})


def index(request):
    # Подготовка контекста для даты и временной зоны
    user_timezone = pytz.timezone('Europe/Minsk')
    current_date = timezone.now().astimezone(user_timezone)
    utc_time = timezone.now().astimezone(pytz.UTC)
    # Текстовый календарь для текущего месяца
    cal = calendar.TextCalendar().formatmonth(current_date.year, current_date.month)

    context = {
        'current_date': current_date,
        'user_timezone': user_timezone.zone,
        'utc_time': utc_time,
        'calendar_text': cal
    }

    logger.debug(f"Доступ к главной странице для пользователя: {request.user.username if request.user.is_authenticated else 'anonymous'}")
    logger.info(f"Пользователь {request.user.username if request.user.is_authenticated else 'anonymous'} посетил главную страницу")
    return render(request, 'index.html', context)


def about(request):
    logger.info(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} accessed about")
    return render(request, 'about.html')


def contacts(request):
    contacts = Contact.objects.all()
    logger.info(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} accessed contacts")
    return render(request, 'contacts.html', {'contacts': contacts})


def coupons(request):
    coupons = Coupon.objects.all()
    logger.info(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} accessed coupons")
    return render(request, 'coupons.html', {'coupons': coupons})


def faq(request):
    faqs = FAQ.objects.all()
    logger.info(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} accessed faq")
    return render(request, 'faq.html', {'faqs': faqs})


def policy(request):
    logger.info(f"User {request.user.username if request.user.is_authenticated else 'anonymous'} accessed policy")
    return render(request, 'policy.html')


def review_list(request):
    reviews = Review.objects.all()
    logger.info(f"User {request.user.username} accessed review list")
    return render(request, 'review_list.html', {'reviews': reviews})


@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            logger.info(f"User {request.user.username} created review {review.id}")
            return redirect('review_list')
        else:
            logger.error(f"Review form validation failed for {request.user.username}: {form.errors}")
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form})


@login_required
def edit_review(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'PUT':
        data = json.loads(request.body)
        review.text = data.get('text', review.text)
        review.rating = data.get('rating', review.rating)
        review.save()
        return JsonResponse({'success': True})

    return render(request, 'edit_review.html', {'review': review})

@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'DELETE':
        review.delete()
        return JsonResponse({'success': True})

    return render(request, 'confirm_delete.html', {'review': review})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.utils import timezone
import logging
import pytz
import calendar

logger = logging.getLogger(__name__)

def login(request):
    # Подготовка контекста для даты и временной зоны
    user_timezone = pytz.timezone('Europe/Minsk')  # Из settings.TIME_ZONE
    current_date = timezone.now().astimezone(user_timezone)
    utc_time = timezone.now().astimezone(pytz.UTC)
    # Текстовый календарь для текущего месяца
    cal = calendar.TextCalendar().formatmonth(current_date.year, current_date.month)

    context = {
        'current_date': current_date,
        'user_timezone': user_timezone.zone,
        'utc_time': utc_time,
        'calendar_text': cal
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        logger.debug(f"Попытка входа для пользователя: {username}")

        if not username or not password:
            messages.error(request, 'Необходимо указать имя пользователя и пароль.')
            logger.warning(f"Пустое имя пользователя или пароль при попытке входа")
            return render(request, 'login.html', context)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                logger.info(f"Пользователь {username} успешно вошел")
                return redirect('/')
            else:
                messages.error(request, 'Ваш аккаунт неактивен. Обратитесь в поддержку.')
                logger.warning(f"Попытка входа неактивным аккаунтом: {username}")
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            logger.warning(f"Неуспешная попытка входа для пользователя: {username}")

        return render(request, 'login.html', context)

    # Обработка GET запроса
    context['next'] = request.GET.get('next', '')
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Client.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                age=(now().year - form.cleaned_data['birth_date'].year)
            )
            auth.login(request, user)
            logger.info(f"User {user.username} registered")
            return redirect('settings')
        else:
            messages.info(request, form.errors)
            logger.error(f"Registration failed: {form.errors}")
            return redirect('register')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def logout(request):
    logger.info(f"User {request.user.username} logged out")
    auth.logout(request)
    return redirect('login')


@login_required
def settings(request):
    user_client = Client.objects.get(user=request.user)
    if request.method == 'POST':
        user_client.address = request.POST['address']
        user_client.phone_number = request.POST['phone_number']
        user_client.save()
        logger.info(f"User {request.user.username} updated settings")
    return render(request, 'settings.html', {'user_client': user_client})


@role_required('admin')
def admin_dashboard(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'user__username')
    orders = Order.objects.all()
    clients = Client.objects.all()
    services = Service.objects.all()
    spare_parts = SparePart.objects.all()
    if search_query:
        clients = clients.filter(user__username__icontains=search_query) | clients.filter(
            address__icontains=search_query)
        services = services.filter(name__icontains=search_query) | services.filter(description__icontains=search_query)
        spare_parts = spare_parts.filter(name__icontains=search_query) | spare_parts.filter(
            description__icontains=search_query)
    clients = clients.order_by(sort_by)
    services = services.order_by(sort_by)
    spare_parts = spare_parts.order_by(sort_by)
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    logger.info(f"Admin {request.user.username} accessed dashboard with search '{search_query}' and sort '{sort_by}'")
    context = {
        'orders': orders,
        'clients': clients,
        'services': services,
        'spare_parts': spare_parts,
        'total_revenue': total_revenue
    }
    return render(request, 'admin_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='/')
def statistics(request):
    # Clients and services in alphabetical order
    clients = Client.objects.order_by('user__username')
    services = Service.objects.order_by('name')

    # Total sales
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Sales statistics
    sales = [order.total_price for order in Order.objects.all()]
    sales_avg = mean(sales) if sales else 0
    sales_median = median(sales) if sales else 0
    sales_mode = mode(sales) if sales else 0

    # Client age statistics
    ages = [client.age for client in Client.objects.all()]
    age_avg = mean(ages) if ages else 0
    age_median = median(ages) if ages else 0

    # Most popular service type
    popular_service_type = ServiceType.objects.annotate(total_orders=Count('services__orderitem')).order_by(
        '-total_orders').first()

    # Most profitable service type
    profitable_service_type = ServiceType.objects.annotate(
        total_profit=Sum('services__orderitem__order__total_price')).order_by('-total_profit').first()

    # Count orders by service type
    service_types = ServiceType.objects.annotate(total_orders=Count('services__orderitem')).order_by('-total_orders')

    service_names = [service.name for service in service_types]
    order_counts = [service.total_orders for service in service_types]

    # Create a directory if it doesn't exist
    chart_dir = 'media/'
    os.makedirs(chart_dir, exist_ok=True)

    # Create a bar chart for orders by service type
    plt.figure(figsize=(10, 5))
    plt.bar(service_names, order_counts, color='lightcoral')
    plt.title('Orders by Service Type')
    plt.xlabel('Service Type')
    plt.ylabel('Number of Orders')
    plt.xticks(rotation=45, ha='right')

    # Save the figure
    chart_path = os.path.join(chart_dir, 'orders_by_service_type.png')
    plt.savefig(chart_path)
    plt.close()

    context = {
        'clients': clients,
        'services': services,
        'total_sales': total_sales,
        'sales_avg': sales_avg,
        'sales_median': sales_median,
        'sales_mode': sales_mode,
        'age_avg': age_avg,
        'age_median': age_median,
        'popular_service_type': popular_service_type,
        'profitable_service_type': profitable_service_type,
        'chart_path': chart_path
    }
    logger.info(f"Admin {request.user.username} accessed statistics")
    return render(request, 'statistics.html', context)


def news(request):
    # Подготовка контекста для даты и временной зоны
    user_timezone = pytz.timezone('Europe/Minsk')
    current_date = timezone.now().astimezone(user_timezone)
    utc_time = timezone.now().astimezone(pytz.UTC)
    cal = calendar.TextCalendar().formatmonth(current_date.year, current_date.month)

    # Получение списка новостей
    news_list = News.objects.all()

    context = {
        'current_date': current_date,
        'user_timezone': user_timezone.zone,
        'utc_time': utc_time,
        'calendar_text': cal,
        'news_list': news_list
    }

    logger.debug(f"Доступ к странице новостей для пользователя: {request.user.username if request.user.is_authenticated else 'anonymous'}")
    logger.info(f"Пользователь {request.user.username if request.user.is_authenticated else 'anonymous'} посетил страницу новостей")
    return render(request, 'news.html', context)

def news_detail(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news_detail.html', {'news': news})

def random_joke(request):
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        joke_setup = data["setup"]
        joke_punchline = data["punchline"]
    else:
        joke_setup = "ошибка"
        joke_punchline = "ошибка"
    return render(request, 'random_joke.html', context={'joke_setup': joke_setup, 'joke_punchline': joke_punchline})

def cat_fact(request):
    api_url = "https://catfact.ninja/fact"
    response = requests.get(api_url)
    print('response', response.json())
    if response.status_code == 200:
        cat_fact = response.json()['fact']
    else:
        cat_fact = "ошибка"
    context = {'cat_fact': cat_fact}
    return render(request, 'cat_fact.html', context)
