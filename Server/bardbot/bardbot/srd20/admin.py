from django.contrib import admin
from bardbot.srd20.models import Spell, Feat, Ability, CharacterClass, Monster, MonsterAbility, Race, Skill

class SpellAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'short_description')
    list_filter = ('school',)
    search_fields = ('name',)
    prepopulated_fields = {'altname': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('name', 'altname', ('school', 'subschool'), 'descriptor', 'level', 'reference')
        }),
        ('Properties', {
            'fields': ('components', 'range', ('target', 'area', 'effect'), 'duration', 'saving_throw', 'spell_resistance')
        }),
        ('Epic requirements', {
            'fields': ('spellcraft_dc', 'to_develop'),
            'classes': ("collapse",)
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'verbal_components',
            'material_components', 'arcane_material_components', 'focus',
            'arcane_focus', 'cleric_focus', 'druid_focus','xp_cost')
        }),
    )
admin.site.register(Spell, SpellAdmin)


class FeatAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)
    prepopulated_fields = {'altname': ('name',)}

    fieldsets = (
        (None, {
            'fields': ('name', 'altname', 'type', ('multiple', 'stack'), 'prerequisite', 'choice')
        }),
        ('Description', {
            'fields': ('benefit', 'normal', 'special')
        }),
        ('Source', {
            'fields': ('reference',),
        }),
    )
admin.site.register(Feat, FeatAdmin)


class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference',)
    list_filter = ('reference',)
admin.site.register(CharacterClass, CharacterClassAdmin)


class MonsterAbilityInline(admin.TabularInline):
    model = MonsterAbility

class MonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'alignment', 'size', 'type', 'environment', 'cr')
    list_filter = ('cr', 'type', 'size', 'alignment', 'reference')
    search_fields = ('name',)
    inlines = [MonsterAbilityInline]
admin.site.register(Monster, MonsterAdmin)


class AbilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbr',)
    list_filter = ('name', 'abbr',)
admin.site.register(Ability, AbilityAdmin)


class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'speed',)
    list_filter = ('size',)
admin.site.register(Race, RaceAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'ability', 'untrained', 'ac_penalty',)
    list_filter = ('ability',)
admin.site.register(Skill, SkillAdmin)

