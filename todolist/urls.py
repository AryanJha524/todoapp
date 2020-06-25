from . import views
from django.urls import path
from .views import ItemListCreateView

urlpatterns = [
    path('', ItemListCreateView.as_view(), name='todo-home'),
    path('<int:pk>/update/', views.update_item, name='todo-update'),
    path('<int:pk>/delete/', views.delete_item, name='todo-delete'),
]
