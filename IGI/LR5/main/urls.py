from django.urls import path
from django.conf.urls.static import static
from autoservice import settings
from . import views, api

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('coupons/', views.coupons, name='coupons'),
    path('faq/', views.faq, name='faq'),
    path('policy/', views.policy, name='policy'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('services/', views.services, name='services'),
    path('services/<str:service_type>/', views.services, name='services_by_type'),
    path('spare_parts/', views.spare_parts, name='spare_parts'),
    path('spare_parts/<str:spare_part_type>/', views.spare_parts, name='spare_parts_by_type'),
    path('add_to_order/service/<int:service_id>/', views.add_to_order, name='add_service_to_order'),
    path('add_to_order/spare_part/<int:spare_part_id>/', views.add_to_order, name='add_spare_part_to_order'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('master_schedule/', views.master_schedule, name='master_schedule'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('review_list/', views.review_list, name='review_list'),
    path('review_list/create_review/', views.create_review, name='create_review'),
    path('review_list/edit_review/<int:id>/', views.edit_review, name='edit_review'),
    path('review_list/delete_review/<int:id>/', views.delete_review, name='delete_review'),
    path('statistics/', views.statistics, name='statistics'),
    path('news/', views.news, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('random_joke/', views.random_joke, name='random_joke'),
    path('cat_fact/', views.cat_fact, name='cat_fact'),
    path('api/services/', api.service_list, name='api_service_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)