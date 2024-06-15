from django.contrib import admin

# Register your models here.

from srvmedicals.models import User,Product,Order,Cart,AboutUs,OrderItem

class UserAdmin(admin.ModelAdmin):
    list_display=("email","mobile_no","first_name","last_name","gender")

admin.site.register(User,UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=("id","product_name","product_desc","price","discount","availability","category","image")

admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=("id","user","product","quantity")

admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=("id","user","amount","prescription","quantity","discount","payment_method","payment_status","delivery_address","delivery_status")

admin.site.register(Order,OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display=("id","order","product","quantity")

admin.site.register(OrderItem,OrderItemAdmin)

class AboutUsAdmin(admin.ModelAdmin):
    list_display=("id","email","contact","address","description")

admin.site.register(AboutUs,AboutUsAdmin)
