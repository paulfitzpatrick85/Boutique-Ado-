from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)  # programmatic name
    friendly_name = models.CharField(max_length=254, null=True, blank=True)  # name on front end, both true value make this name optional

    def __str__(self):    # take in catagory model itself
        return self.name

    def get_friendly_name(self):  # same as above but for f name
        return self.friendly_name


class Product(models.Model):
    # allow to be null in database and blank in forms & if catagory is deleted will set product to have null rather than be deleted
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL) # foreign key to catagory model
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name   # returns product name