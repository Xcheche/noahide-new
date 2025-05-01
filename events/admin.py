from django.contrib import admin
from .models import Event

# Register your models here.



class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
   
    date_hierarchy = 'created_at'
    list_per_page = 10
    actions_on_top = True
    # actions_on_bottom = True
    save_on_top = True
    
    
admin.site.register(Event, EventAdmin)    
    