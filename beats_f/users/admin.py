from django.contrib import admin
from .models import Userinfo
from .models import ChatBot
from .models import EcoFootprintCategory
from .models import EcoFootprintQuestion
from .models import AIResult


admin.site.register(Userinfo)
admin.site.register(ChatBot)
admin.site.register(EcoFootprintCategory)
admin.site.register(EcoFootprintQuestion)
admin.site.register(AIResult)