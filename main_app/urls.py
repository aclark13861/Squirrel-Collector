from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('squirrels/', views.squirrels_index, name='index'),
  path('squirrels/<int:squirrel_id>/', views.squirrels_detail, name='detail'),
  path('squirrels/create/', views.SquirrelCreate.as_view(), name='squirrels_create'),
  path('squirrels/<int:pk>/update/', views.SquirrelUpdate.as_view(), name='squirrels_update'),
  path('squirrels/<int:pk>/delete/', views.SquirrelDelete.as_view(), name='squirrels_delete'),
  path('squirrels/<int:squirrel_id>/add_feeding/', views.add_feeding, name='add_feeding'),
  path('squirrels/<int:squirrel_id>/assoc_toy/<int:toy_id>/', views.assoc_toy, name='assoc_toy'),
  path('squirrels/<int:squirrel_id>/unassoc_toy/<int:toy_id>/', views.unassoc_toy, name='unassoc_toy'),
  path('toys/', views.ToyList.as_view(), name='toys_index'),
  path('toys/<int:pk>/', views.ToyDetail.as_view(), name='toys_detail'),
  path('toys/create/', views.ToyCreate.as_view(), name='toys_create'),
  path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toys_update'),
  path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toys_delete'),
  path('accounts/signup/', views.signup, name='signup'),
]