from new import classobj
from django.contrib import admin
#from mptt.admin import MPTTModelAdmin

#from reversion.admin import VersionAdmin

import models

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
    if __custom_admins__.has_key(model):
        params.append(__custom_admins__[model])
    else:
        _dyn_class = classobj('%sAdmin' % (model,),
            (admin.ModelAdmin,), {})
        #( VersionAdmin, ), {} )
        params.append(_dyn_class)
    admin.site.register(*params)
