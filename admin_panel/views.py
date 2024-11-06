from django.shortcuts import render
from employees.models import Employee
from items.models import Appetizer,Burger,Desert,Entree,Item,MainCourse,Order,Sandwich,Side,Special,condiments,toppings
from management.models import Manager
from menu.models import Beer,Cocktail,Drink,Shot
from tables.models import Table
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

