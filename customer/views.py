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
        pass
   

        

