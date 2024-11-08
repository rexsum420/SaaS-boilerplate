from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import activate, CheckTokenView, UserViewSet
from employees.views import EmployeeViewSet
from management.views import ManagerViewSet
from owners.views import OwnerViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('employees', EmployeeViewSet, basename='employee')
router.register('managers', ManagerViewSet, basename='manager')
router.register('owners', OwnerViewSet, basename='owner')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('token/check', CheckTokenView.as_view(), name='check_token'),
    path('activate/<str:username>/<str:token>', activate, name='activate'),
    path('token/', ObtainAuthToken.as_view()),
    path('accounts/register/', views.register_view, name="register"),
    path('accounts/login/', views.UserLoginView.as_view(), name="login"),
    path('accounts/logout/', views.logout_view, name="logout"),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password-change-done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    path('accounts/password-reset-confirm/<uidb64>/<token>/',
        views.UserPasswrodResetConfirmView.as_view(), name="password_reset_confirm"
    ),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password-reset-done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password-reset-complete.html'
  ), name='password_reset_complete'),
    path('', views.index, name="index"),
]
