from django.urls import path
from shop import views
urlpatterns = [
    path('',views.home_view.as_view(),name='home'),
    path('aboutus/',views.AboutUs.as_view(),name='aboutpage'),
    path('allproducts/',views.AllProduct_view.as_view(),name='product'),
    path('detail/<slug:slug>',views.Detail_view.as_view(),name='details'),
    path('cart/<int:product_id>/',views.AddCart_view.as_view(),name='add_cart'),
    path('mycart/',views.mycart_view.as_view(),name='mycart'),
    path('mymanagecart/<int:cp_id>/',views.CartManager_View.as_view(),name='managecart'),
    path('empty-cart/',views.EmptyCart.as_view(),name='emptycart'),
    path('checkout/',views.Checkout.as_view(),name='checkcart'),
    path('payment/',views.PaymentGateWay.as_view(),name='payments'),
    path('paymentverify_serverside/',views.PaymentGateWayerverside.as_view(),name='paymentside'),



    # user login related details of urls
    path('register/',views.Customer_Register_View.as_view(),name='register'),
    path('log_out/',views.logout_view.as_view(),name='logout'),
    path('log_in/',views.Login_View.as_view(),name='login'),



    ## pwd details
    path('forgetpwd/',views.ForgetPwd.as_view(),name='pwdrst'),
    path('password-reset/<email>/<token>/',views.RestPwd_view.as_view(),name='pwdreset'),


    # profile urls
    path('profile/',views.Profile_View.as_view(),name='profile'),
    path('profile/order-<int:pk>/',views.ProfileOrderDetail_View.as_view(),name='orderdetails'),

    path('search/',views.searchview.as_view(),name='searchbox'),

    # this urls related to admin page
    path('adminlist/details/',views.ADMINLISTVIEW.as_view(),name='adlistpr'),
    path('adminaddproducts/',views.AdmibAddProduct.as_view(),name='adproducts'),
    path('admin_login/',views.adminView.as_view(),name='adminlog'),
    path('admin-home/',views.Admin_Home_View.as_view(),name='adminhome'),
    path('admin-orderdetails/<int:pk>',views.Adminorderdetails_view.as_view(),name='adminordedtail'),
    path('admin-alldtls/', views.Admin_allorder_View.as_view(), name='allorders'),
    path('admin-order/<int:pk>-change/',views.Admin_status_view.as_view(),name='orderstatus'),
]