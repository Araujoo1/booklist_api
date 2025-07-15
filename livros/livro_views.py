from django.shortcuts import render,redirect,get_object_or_404
from .models import Livro
from .forms import LivroForm
from django.db.models import Q
import requests, unicodedata
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'livros/home.html')

def remove_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

@login_required
def livros(request):
    status = request.GET.get('status')
    busca = request.GET.get('busca')
    livros = Livro.objects.filter(usuario=request.user)
    
    if status == 'lido':
        livros = livros.filter(lido=True)
    if status == 'nao_lido':
        livros = livros.filter(lido=False)

    if busca:
        busca_normalizada = remove_acentos(busca).lower()
        livros = [
            livro for livro in livros
            if busca_normalizada in remove_acentos(livro.titulo).lower()
            or busca_normalizada in remove_acentos(livro.autor).lower()
        ]
    total_livros = len(livros)
    return render(request, 'livros/livros.html', {'livros': livros, 'total_livros': total_livros})

@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            livro = form.save(commit=False)

            # Buscar dados na API do Google Books com base no título
            titulo = livro.titulo
            url = f'https://www.googleapis.com/books/v1/volumes?q={titulo}'
            resposta = requests.get(url)

            if resposta.status_code == 200:
                dados = resposta.json()
                if 'items' in dados and len(dados['items']) > 0:
                    volume = dados['items'][0]['volumeInfo']
                    livro.descricao = volume.get('description', '')
                    livro.capa_url = volume.get('imageLinks', {}).get('thumbnail', '')
            livro.usuario = request.user
            livro.save()
            return redirect('livros')
    else:
        form = LivroForm()

    return render (request, 'livros/cadastrar_livro.html', {'form': form})

@login_required
def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    return render(request, 'livros/detalhes_livro.html', {'livro': livro})

@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance = livro)
        if form.is_valid():
            form.save()
            return redirect('livros')
    else:
        form = LivroForm(instance = livro)
    return render(request, 'livros/editar_livro.html', {'form': form, 'livro': livro})

@login_required
def confirmar_exclusao(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if request.method == 'POST':
        livro.delete()
        return redirect('livros')