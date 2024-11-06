from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import activate, CheckTokenView, UserViewSet
from employees.views import EmployeeViewSet
from management.views import ManagerViewSet
from owners.views import OwnerViewSet
from items.views import AppetizerViewSet,BurgerViewSet,DesertViewSet,EntreeViewSet,ItemViewSet,MainCourseViewSet,SandwichViewSet,SideViewSet,SpecialViewSet
from orders.views import OrderViewSet
from menu.views import BeerViewSet,CocktailViewSet,DrinkViewSet,ShotViewSet
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetCompleteView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('employees', EmployeeViewSet, basename='employee')
router.register('managers', ManagerViewSet, basename='manager')
router.register('owners', OwnerViewSet, basename='owner')
router.register('items', ItemViewSet, basename='item')
router.register('orders', OrderViewSet, basename='order')

foodrouter = DefaultRouter()
foodrouter.register('appetizers', AppetizerViewSet, basename='appetizer')
foodrouter.register('burgers', BurgerViewSet, basename='burger')
foodrouter.register('deserts', DesertViewSet, basename='desert')
foodrouter.register('entrees', EntreeViewSet, basename='entree')
foodrouter.register('main_courses', MainCourseViewSet, basename='main_course')
foodrouter.register('sandwiches', SandwichViewSet, basename='sandwich')
foodrouter.register('sides', SideViewSet, basename='side')
foodrouter.register('specials', SpecialViewSet, basename='special')

drinkrouter = DefaultRouter()
drinkrouter.register('beers', BeerViewSet, basename='beer')
drinkrouter.register('cocktails', CocktailViewSet, basename='cocktail')
drinkrouter.register('drinks', DrinkViewSet, basename='drink')
drinkrouter.register('shots', ShotViewSet, basename='shot')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('token/check', CheckTokenView.as_view(), name='check_token'),
    path('activate/<str:username>/<str:token>', activate, name='activate'),
    path('menu/', include(foodrouter.urls)),
    path('drinks/', include(drinkrouter.urls)),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password_change/', PasswordChangeView.as_view()),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset/done/', PasswordResetDoneView.as_view()),
    path('password_comfirm', PasswordResetConfirmView.as_view(),)
    
]
