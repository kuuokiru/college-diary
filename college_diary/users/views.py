from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def user_list(request):
    users = User.objects.all().order_by('role', 'last_name')
    return render(request, 'users/list.html', {'users': users})
