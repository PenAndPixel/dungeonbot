from django.contrib import admin
from django.conf import settings
from . import models



class BonusItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_quality_display', 'get_item_display', 'get_effect_display', 'total']


__custom_admins__ = {
    'BonusItem': BonusItemAdmin ,
    }




for model in models.__admin__:
    params = [getattr(models, model)]
    if model in __custom_admins__:
        params.append(__custom_admins__[model])
    else:
        _dyn_class = type('%sAdmin' % ( str(model),), (admin.ModelAdmin,), {})
        #( VersionAdmin, ), {} )
        params.append(_dyn_class)
    admin.site.register(*params)
