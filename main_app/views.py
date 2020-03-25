from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Squirrel, Toy
from .forms import FeedingForm

# Create your views here.

class SquirrelCreate(CreateView):
    model = Squirrel
    fields = '__all__'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def squirrels_index(request):
    squirrels = Squirrel.objects.all()
    return render(request, 'squirrels/index.html', {'squirrels': squirrels})

def squirrels_detail(request, squirrel_id):
    squirrel = Squirrel.objects.get(id=squirrel_id)
    toys_squirrel_doesnt_have = Toy.objects.exclude(id__in = squirrel.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'squirrels/detail.html', {
        'squirrel': squirrel, 'feeding_form': feeding_form,
        'toys' : toys_squirrel_doesnt_have
     })

class SquirrelUpdate(UpdateView):
    model = Squirrel
    fields = ['breed', 'description', 'age']

class SquirrelDelete(DeleteView):
    model = Squirrel
    succes_url = '/squirrels/'

def add_feeding(request, squirrel_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.squirrel_id = squirrel_id
    new_feeding.save()
  return redirect('detail', squirrel_id=squirrel_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def assoc_toy(request, squirrel_id, toy_id):
  Squirrel.objects.get(id=squirrel_id).toys.add(toy_id)
  return redirect('detail', squirrel_id=squirrel_id)