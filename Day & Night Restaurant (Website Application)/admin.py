from django.contrib import admin
from .models import Entree_Model
from .models import Drinks_Model
from .models import Reservation_Model
from .models import CheckoutScreen_Model
from .models import  Appetizers_Model
from .models import Dessert_Model
from .models import Order_History_Items_Model



# Register your models here.

admin.site.register(Appetizers_Model)
admin.site.register(Entree_Model)
admin.site.register(Drinks_Model)
admin.site.register(Dessert_Model)
admin.site.register(Reservation_Model)
admin.site.register(CheckoutScreen_Model)
admin.site.register(Order_History_Items_Model)
