import json 
from homepage.models import Item

Item.objects.all().delete()