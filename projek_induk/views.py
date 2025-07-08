from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.views import LogoutView, LoginView

class LogoutGetView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class CustomLoginView(LoginView):
    template_name = 'login.html'
    
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('manage_alumni')  # atau halaman mana pun
        else:
            return render(request, 'login.html', {'error': 'Username atau password salah'})
    return render(request, 'login.html')

def halaman_utama(request):
    return render(request, 'halaman_utama.html')
