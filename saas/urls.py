from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import activate, CheckTokenView, UserViewSet
from employees.views import EmployeeViewSet
from management.views import ManagerViewSet
from owners.views import OwnerViewSet
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from rest_framework.authtoken.views import ObtainAuthToken

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
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/', ObtainAuthToken.as_view()),

]
