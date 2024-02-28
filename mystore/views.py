from django.shortcuts import render,redirect
from django.views.generic import View,DetailView,TemplateView
from mystore.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from mystore.models import Product,BasketItem,Size



# Create your views here.
class SignupView(View):


    def get(self,request,*args,**kwargs):
        form=RegistrationForm
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
          return render(request,"login.html",{"form":form})


class SignInView(View):


    def get(self,request,*args,**kwargs):
     form=LoginForm()
     return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
       form=LoginForm(request.POST)
       if form.is_valid():
          u_name=form.cleaned_data.get("username")
          pwd=form.cleaned_data.get("password")
          user_object=authenticate(request,username=u_name,password=pwd)
          if user_object:
            login(request,user_object)
            return redirect("index")
          
       messages.error(request,"invalid credentials")
       return render(request,"login.html",{"form":form})



class IndexView(View):
   

   def get(self,request,*args,**kwargs):
    qs=Product.objects.all()
    return render(request,"index.html",{"data":qs})
   
        

class ProductDetailView(View):
   

   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      qs=Product.objects.get(id=id)
      return render(request,"product_detail.html",{"data":qs})

   

#    template_name="product_detail.html"
#    model=Product
#    context_object_name="data"

class HomeView(TemplateView):
   template_name="base.html"


#add to basket
#url:localhost:8000/product/{id}/ad_to_cart
#method:post

class AddToBasketView(View):
   
   def post(self,request,*args,**kwargs):
      size=request.POST.get("size")
      size_obj=Size.objects.get(name=size)
      qty=request.POST.get("qty")
      id=kwargs.get("pk")
      product_obj=Product.objects.get(id=id)
      BasketItem.objects.create(
         size_object=size_obj,
         qty=qty,
         product_object=product_obj,
         basket_object=request.user.cart
      )
      return redirect("index")

# basket item list view
# localhost:8000/basket/items/all
#method:get
   
class BasketItemListView(View):
   
   def get(self,request,*args,**kwargs):
      qs=request.user.cart.cartitem.filter(is_order_placed=False)
      return render(request,"cart_list.html",{"data":qs})
      
      

















class SignOutView(View):


    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    


