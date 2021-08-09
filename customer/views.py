from django.core.mail import send_mail
from django.http.response import JsonResponse
from customer.models import Category, MenuItem, OrderModel
from django.shortcuts import redirect,render
from django.views import View
import json
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
        zip_code = request.POST.get('zip')
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
            zip_code=zip_code


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
        return redirect('order_confirmation',pk=order.pk)
"""
Adding a Confirmation view and redirect it as a Post request to a Url
"""
class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/order_pay_confirmation.html')





  