from django.urls import path
from . import views

from django.contrib.auth import views as auth_views



urlpatterns = [
   # home page
   path('', views.index, name='index'),

   # register
   path('register', views.register, name='register'),
   path('userlogin', views.userLogin, name='userLogin'),
   path('dashboard', views.dashboard, name='dashboard'),
   path('userlogout', views.userLogout, name='userLogout'),
   path('post-thought',views.postThought, name='postThought'),
   path('my-thoughts',views.myThoughts, name='myThoughts'),
   path('update-Thought/<str:pk>',views.updateThought, name='updateThought'),
   path('delete-Thought/<str:pk>',views.deleteThought, name='deleteThought'),
   path('manage-profile', views.manageProfile, name='manageProfile'),
   path('delete-account', views.deleteAccount, name='deleteAccount'),
   path('userProfile/<str:pk>', views.userProfile, name='userProfile'),


   #  password reset
   # allow to enter an email to receive a password link
   path('reset_password', auth_views.PasswordResetView.as_view(template_name='password-reset/password-reset.html'), name='reset_password'),

   # show a succss message that email was ssent
   path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='password-reset/password-reset-sent.html'), name='password_reset_done'),

   # send a link to email to change password
   path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password-reset/password-reset-form.html'), name='password_reset_confirm'),

   # show message that password has changed
   path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='password-reset/password-reset-complete.html'), name='password_reset_complete')
   
] 