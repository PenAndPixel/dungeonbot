from django.contrib import admin
from . import models
#from mptt.admin import MPTTModelAdmin

#from reversion.admin import VersionAdmin

#class QualificationInline(admin.TabularInline):
#    model = c_models.Qualification

#class CourseAdmin(admin.ModelAdmin):
#    inlines = [
#        QualificationInline,
#    ]

__custom_admins__ = {

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
