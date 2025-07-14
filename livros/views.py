from django.shortcuts import render,redirect,get_object_or_404
from .models import Livro
from .forms import LivroForm
import requests

def home(request):
    return render(request, 'home.html')

def livros(request):
    livros = Livro.objects.all()
    total_livros = len(livros)
    return render(request, 'livros.html', {'livros': livros, 'total_livros': total_livros})

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
            form.save()
            return redirect('livros')
    else:
        form = LivroForm()

    return render (request, 'cadastrar_livro.html', {'form': form})

def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    return render(request, 'detalhes_livro.html', {'livro': livro})

def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)

    if request.method == 'POST':
        form = LivroForm(request.POST, instance = livro)
        if form.is_valid():
            form.save()
            return redirect('livros')
    else:
        form = LivroForm(instance = livro)
    return render(request, 'editar_livro.html', {'form': form, 'livro': livro})

def confirmar_exclusao(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if request.method == 'POST':
        livro.delete()
        return redirect('livros')