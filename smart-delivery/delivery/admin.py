from django.contrib import admin
from .models import ChatMessage, Customer, Delivery, Driver, StatusHistory, User


admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Delivery)
admin.site.register(StatusHistory)
admin.site.register(ChatMessage)