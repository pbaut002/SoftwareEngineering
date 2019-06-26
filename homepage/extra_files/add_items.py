import json 
from homepage.models import Item

# Choose csv with item_name and description to fill up items

path = './homepage/MOCK_DATA.json'
with open(path) as json_file:
	data = json.load(json_file)
	for item in data:
		items = Item(name=item['Item_name'],description=item['Description'])
		items.save()


print("Success")