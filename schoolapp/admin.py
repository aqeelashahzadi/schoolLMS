from django.contrib import admin
from .models import coursesdb
from .models import contact_db
from .models import payment_db
from .models import carts_db
from .models import subjectdb
from .models import comment_db
 # Register your models here.
admin.site.register(coursesdb)
admin.site.register(contact_db)
admin.site.register(payment_db)
admin.site.register(carts_db)
admin.site.register(subjectdb)
admin.site.register(comment_db)