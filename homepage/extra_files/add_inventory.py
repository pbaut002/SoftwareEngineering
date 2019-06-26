from homepage.models import Item, Inventory, GroceryStore 
import random 


# Choose random item in the model

def get_random(modelName):
    return modelName.objects.order_by("?").first()


# Enter 50 items into the database
for x in range(0,50):
	curr_item = get_random(Item)
	grocery_item = curr_item.name
	random_price = random.randint(99,2400)/100 # Choose price from $0.99 to $24.00
	random_quant = random.randint(0,301) # Choose a random quantity from 0 to 100
	gstore = get_random(GroceryStore)
	try:
		new_inventory = Inventory(item=curr_item,price=random_price,stock=random_quant,store=gstore)
		new_inventory.save()
	except:
		pass

