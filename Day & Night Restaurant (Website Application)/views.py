from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Appetizers_Model, Reservation_Model
from .models import Entree_Model
from .models import Drinks_Model
from .models import Dessert_Model
from .models import CheckoutScreen_Model
from .models import Order_History_Items_Model

from .forms import ReservationForm, Checkout_ScreenForm, CustomUserCreationForm




def homepage(request):
    homepage_content = {"homepage_message":
                            "Welcome to Day & Night. We are open 24 hours a day, 7 days a week."}

    return render(request,"homepage.html", homepage_content)

def about_page(request):

    return render(request, "about_page.html")


def Appetizers(request):
    appetizer_items = Appetizers_Model.objects.all()
    context = {
    "Appetizer_items": appetizer_items
    }
    return render(request, "appetizer.html", context)


def Appetizer_detail(request, item_id):
    appetizer_detail = get_object_or_404(Appetizers_Model, id= item_id)
    appetizer_dictionary = {"appetizer_index": appetizer_detail}
    return render(request, "appetizer_detail.html", appetizer_dictionary)


def entrees(request):
    entree_items = Entree_Model.objects.all()
    context = {
    "entrees": entree_items
    }
    return render(request, "entrees.html", context)

def entrees_detail(request, item_id):
    entree_item_detail = get_object_or_404(Entree_Model, id= item_id)
    entree_item_detail_dictionary = {"entree_index":entree_item_detail}
    return render(request, "entrees_detail.html", entree_item_detail_dictionary)


def desserts(request):
    dessert_items = Dessert_Model.objects.all()
    context = {
    "dessert_items": dessert_items
    }
    return render(request, "desserts.html", context)

def desserts_detail(request, item_id):
    dessert_detail = get_object_or_404(Dessert_Model, id= item_id)
    dessert_dictionary = {"dessert_index": dessert_detail}
    return render(request, "desserts_detail.html", dessert_dictionary)


def drinks(request):
    drink_items = Drinks_Model.objects.all()
    context = {
        "drinks": drink_items,
    }
    return render(request, "drinks.html", context)


def drink_detail(request, item_id):
    drink_item_detail = get_object_or_404(Drinks_Model, id= item_id)
    drink_item_detail_dictionary = {"drink_index": drink_item_detail}
    return render(request, "drink_detail.html", drink_item_detail_dictionary)

def reservation(request):
    reservation_form = ReservationForm()
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)

        if reservation_form.is_valid():
            reservation_form.save()
            return redirect("reservation_success")
        else:
            context = {"reservation_form": reservation_form}

            return render (request, "reservation.html", context)
    else:
        reservation_form = ReservationForm()
        context = {"reservation_form": reservation_form}
        return render(request, "reservation.html", context)

def reservation_success(request):
    success_page = {"success":"Thank you, your reservation has been created successfully! A text confirmation will be sent to the number provided. "
                              "Please return to the home page."}
    return render(request, "reservation_success.html", success_page)

def take_out(request):
    appetizer_items = Appetizers_Model.objects.all()
    entree_items = Entree_Model.objects.all()
    drink_items = Drinks_Model.objects.all()
    dessert_items = Dessert_Model.objects.all()

    cart_items, cart_total = mini_cart_view(request)
    context = {
        "appetizers": appetizer_items,
        "entrees": entree_items,
        "drink": drink_items,
        "desserts":dessert_items,
        "cart_items": cart_items,
        "cart_total": cart_total
    }
    return render(request, "take_out.html", context)


def add_to_cart(request, item_type, item_id):
    cart = request.session.get("cart", {})
    key = f"{item_type}_{item_id}"

    if key in cart:
        cart[key] +=1
    else:
        cart[key] = 1

    request.session["cart"] = cart

    cart_items = []
    total = 0

    for key, quantity in cart.items():
        type_, id_ = key.split("_")
        id_ = int(id_)
        if type_ == "entree":
            obj = Entree_Model.objects.get(id=id_)
            price = obj.entree_price
        elif type_ == "drink":
            obj = Drinks_Model.objects.get(id=id_)
            price = obj.drink_price
        elif type_ == "appetizer":
            obj = Appetizers_Model.objects.get(id=id_)
            price = obj.appetizer_price
        elif type_ == "dessert":
            obj = Dessert_Model.objects.get(id=id_)
            price = obj.dessert_price
        else:
            continue

        item_total = price*quantity
        total+= item_total

        cart_items.append({
            "item": obj,
            "quantity": quantity,
            "item_type": type_,
            "item_total": item_total

        })

    mini_cart_html = render_to_string("partials/_cart.html", {"cart_items": cart_items, "grand_total":total}, request=request)

    return JsonResponse({"success": True,
                         "cart_count": sum(cart.values()),
                         "mini_cart_html":mini_cart_html}
                        )

def cart_view(request):
    items, total = mini_cart_view(request)
    return render(request, "cart.html", {"items": items, "total": total})


def mini_cart_view(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for key, quantity in cart.items():
        item_type, item_id = key.split("_")
        item_id = int(item_id)

        if item_type == "entree":
            item = Entree_Model.objects.get(id=item_id)
            item_total = item.entree_price * quantity


        elif item_type =="drink":
            item = Drinks_Model.objects.get(id=item_id)
            item_total = item.drink_price * quantity

        elif item_type =="appetizer":
            item = Appetizers_Model.objects.get(id=item_id)
            item_total = item.appetizer_price * quantity

        elif item_type =="dessert":
            item = Dessert_Model.objects.get(id=item_id)
            item_total = item.dessert_price * quantity

        else:
            continue
        total += item_total

        items.append({
            "item_id": key,
            "item": item,
            "item_type": item_type,
            "quantity": quantity,
            "item_total": item_total


        })

    return items, total



@login_required
def reorder_function(request, order_id):

    previous_order = get_object_or_404(CheckoutScreen_Model, id=order_id, user=request.user)

    previous_items = Order_History_Items_Model.objects.filter(past_order=previous_order)


    cart = request.session.get('cart', {})


    for item in previous_items:

        key = f"{item.order_item_type}_{item.order_item_id}"

        if key in cart:
            cart[key] += item.order_item_quantity
        else:
            cart[key] = item.order_item_quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect("take_out")


def increase_cart_quantity_button(request, item_type, item_id):
    cart = request.session.get("cart", {})

    key = f"{item_type}_{item_id}"

    if key in cart:
        cart[key] += 1
    else:
        cart[key] = 1

    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER", "/"))



def decrease_cart_quantity_button(request, item_type, item_id):
    cart = request.session.get("cart", {})

    key = f"{item_type}_{item_id}"

    if key in cart:
        cart[key] -= 1
        if cart[key]<=0:
            del cart[key]

    else:
        cart[key] = 1

    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER", "/"))



def clear_cart(request):

    if "cart" in request.session:
        del request.session ["cart"]
    return redirect(request.META.get("HTTP_REFERER", "menu"))




def checkout_screen(request):
    items, total = mini_cart_view(request)

    if not items:
        return redirect("cart_view")

    form = Checkout_ScreenForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = CheckoutScreen_Model.objects.create(
            user=request.user if request.user.is_authenticated else None,
            Customer_Name = form.cleaned_data["Customer_Name"],
            Customer_Phone_Number=form.cleaned_data["Customer_Phone_Number"],
            Customer_Email=form.cleaned_data.get("Customer_Email"),

            Total_Price=total
        )

        for item in items:
            Order_History_Items_Model.objects.create(
                past_order = order,
                order_item_name=item["item"],
                order_item_type=item["item_type"],
                order_item_id=item["item"].id,
                order_item_price=item["item_total"]/item["quantity"],
                order_item_quantity=item["quantity"]

            )

        request.session["cart"] = {}
        request.session.modified = True
        return redirect("checkout_success", order_id=order.id)
    return render(request, "checkout_screen.html",{"form": form, "cart_items": items, "cart_total": total})


def checkout_success(request, order_id):

   order = CheckoutScreen_Model.objects.get(id=order_id)

   context = {
       "checkout_success":"Thank you, your take out order has been placed successfully. "
                            "We will notify you when your order is ready. ",
                                 "order_number":order.id
                }
   return render(request, "checkout_success.html", context)



def signup_page(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login") #login.html

    else:
        form = UserCreationForm()

    return render(request, "signup_page.html", {"form": form})


@login_required()
def order_history(request):

    previous_orders = CheckoutScreen_Model.objects.filter(user = request.user).order_by("-id")

    return render(request, "order_history.html", {"previous_orders":previous_orders})

def reservations_api(request):
    reservations = Reservation_Model.objects.all()

    data = []

    for reservation in reservations :
        data.append({
        "reservation_name":reservation.Reservation_Name,
        "date":reservation.Requested_Date,
        "reservation_time":reservation.Requested_Time,
        "reservation_phone_number": reservation.Phone_Number,
        "reservation_email": reservation.Email,
        "party_size":reservation.Party_Size,
        "special_requests": reservation.special_Requests

        })

    return JsonResponse(data, safe=False)