from django.contrib import admin

from . models import Assignment, Chore, Person, Week


admin.site.register(Chore)
admin.site.register(Person)
admin.site.register(Week)
admin.site.register(Assignment)
