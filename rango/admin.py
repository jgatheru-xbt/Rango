# Register your models here so that you can benefit from Django admin interface.

from django.contrib import admin
from rango.models import Category, Page




class CategoryAdmin(admin.ModelAdmin):
    # 'slug' is the target field, ('name',) is the source field tuple
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
