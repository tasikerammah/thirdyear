from django.contrib import admin
from products.models import Product, Category

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug', 'is_digital','image']
	prepopulated_fields = {'slug': ('title',)}

	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name','created_at','updated_at')
	list_display_links = ('name',)
	list_per_page = 20
	ordering = ['name',]
	search_fields = ['name', 'description',]
	exclude = ('created_at', 'updated_at')
	# set up slug to generated from name
	prepopulated_fields = {'slug': ('name',)}
	
admin.site.register(Category,CategoryAdmin)
