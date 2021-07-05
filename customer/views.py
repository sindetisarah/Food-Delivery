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
    def get(self,request,*args,**kwargs):
        appetizers=MenuItem.objects.filter(category_name_contains='Appetizers')
        entres=MenuItem.objects.filter(category_name_contains='Dessert')
        desserts=MenuItem.objects.filter(category_name_contains='Entre')
        drinks=MenuItem.objects.filter(category_name_contains='Drink')

        context={
            'appetizers':appetizers,
            'desserts':desserts,
            'entres':entres,
            'drinks':drinks


        }

        return render(request,'customer/order.html', context)
    def post(self, request, *args, **kwargs):
        order_items={
            'items':[]
        }
        items=request.POST.getlist('items[]')

        for item in items:
            menu_item=MenuItem.objects.get(pk_contains=int(item))
            Item_data={
                'id':menu_item.pk,
                'name':menu_item.name,
                'price':menu_item.price
            }
            order_items['items'].append(Item_data)

            price = 0
            item_ids =[]
            for item in order_items['items']:
                price+=item['id']
            
            order=OrderModel.objects.create(price=price)
            order.items.add(item_ids)

            context={
                'Item':order_items['items'],
                'price':price

            }
            return render(request, 'customeer/order_confirmation.html,',context)


        

