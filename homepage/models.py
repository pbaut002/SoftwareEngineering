from django.db import models

# An address, to be used by grocery stores and users for shipping alike
class Address(models.Model):
	
	class Meta:
		ordering = ['addressee']  # Order items in ascending order
		verbose_name_plural = "Addresses"


	addressee = models.CharField(max_length=50)
	street_name = models.CharField(max_length=50)
	suite = models.IntegerField(blank=True,null=True)
	city = models.CharField(max_length=20)
	state_abbreviation = models.CharField(max_length=2)
	zip_code = models.DecimalField(max_digits=5, decimal_places=0)
	Store = models.BooleanField(default=False,null=False,blank=False)
	# Addresses have many-to-one relationships with Orders and GroceryStores
	
	def __str__(self):
		return (
			self.addressee + "\n" +
			" " + self.street_name + ((", #" + str(self.suite)) if self.suite else "") + "\n" +
			self.city + ", " + self.state_abbreviation + " " + str(self.zip_code)
		)



# A grocery store connected to our website
class GroceryStore(models.Model):
	
	class Meta:
		ordering = ['name']  # Order items in ascending order
		verbose_name_plural = "Grocery Stores"

	name = models.CharField(max_length=50)
	address = models.ForeignKey(Address, 
								on_delete=models.CASCADE,
								limit_choices_to={'Store':True},)
	# GroveryStores have a many-to-one relationship with Inventory

	def __str__(self):
		return self.name



# Items are types of product like apples
class Item(models.Model):

	class Meta:
		ordering = ['name'] # Order items in ascending order

	name = models.CharField(primary_key=True,max_length=50)
	description = models.TextField(blank=True)
	# Items have a many-to-one relationship with Inventory
	
	
	def __str__(self):
		return self.name



# Inventory instances contain the price and stock for a specific Item at a specific GroceryStore
class Inventory(models.Model):
	
	class Meta:
		ordering = ['store','item']  # Order items in ascending order
		verbose_name_plural = "Inventory"
		constraints = [models.UniqueConstraint(fields=['item','store'],name='Item_Store')]

	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	stock = models.IntegerField()
	store = models.ForeignKey(GroceryStore, on_delete=models.CASCADE)
	# Inventory items have many-to-many relationships with Orders

	def __str__(self):
		return self.item.name + " " + self.store.name + " $" + str(self.price) + " " + str(self.stock)



# Orders placed by the customer
class Order(models.Model):
	# order_number is the "id" field which Django automatically generates
	# 
	class Meta:
		ordering = ['id']

	ordered_inventory = models.ManyToManyField(Inventory)
	date = models.DateField()
	total_price = models.DecimalField(max_digits=9, decimal_places=2)
	DELIVERY_METHODS = (
		('P', 'Pickup'),
		('D', 'Delivery') 
	)
	delivery_choice = models.CharField(max_length=1, choices=DELIVERY_METHODS)
	delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return str(self.id)
