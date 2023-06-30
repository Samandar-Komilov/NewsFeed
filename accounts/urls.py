from django.urls import path
from .views import edit_user, user_login, dashboard_view, user_register, EditUserView
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView)

urlpatterns = [
    # path('login/',user_login, name='login'),   | We did everything on hand, but we can use ready tools here...
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),   # In order to use ready Login/LogoutView, we have to change template folder to registration/login.html
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/',PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/',PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Sign Up
    path('signup/', user_register, name='user_register'),
    # path('profile/edit/', edit_user, name='edit_user'),
    path('profile/edit/', EditUserView.as_view(), name='edit_user'),

    # Profile
    path('profile/', dashboard_view, name='user_profile'),
]
