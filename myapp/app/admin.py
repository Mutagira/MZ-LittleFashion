from django.contrib import admin
from .models import Category, Product, Customer, ShippingAddress,Cart, Order, ContactMessage

admin.site.site_header = 'MZ Administration'
admin.site.site_title = 'MZ'
admin.site.index_title = 'MZ Site'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'category', 'price', 'description')  
    list_filter = ('category',)
    search_fields = ('name', 'description')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'country')
    list_filter = ('city',)
    search_fields = ('user', 'city')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name','address_line', 'get_phone', 'get_city', 'get_country')
    list_filter = ('profile__city', 'profile__country')
    search_fields = ('full_name', 'profile__city',)

    def get_phone(self, obj):
        return obj.profile.phone
    get_phone.short_description = 'Phone'

    def get_city(self, obj):
        return obj.profile.city
    get_city.short_description = 'City'

    def get_country(self, obj):
        return obj.profile.country
    get_country.short_description = 'Country'

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('product',)
    search_fields = ('user', 'product')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity','shipping_cost','product_total','total_price','status',
        'payment_method','is_paid','order_date')
    list_filter = ('product',)
    search_fields = ('user', 'order_date', 'status')

    def product_total(self, obj):
        return f"Rs. {obj.product_total:.2f}"

    def total_price(self, obj):
        return f"Rs. {obj.total_price:.2f}"
    
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','message','created_at')
    list_filter = ('subject',)
    search_fields = ('created_at', 'subject')
    

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(ShippingAddress, AddressAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ContactMessage, ContactAdmin)
