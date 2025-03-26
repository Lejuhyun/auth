from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else: # 겟 요청일 때
        form = CustomUserCreationForm()
    
    context = {
        'form': form
    }

    return render(request, 'signup.html', context)

def login(request):
    pass