import json 
from homepage.models import Item
import mysql.connector

# Choose csv with item_name and description to fill up items

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="peter",
#   passwd="password",
#   database="cpsc362"
# )


# mycursor = mydb.cursor()

path = './homepage/MOCK_DATA.json'
with open(path) as json_file:
	data = json.load(json_file)
	for item in data:
		items = Item(name=item['Item_name'],description=item['Description'])
		items.save()


print("Success")