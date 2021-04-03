from django.contrib import admin
from .models import Law, LawCategory, LawInnerCategory

# Customised Admin view for Block users List
class LawAdmin(admin.ModelAdmin):
    list_display = ('id', 'laws','is_active')
    list_display_links = ('id','laws')



# Customised Admin view for Block users List
class LawCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','is_active')
    list_display_links = ('id','name')
    ordering = ['id']

class LawInnerCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description_1','description_2','law','summary_offence','indictable_offence','is_active','sentence_by_magistrate', 'appeal_court', 'max_setence', 'a_f', 'm_f','keywords','plead')
    list_display_links = ('id','name')
    ordering = ['id']

# Registering the Admin View
admin.site.register(Law, LawAdmin)
admin.site.register(LawCategory, LawCategoryAdmin)
admin.site.register(LawInnerCategory, LawInnerCategoryAdmin)
