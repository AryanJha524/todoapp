from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import todoItem
from .forms import CreateItemForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


class ItemListCreateView(LoginRequiredMixin, CreateView, ListView):
    model = todoItem
    template_name = 'todolist/home.html'
    context_object_name = 'todo_items'
    fields = ['item_text', 'priority']
    paginate_by = 10

    def get_success_url(self):  # returns to homepage after creating a new post
        return reverse('todo-home', kwargs={})

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user.username)
        todoItem.objects.filter(
            author=user, completed=True).update(priority=0)  # reorders all completed tasks to priority 0
        return todoItem.objects.filter(author=user).order_by(
            '-priority', '-date_posted',)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def update_item(request, pk):
    current_item = todoItem.objects.get(id=pk, author=request.user)
    form = CreateItemForm(instance=current_item)

    if request.method == 'POST':
        # 2nd arg ensures it wont create a new item, but rather update it
        form = CreateItemForm(request.POST, instance=current_item)
        if form.is_valid():
            form.save()
            return redirect('todo-home')
        else:
            messages.success(
                request, f'Could not update!')
    context = {
        'form': form,
        'item': current_item
    }
    return render(request, 'todolist/edit_item.html', context)


@login_required
def delete_item(request, pk):
    current_item = todoItem.objects.get(id=pk, author=request.user)
    if request.method == 'POST':
        current_item.delete()
        return redirect('todo-home')

    context = {
        'item': current_item
    }
    return render(request, 'todolist/delete_item.html', context)
