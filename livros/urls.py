from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar/', views.cadastrar_livro, name='cadastrar'),
    path('livros/', views.livros, name='livros'),
    path('detalhes/<int:livro_id>/', views.detalhes_livro, name='detalhes'),
    path('editar/<int:livro_id>/', views.editar_livro, name='editar'),
    path('excluir/<int:livro_id>/', views.confirmar_exclusao, name='confirmar_exclusao'),
]