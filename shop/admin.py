from django.contrib import admin
from .models import AdminUser, Cart,Category,Customer,CartProduct,Product,Order,ProductImage
# Register your models here.
lis=[Cart,Category,Customer,CartProduct,Product,Order,AdminUser,ProductImage]
admin.site.register(lis)
