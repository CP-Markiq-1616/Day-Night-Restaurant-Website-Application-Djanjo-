from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Class names are written in Name_Model format for my understanding.



class Appetizers_Model(models.Model):
    appetizer_name = models.CharField (max_length= 200)
    appetizer_description = models.TextField(blank=True, null=True, max_length=200)
    appetizer_price = models.DecimalField(max_digits=6, decimal_places=2)
    appetizer_image = models.ImageField(upload_to="menu_images/")

    def __str__(self):
        return self.appetizer_name

    class Meta:
        db_table = 'restaurant_02_appetizers_model'



class Entree_Model(models.Model):
   entree_name = models.CharField (max_length= 200)
   entree_description = models.TextField(blank = True, null = True, max_length= 200)
   entree_price = models.DecimalField (max_digits= 6, decimal_places= 2)
   entree_image = models.ImageField(upload_to="menu_images/")

   def __str__(self):
      return self.entree_name

   class Meta:
       db_table = 'restaurant_02_entree_model'



class Dessert_Model(models.Model):
    dessert_name = models.CharField(max_length=200)
    dessert_description = models.TextField(max_length=200)
    dessert_price = models.DecimalField(max_digits= 6, decimal_places= 2)
    dessert_image = models.ImageField(upload_to="menu_images/")

    def __str__(self):
        return self.dessert_name

    class Meta:
        db_table = 'restaurant_02_dessert_model'

class Drinks_Model(models.Model):
    drink_name= models.CharField(max_length=200)
    drink_description = models.TextField(blank = True, null = True, max_length=200)
    drink_price = models.DecimalField(max_digits=6, decimal_places=2)
    drink_image = models.ImageField(upload_to="menu_images/")

    def __str__(self):
        return self.drink_name

    class Meta:
        db_table = 'restaurant_02_drinks_model'

class Reservation_Model(models.Model):
    Reservation_Name = models.CharField (max_length=200)
    Requested_Date = models.DateField()
    Requested_Time = models.TimeField()
    Phone_Number = models.CharField(max_length=20)
    Email = models.EmailField(null=True, blank=True)
    Party_Size = models.PositiveIntegerField (validators=[MinValueValidator(1), MaxValueValidator(50)], help_text= "Please enter number of guests between 1 and 50")
    special_Requests = models.TextField(null = True, blank = True,max_length=200)

    def __str__(self):
        return self.Reservation_Name

    class Meta:
        db_table = 'restaurant_02_reservation_model'




class CheckoutScreen_Model(models.Model): # AKA Orders_Model
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Customer_Name = models.CharField (max_length= 100)
    Customer_Phone_Number = models.CharField(max_length= 20)
    Customer_Email = models.EmailField (max_length= 100)
    Created_at = models.DateTimeField(auto_now_add=True)
    Total_Price = models.DecimalField(max_digits= 8, decimal_places=2)
    Completed = models.BooleanField(default=False)
    # customer_phone_number_model = PhoneNumberField()

    def __str__(self):
        return f"Order # {self.id} Created By User ID: {self.user}"

    class Meta:
        db_table = 'restaurant_02_checkoutscreen_model'



class Order_History_Items_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    past_order = models.ForeignKey(CheckoutScreen_Model, on_delete=models.CASCADE, related_name="items")
    order_item_type = models.CharField(max_length=20)
    order_item_id = models.IntegerField(default=0)
    order_item_name = models.CharField(max_length=200)
    order_item_price = models.DecimalField(max_digits=6, decimal_places=2)
    order_item_quantity = models.IntegerField(default = 1)

    def __str__(self):
        if self.past_order.user:
            username = self.past_order.user.username
        else:
            username = self.past_order.Customer_Name or "Guest"

        return f"Order #{self.past_order.id} - {self.order_item_quantity}x {self.order_item_name} from {username}"

    class Meta:
        db_table = 'restaurant_02_order_history_items_model'