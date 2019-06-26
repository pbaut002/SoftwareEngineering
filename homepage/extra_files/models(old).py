from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length=200)
	tutorial_content = models.TextField()
	tutorial_published = models.DateTimeField("date published")

	def __str__(self):
		return self.tutorial_title

class Item(models.Model):
	item_name = models.CharField(max_length=50)
	item_price = models.DecimalField(max_digits=7,decimal_places=2)
	store1_quant = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(999)])
	store2_quant = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(999)])
	store3_quant = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(999)])
	store4_quant = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(999)])


	def __str__(self):
		return self.item_name
