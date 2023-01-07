from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # bloquer l'acces par la barre des urls
from django.contrib.auth.forms import UserCreationForm #essentiel pour creer le formulaire de register
from django.contrib.auth import login #pour logger le user apres la creation du compte

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    #la method qui suit permet d'eviter les redirection dans l'urlbar lorsque le user est deja connecté
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    #cette methode permet de gerer les espaces membres
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user) #restrindre les taches en fonctions des utilisateurs
        context['count'] = context['tasks'].filter(complete = False).count()

        #recuperer la valeur dd'un champ dans la barre d'adresse url
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains = search_input)
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html' # pour definir precisement le template sur lequel on doit travailler ou s'executer

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'descrption', 'complete'] # pour importer les champs selon le modele defini dans models.py/media/black_hole/Works/To-Do-list_Django/todo_list/base/views.py
    success_url = reverse_lazy('tasks') # Redirige vers la liste des taches

    #cette methode permettra à l'utilisateur de créer des taches  uniquement lié à sa session ou son compte
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'descrption', 'complete'] # pour importer les champs selon le modele defini dans models.py /// il y'a une erreur sur description
    success_url = reverse_lazy('tasks') # Redirige vers la liste des taches

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')