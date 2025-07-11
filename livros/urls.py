from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar_livro, name='cadastrar'),
    path('livros/', views.livros, name='livros'),
    path('detalhes/<int:id>/', views.detalhes_livro, name='detalhes'),
    path('editar/<int:id>/', views.editar_livro, name='editar'),
]