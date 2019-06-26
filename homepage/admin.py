from django.contrib import admin
from .models import Item, Inventory,GroceryStore, Address, Order
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	fields = ['name','description']

class InventoryAdmin(admin.ModelAdmin):
	fields = ['item','price','stock','store']

class GroceryAdmin(admin.ModelAdmin):
	fields = ['name','address']

class AddressAdmin(admin.ModelAdmin):
	fields = ['addressee',
			  'street_name',
			  'suite','city',
			  'state_abbreviation',
			  'zip_code',
			  'Store']

class OrdersAdmin(admin.ModelAdmin):
	fields = ['ordered_inventory',
			  'date',
			  'total_price',
			  'delivery_choice',
			  'delivery_address',]

admin.site.register(Item,ItemAdmin)
admin.site.register(Inventory,InventoryAdmin)
admin.site.register(GroceryStore,GroceryAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Order,OrdersAdmin)