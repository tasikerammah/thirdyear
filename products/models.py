from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from ecommerce.utils import unique_slug_generator


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(price__icontains=query) |
                  Q(tag__title__icontains=query)
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class ActiveCategoryManager(models.Manager):
	def get_query_set(self):
		return super(ActiveCategoryManager,self).get_query_set().filter(active=True)


class Category(models.Model):
	name        = models.CharField(max_length=50)
	slug        = models.SlugField(max_length=50,unique=True,
	                         help_text='Unique value for product '
	                                   'page URL, created from name')
	description = models.TextField()
	active      = models.BooleanField(default=True)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at  = models.DateTimeField(auto_now=True)

	objects     = ActiveCategoryManager()
	
	class Meta:
		db_table = 'categories'
		ordering = ['-created_at']
		verbose_name_plural = 'categories'
		
	def __str__(self):
		return self.name

class Product(models.Model):
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True, unique=True)
    description     = models.TextField()
    image           = models.ImageField(blank=False,default='')
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    is_digital      = models.BooleanField(default=False) # User Library
    category        = models.ForeignKey(Category,blank=True,null=True, on_delete=models.CASCADE)
	

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product) 


