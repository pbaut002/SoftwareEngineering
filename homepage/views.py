from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from .models import Item, Inventory, Order, Address
from django.urls import reverse
import datetime

# Create your views here.

def homepage(request):

	# Setup request sessions
	# If cart/quantity does not exist since user hasn't visited, then create a new variable.
	if 'cart_id' not in request.session or 'cart_quant' not in request.session:
		# Note: Make a temporary cart object with placeholders
		request.session.flush()
		new_cart = Order(date=datetime.datetime.now(),total_price=0,
						 delivery_address=Address.objects.all().first(),
						 delivery_choice='D')
		new_cart.save()
		request.session['cart_id'] = new_cart.id
		request.session['cart_quant'] = {}
	

	#  Get the list of inventory items and separate them into pages
	item_list = Inventory.objects.all()
	paginator = Paginator(item_list, 15)
	page = request.GET.get('page')
	
	try:
		InventoryList = paginator.page(page)
	except PageNotAnInteger:
		InventoryList = paginator.page(1)
	except EmptyPage:
		InventoryList = paginator.page(paginator.num_pages)
	
	return render(request=request, 
				  template_name="homepage/home.html", # Where to find the html file
				  context={"Inventory":InventoryList}) # We can pass Tutorial objects via the name "tutorials"


def add_to_cart(request, item):
	
	# Add an item to the cart

	# Check if web page sent a POST request. 
	if request.POST:
		inventory_item = get_object_or_404(Inventory, pk=item) # Chooses item that was passed in
		chosen_quantity = request.POST.getlist('quantities') # Get from field quantities
		chosen_quantity = int(chosen_quantity[0])
		
		# Add to request session 'cart'
		if(chosen_quantity > 0 and inventory_item):
			
			# Retrieve cart ID and order
			# Also update quantity
			cart_id = request.session['cart_id']
			cart = Order.objects.get(id=cart_id)
			cart.ordered_inventory.add(inventory_item)
			cart_quantity = request.session['cart_quant']
			cart_quantity[inventory_item.id] = chosen_quantity
			print(cart_quantity)
			print(cart_quantity)
			request.session.modified = True
			cart.total_price += chosen_quantity * inventory_item.price
			cart.save()

			# Display to the user that the item was successfully added to the cart.
			success_string = "%d %s added to Cart" % (chosen_quantity,inventory_item.item)
			messages.success(request, success_string)
		
		else:
			# If item is not successfully added to the cart, then display that the action was invalid.
			messages.error(request, "Sorry, you can't do that")
		
		return redirect(reverse('homepage:homepage'))
	

def order_page(request):

	# Retrieve object

	cart = Order.objects.get(id=request.session['cart_id'])
	cart_items = cart.ordered_inventory.all()

	store_list = []
	for item in cart_items:
		if item.store not in store_list:
			store_list.append(item.store)
	cart_quantity = request.session['cart_quant']
	
	if len(store_list) > 1:
		messages.warning(request, "You have items in your cart that are from different stores!")

	return render(request=request,
					  template_name="homepage/orders.html",
					  context={"cart":cart, "items":cart.ordered_inventory.all(),"inventory_quantities":cart_quantity})

def submit_order(request):

	if request.POST:
		# Address:
		order_address = {}
		try:
			order_address['first_name'] = request.POST.getlist("First_Name")[0]
			order_address['last_name'] = request.POST.getlist("Last_Name")[0]
			order_address['email'] = request.POST.getlist("email")[0]
			order_address['address'] = request.POST.getlist("address")[0]
			order_address['city'] = request.POST.getlist("city")[0]
			order_address['zip_code'] = request.POST.getlist("zip_code")[0]
			order_address['country'] = request.POST.getlist("country")[0]
			order_address['state'] = request.POST.getlist("state")[0]
		except IndexError:
			messages.error(request,"Please enter everything")
			return redirect(reverse('homepage:orders'))	

		for address in order_address:
			if not order_address[address]:
				messages.error(request,"Oh no! %s is missing." % address)
				return redirect(reverse('homepage:orders'))	
		

		# Card information
		card_info = {}
		card_info['card_name']= request.POST.getlist("name_on_card")[0]
		card_info['card_month'] = request.POST.getlist("month")[0]
		card_info['card_year']= request.POST.getlist("year")[0]

		for info in card_info:
			if not card_info[info]:
				messages.error(request,"Oh no! %s is missing." % info)
				return redirect(reverse('homepage:orders'))		

		# Shipping Information
		shipping = request.POST.getlist("shipping_button")
		final_shipping = {}
		if not shipping:
			final_shipping['first_name'] = request.POST.getlist("First_Name")[0]
			final_shipping['last_name'] = request.POST.getlist("Last_Name")[0]
			final_shipping['email'] = request.POST.getlist("email")[0]
			final_shipping['address']= request.POST.getlist("address")[0]
			final_shipping['city'] = request.POST.getlist("city")[0]
			final_shipping['zip_code'] = request.POST.getlist("zip_code")[0]
			final_shipping['country'] = request.POST.getlist("country")[0]
			final_shipping['state'] = request.POST.getlist("state")[0]
		else:
			final_shipping = order_address
		
		current_cart = Order.objects.get(id=request.session['cart_id'])
		
		if request.POST.getlist("Delivery")[0] == 'D':
			current_cart.delivery_choice = request.POST.getlist("Delivery")[0]
			current_cart.total_price += 5

		cart_quantity = request.session['cart_quant']
		
		for items in cart_quantity.keys():
			print(items)
			current_inventory = current_cart.ordered_inventory.get(id=str(items))		
			if current_inventory:
				# Check if item exists, otherwise send an error message
				if current_inventory.stock - cart_quantity[items] < 0:
					# Check if user is trying to buy more than what is in stock
					messages.error(request, "I'm sorry, there's not enough %s in stock." % current_inventory.item)
					return redirect(reverse('homepage:orders'))
				else:
					current_inventory.stock -= cart_quantity[items]
					current_inventory.save()
			else:
				messages.error(request, "Oh no! The item was deleted from inventory");
				return redirect(reverse('homepage:orders'))
		

		current_cart.date = datetime.datetime.now()
		new_address = Address(addressee=final_shipping['first_name'] + " " + final_shipping['last_name'],
												street_name=final_shipping['address'],
												city=final_shipping['city'],
												state_abbreviation=final_shipping['state'],
												zip_code=final_shipping['zip_code'],)
		new_address.save()
		
		current_cart.delivery_address = new_address
		current_cart.delivery_address.save()
		current_cart.save()

		messages.success(request, "Order successfully entered. Confirmation Number #%d" % request.session['cart_id'])
		request.session.flush()
		
		
	return redirect(reverse('homepage:homepage'))




def search_page(request):

	# Render page where users can search for items
	return render(request=request,
				  template_name="homepage/search.html",
				 )

def search(request):

	# Retrieve what items what searched for in search page

	if request.GET:		
		search_item = request.GET.getlist("search") 
		search_string = search_item[0] # Retrieve the string that was searched

		# Retrieve the list of objects that contain the search string
		found_items = Inventory.objects.filter(item__name__icontains=search_string)


		if found_items:
			# If an item is found then redirect to a page with the list of items
			# that contained the search string
			return render(request=request, 
				  template_name="homepage/searchlist.html", # Where to find the html file
				  context={"Inventory":found_items}) 
		else:
			# If item is not found, then redirect back to the search page and output
			# The item was not found
			messages.error(request, "Item: %s not found" % search_string)
			return redirect(reverse('homepage:search'))

def cart(request):
	currentCart = Order.objects.get(id=request.session['cart_id'])
	items = currentCart.ordered_inventory.all()

	return render(request = request, 
                  template_name="homepage/cart.html",
                  context={"items":currentCart.ordered_inventory.all(),
				  		   "inventory_quantities":request.session['cart_quant'],
						   "cart_total":currentCart.total_price})

def remove_from_cart(request, item):
	inventory_item = get_object_or_404(Inventory, pk=item)
	cart_id = request.session['cart_id']
	cart = Order.objects.get(id=cart_id)
	quant_dictionary = request.session['cart_quant']
	item_quantity = quant_dictionary[str(inventory_item.id)]

	cart.total_price -= inventory_item.price * item_quantity
	del request.session['cart_quant'][str(inventory_item.id)]
	request.session.modified = True
	cart.ordered_inventory.remove(inventory_item)
	cart.save()

	return redirect(reverse('homepage:cart'))

def retrieve_order(request):
	try:
		order_number = Order.objects.get(id=request.GET.getlist("confirmation")[0])
	except Order.DoesNotExist:
		messages.error(request,"I'm sorry that order number doesn't exist.")
		return redirect(reverse('homepage:orders'))

	cart_list = order_number.ordered_inventory.all()

	store_list = []
	
	for item in cart_list:
		if item.store not in store_list:
			store_list.append(item.store)

	return render(request=request,
				  template_name="homepage/order_page.html",
				  context={"order" : order_number,"items": cart_list,"stores" : store_list})
