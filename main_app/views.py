from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Squirrel, Toy
from .forms import FeedingForm
import uuid
import boto3

# Create your views here.

class SquirrelCreate(LoginRequiredMixin, CreateView):
    model = Squirrel
    fields = ['name','breed', 'description', 'age']

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)
    
class SquirrelUpdate(LoginRequiredMixin, UpdateView):
    model = Squirrel
    fields = ['breed', 'description', 'age']

class SquirrelDelete(LoginRequiredMixin, DeleteView):
    model = Squirrel
    success_url = '/squirrels/'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def squirrels_index(request):
    squirrels = Squirrel.objects.filter(user=request.user)
    return render(request, 'squirrels/index.html', {'squirrels': squirrels})

@login_required
def squirrels_detail(request, squirrel_id):
  squirrel = Squirrel.objects.get(id=squirrel_id)
  toys_squirrel_doesnt_have = Toy.objects.exclude(id__in = squirrel.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'squirrels/detail.html', {
      'squirrel': squirrel, 'feeding_form': feeding_form,
      'toys' : toys_squirrel_doesnt_have
    })

def add_feeding(request, squirrel_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.squirrel_id = squirrel_id
    new_feeding.save()
  return redirect('detail', squirrel_id=squirrel_id)

@login_required
def assoc_toy(request, squirrel_id, toy_id):
  Squirrel.objects.get(id=squirrel_id).toys.add(toy_id)
  return redirect('detail', squirrel_id=squirrel_id)

@login_required
def unassoc_toy(request, squirrel_id, toy_id):
  Squirrel.objects.get(id=squirrel_id).toys.remove(toy_id)
  return redirect('detail', squirrel_id=squirrel_id)


class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
