from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
   path('',views.index, name='index'),
   path('register/', views.register, name='register'),
   path('otp/', views.otp, name='otp'),
   
   path('login/', views.login, name='login'),
   path('logout/', views.logout, name='logout'),
   
   path('contact/', views.contact, name='contact'),
   
   path('resetpassword/',views.resetpassword,name='resetpassword'),
   path('resetpassword_otp/',views.resetpassword_otp,name='resetpassword_otp'),
   path('confirmpassword/<str:username>/', views.confirmpassword, name='confirmpassword'),
   
   path('post/', views.post, name='post'),
   
   path('pendingpost/', views.pendingpost, name='pendingpost'),
   path('pendingpostdel/<int:id>/', views.pendingpostdel, name='pendingpostdel'),
   path('pendingpostapprove/<int:id>/', views.pendingpostapprove, name='pendingpostapprove'),
   
   path('delete/<int:id>/', views.delete, name='delete'),
   path('edit/<int:id>/', views.edit, name='edit'),
   
   
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

