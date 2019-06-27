from django import template
import math

register = template.Library()

def get_stock(value):
	if(value == 1):
		return range(2)
	stock = math.floor(value/4)

	if(stock < 10 and stock >= 0):
		return range(value)
	elif(stock == 0):
		return range(0)
	else:
		return range(13)
	
def get_quant(dictionary, key):
	return dictionary[str(key)]

def card_year(year):
	return range(2019,year)

def card_month(start_month):
	return range(start_month,13)


register.filter('get_stock',get_stock)
register.filter('get_quant',get_quant)
register.filter('card_year',card_year)
register.filter('card_month',card_month)
