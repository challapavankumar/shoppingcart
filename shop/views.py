from django.shortcuts import render,redirect
from .models import *

from .forms import PasswordForgeForm,AdminAddProductForm, Password_Reset_Form, AdminLoginForm,ChcekOutForm,CustomerRegisterForm,CustomerLoginForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth import logout,login,authenticate
from django.views.generic import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .utils import password_reset_token
from django.core import mail
from django.conf import settings
# Create your views here.
class AboutUs(TemplateView):
    template_name = 'ecom/aboutus.html'


class EcomerceMixin_view(object):
    def dispatch(self,request, *args,**kwargs):
        cart_id=request.session.get('cart_id')
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and  Customer.objects.filter(user=request.user).exists():
                cart_obj.customer=request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args,**kwargs)
class home_view(EcomerceMixin_view,TemplateView):
    template_name = 'ecom/product.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        product=Product.objects.all().order_by('-id')
        paginator = Paginator(product,10)
        page_number =self.request.GET.get('page')
        product_page = paginator.get_page(page_number)
        context['product_list']=product_page

        # context['category']=Category.objects.all()
        return context

class AllProduct_view(EcomerceMixin_view,TemplateView):
    template_name = 'ecom/categories.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['allcategories']=Category.objects.all().order_by('-id')
        return context


class Detail_view(EcomerceMixin_view,TemplateView):
    template_name = 'ecom/details.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        slug_url=self.kwargs['slug']
        product=Product.objects.get(slug=slug_url)
        product.view_count +=1
        product.save()

        context['Product']=product
        return context
class AddCart_view(EcomerceMixin_view,TemplateView):
    template_name = 'ecom/cart.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        #get product id from requested url
        product_id=self.kwargs['product_id']
        product_obj=Product.objects.get(id=product_id)
        #check if cart exists
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            this_product_in_cart=cart_obj.cartproduct_set.filter(product=product_obj)
            # item alredy exists
            if this_product_in_cart.exists():
                cartproduct=this_product_in_cart.last()
                cartproduct.quantity +=1
                cartproduct.subtotal +=product_obj.selling_price
                cartproduct.save()
                cart_obj.total +=product_obj.selling_price
                cart_obj.save()
              # item added in cart
            else:
                cartproduct=CartProduct.objects.create(cart=cart_obj,product=product_obj,rate=product_obj.selling_price,quantity=1,subtotal=product_obj.selling_price)
                cart_obj.total +=product_obj.selling_price
                cart_obj.save()

        else:
            cart_obj=Cart.objects.create(total=0)
            self.request.session['cart_id']=cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj,product=product_obj,
                        rate=product_obj.selling_price,quantity=1,
                        subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()

        return context


class CartManager_View(EcomerceMixin_view,View):
    def get(self,request,*args,**kwargs):
        cp_id=self.kwargs['cp_id']
        action=request.GET.get('action')
        cp_obj=CartProduct.objects.get(id=cp_id)
        cart1=cp_obj.cart


        if action == 'inc':
            cp_obj.quantity +=1
            cp_obj.subtotal +=cp_obj.rate
            cp_obj.save()
            cart1.total +=cp_obj.rate
            cart1.save()

        elif action == 'dcr':
            cp_obj.quantity -=1
            cp_obj.subtotal -=cp_obj.rate
            cp_obj.save()
            cart1.total -=cp_obj.rate
            cart1.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()


        elif action == 'rmv':

            cart1.total -= cp_obj.subtotal
            cart1.save()
            cp_obj.delete()
        else:
            pass

        return redirect('/mycart/')
class mycart_view(EcomerceMixin_view,TemplateView):
     template_name = 'ecom/mycart.html'
     def get_context_data(self, **kwargs):
         context=super().get_context_data(**kwargs)
         cart_id=self.request.session.get('cart_id',None)
         if cart_id:
             cart=Cart.objects.get(id=cart_id)
         else:
             cart=None
         context['cart']=cart
         return context
class   EmptyCart(View):
    def get(self,request,*args,**kwargs):
        cart_id=request.session.get('cart_id',None)
        if cart_id:
            cart=Cart.objects.get(id=cart_id)

            cart.cartproduct_set.all().delete()
            cart.total=0
            cart.save()
        return redirect('mycart')
class Checkout(EcomerceMixin_view,CreateView):

    template_name = 'ecom/checkout.html'
    form_class = ChcekOutForm
    success_url =reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.customer:
            print('logged in user')
            pass
        else:
            return redirect('/log_in/?next=/checkout/')

            print('not logged in user')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cart_id=self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
        else:
            cart_obj=None
        context['cart']=cart_obj
        return context
    def form_valid(self,form):
        cart_id=self.request.session.get('cart_id')
        if cart_id:
            cart_obj=Cart.objects.get(id=cart_id)
            form.instance.cart=cart_obj
            form.instance.subtotal=cart_obj.total
            form.instance.discount=0
            form.instance.total=cart_obj.total
            form.instance.order_status='Order Received'
            del self.request.session['cart_id']
            pm=form.cleaned_data.get('payment_method')
            order = form.save()
            if pm == 'khalti':
                return redirect(reverse('payments')+"?o_id="+str(order.id))

        else:
            return redirect('home')

        return super().form_valid(form)
class PaymentGateWay(View):
    def get(self,request,*args, **kwargs):
        o_id=request.GET.get('o_id')
        order=Order.objects.get(id=o_id)
        context={'ord':order}
        return render(request,'ecom/payment.html',context)

class PaymentGateWayerverside(View):
    def get(self,request,*args,**kwargs):
        token=request.GET.get('token')
        amount=request.GET.get("amount")
        o_id=request.GET.get("order_id")
        print(token,amount,o_id)
        data={"success":True}
        return JsonResponse(data)


class Customer_Register_View(EcomerceMixin_view,CreateView):
    template_name = 'ecom/register.html'
    form_class =CustomerRegisterForm
    success_url = reverse_lazy('home')
    def form_valid(self,form):
        username=form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user=User.objects.create_user(username,email,password)
        form.instance.user=user
        login(self.request,user)
        return super().form_valid(form)
class searchview(TemplateView):
    template_name = 'ecom/search.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        kw=self.request.GET['keyword']
        results=Product.objects.filter(Q(title__icontains=kw)|Q(description__icontains=kw))
        context['results']=results
        return context
class logout_view(EcomerceMixin_view,View):
    def get(self,request):
        logout(request)
        return redirect('home')
class Login_View(EcomerceMixin_view,FormView):
    template_name = 'ecom/login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('home')
    def form_valid(self,form):
        uname=form.cleaned_data.get("username")
        pwd=form.cleaned_data["password"]
        usr=authenticate(username=uname, password=pwd)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request,usr)
        else:
            return render(self.request, self.template_name, {'form':self.form_class,'error':'invalid credentials'})

        return super().form_valid(form)
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url=self.request.GET.get('next')
            return redirect(next_url)
        else:
            return self.success_url
class Profile_View(TemplateView):
    template_name = 'ecom/profile.html'
    def dispatch(self,request, *args,**kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/log_in/?next=/profile/')
        return super().dispatch(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        customer=self.request.user.customer
        context['customer']=customer
        orders=Order.objects.filter(cart__customer=customer).order_by('-id')
        context['orders']=orders
        return  context

class ProfileOrderDetail_View(DetailView):
    template_name = 'ecom/orderdetails.html'
    model=Order
    context_object_name='ord_obj'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
           order_id=self.kwargs['pk']
           order=Order.objects.get(id=order_id)
           if request.user.customer != order.cart.customer:
               return redirect('profile')


        else:
            return redirect('/log_in/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)
class ForgetPwd(FormView):
    template_name = 'ecom/pwdrst.html'
    form_class =PasswordForgeForm
    success_url ='/forgetpwd/?m=s'

    def form_valid(self, form):
        # get mail from user
        email=form.cleaned_data.get('email')
        # get current host ip/domain
        url=self.request.META['HTTP_HOST']
        #get customer and user
        customer=Customer.objects.get(user__email=email)

        user=customer.user
        # send mail to the user with email
        text_content='Please Click the link below to reset your password .'
        html_content= url + '/password-reset/' + email +\
                     '/' + password_reset_token.make_token(user)+ '/'
        mail.send_mail('Password Reset link | ecommerce',
                    text_content + html_content,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
        )
        return super().form_valid(form)

class RestPwd_view(FormView):
    template_name = 'ecom/restpwd.html'
    form_class = Password_Reset_Form
    success_url = '/log_in/'

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse('pwdrst') + "?m=e")
        return super().dispatch(request,*args,**kwargs)

    def form_valid(self, form):

            password=form.cleaned_data['new_password']
            email = self.kwargs.get('email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return super().form_valid(form)

##admin login view details

class adminView(FormView):
    template_name = 'ecom/adminlogin.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy('adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pwd = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pwd)
        if usr is not None and AdminUser.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'invalid credentials'})

        return super().form_valid(form)
class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and AdminUser.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/admin_login/')
        return super().dispatch(request,*args,**kwargs)

class Admin_Home_View(AdminMixin,TemplateView):
    template_name = 'ecom/adminhome.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['pendingorders']=Order.objects.filter(order_status='Order Received').order_by('-id')
        return context


class Adminorderdetails_view(AdminMixin,DetailView):
    template_name = 'ecom/adminordetail.html'
    model = Order
    context_object_name = 'ord_obj'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['allstatus']=Order_Status
        return context

class Admin_allorder_View(AdminMixin,ListView):
    template_name = 'ecom/adordlist.html'
    queryset = Order.objects.all().order_by('-id')
    context_object_name = 'allord'


class Admin_status_view(AdminMixin,View):
    def post(self,request, *args, **kwargs):
        order_id=self.kwargs['pk']
        order_obj=Order.objects.get(id=order_id)
        new_status=request.POST.get("status")
        order_obj.order_status=new_status
        order_obj.save()
        return redirect(reverse_lazy('adminordedtail', kwargs={'pk':order_id}))

class ADMINLISTVIEW(AdminMixin,ListView):
    template_name = 'ecom/adminlist.html'
    queryset = Product.objects.all().order_by('-id')
    context_object_name = 'productsall'

class AdmibAddProduct(AdminMixin,CreateView):
    template_name = 'ecom/adminadprd.html'
    form_class =AdminAddProductForm
    success_url = reverse_lazy('adproducts')
    def form_valid(self, form):
        productimg = form.save()
        mrimges=self.request.FILES.getlist('more_images')
        for i in mrimges:
            ProductImage.objects.create(product=productimg,image=i)

        return super().form_valid(form)