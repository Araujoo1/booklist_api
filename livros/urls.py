from django.urls import path
from . import livro_views
from . import usuario_views

urlpatterns = [
    path('', usuario_views.bem_vindo, name='bem_vindo'),
    path('login/', usuario_views.login_usuario, name='login'),
    path('logout/', usuario_views.logout_usuario, name='logout'),
    path('cadastro_usuario/', usuario_views.cadastrar_usuario, name='cadastro_usuario'),
    path('home', livro_views.home, name='home'),
    path('cadastrar/', livro_views.cadastrar_livro, name='cadastrar'),
    path('livros/', livro_views.livros, name='livros'),
    path('detalhes/<int:livro_id>/', livro_views.detalhes_livro, name='detalhes'),
    path('editar/<int:livro_id>/', livro_views.editar_livro, name='editar'),
    path('excluir/<int:livro_id>/', livro_views.confirmar_exclusao, name='confirmar_exclusao'),
]