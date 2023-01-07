# Dans cette partie nous appelons toutes les class qui devrons
# communiquer avec les differrents template html
from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'), # "TaskDetail.as_view()" cette fonction cherchera dans le dossier template/base/ le fichier sous le nom "task_detail" si un fichier de retour html n'est pas precisé dans la classe correspondante contenu dans le fichier views.py ///# Cette expression "/<int:pk>/" permet d'obtenir l'ID des element d'un tableau dans la barre d'url'
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
]