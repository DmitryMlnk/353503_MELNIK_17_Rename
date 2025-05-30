from django.contrib import admin
from .models import Client, Service, ServiceType, Master, MasterSpecialization, CarType, SparePart, SparePartType, \
    Order, OrderItem, Coupon, Contact, Review, FAQ, News

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(Master)
admin.site.register(MasterSpecialization)
admin.site.register(CarType)
admin.site.register(SparePart)
admin.site.register(SparePartType)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(News)
admin.site.register(Contact)
admin.site.register(Review)
admin.site.register(FAQ)