from django.shortcuts import render, redirect
from django.core import serializers
from .models import CountryData
from .forms import CountryDataForm


def index(request):
    form = CountryDataForm(request.POST or None)
    
    if form.is_valid():
        data = form.save()
        return redirect('dashboard:index')
    
    countries = CountryData.objects.all()
    context = {
        'form': form,
        'countries': countries,
        'datas': serializers.serialize(format='json', queryset=countries)
    }
    return render(request, 'index.html', context)