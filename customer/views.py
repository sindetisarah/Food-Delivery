from django.core.mail import send_mail
from customer.models import Category, MenuItem, OrderModel
from django.shortcuts import render
from django.views import View
# Create your views here.
class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/index.html')
class About(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/about.html')
"""
Building a view for the Actual Order Screen
"""
class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
            category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        """
        Declaring all the values in the Submition Order Form
        """
        name=request.POST.get('name')
        email=request.POST.get('email')
        city=request.POST.get('city')
        state=request.POST.get('state')
        zipCode=request.POST.get('zipCode')
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            city=city,
            state=state,
            zipCode=zipCode,


        )
        order.items.add(*item_ids)
        body=('Thank you for your Order,your Order is being processed,you will receive it in a short while \n'
        f'Your total is:{price}\n'
        'Thank you again for your Order')
        send_mail(
            'Thank you for Your Order!',
            body,
            'sindetisarah@gmail.com',
            [email],
            
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)
  