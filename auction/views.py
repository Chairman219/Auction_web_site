from django.shortcuts import render

def hlavni_stranka(request):
    return render(request, 'hlavni_stranka.html')