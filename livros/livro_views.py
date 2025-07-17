from django.shortcuts import render,redirect,get_object_or_404
from .models import Livro
from .forms import LivroForm
from django.db.models import Q
import requests, unicodedata
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


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
    if status == 'favoritos':
        livros = livros.filter(favorito=True)

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
    volume_id = request.GET.get('volume_id')
    dados_volume = {}

    if volume_id:
        # Buscar os dados diretamente pela ID do volume
        url = f'https://www.googleapis.com/books/v1/volumes/{volume_id}'
        resposta = requests.get(url)

        if resposta.status_code == 200:
            volume = resposta.json().get('volumeInfo', {})
            dados_volume = {
                'titulo': volume.get('title', ''),
                'autor': ', '.join(volume.get('authors', [])),
                'data_publicacao': volume.get('publishedDate', ''),
                'descricao': volume.get('description', ''),
                'capa_url': volume.get('imageLinks', {}).get('thumbnail', '')
            }

    if request.method == 'POST':
        print("POST recebido:", request.POST)
        form = LivroForm(request.POST)
        print("Erros do form:", form.errors)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user

            livro.descricao = request.POST.get('descricao', '')
            livro.capa_url = request.POST.get('capa_url', '')
            livro.save()
            messages.success(request, "Livro cadastrado com sucesso!")
            return redirect('livros')
    else:
        form = LivroForm(initial=dados_volume)

    contexto = {'form': form}
    # Só adiciona descricao e capa_url se estiverem disponíveis
    if dados_volume:
        contexto['descricao'] = dados_volume.get('descricao', '')
        contexto['capa_url'] = dados_volume.get('capa_url', '')

    return render(request, 'livros/cadastrar_livro.html', contexto)

@login_required
def selecionar_livro(request):
    termo = request.GET.get('q')
    resultados = []

    if termo:
        url = f'https://www.googleapis.com/books/v1/volumes?q={termo}'
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            for item in dados.get('items', [])[:5]:  # pega os 5 primeiros resultados
                volume_info = item.get('volumeInfo', {})
                resultados.append({
                    'id': item.get('id'),
                    'titulo': volume_info.get('title', 'Sem título'),
                    'autor': ', '.join(volume_info.get('authors', ['Desconhecido'])),
                    'capa': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'descricao': volume_info.get('description', '')[:200]  # descrição reduzida
                })

    return render(request, 'livros/selecionar_livro.html', {'resultados': resultados, 'termo': termo})


@login_required
def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if livro.usuario != request.user:
        return redirect('livros')
    return render(request, 'livros/detalhes_livro.html', {'livro': livro})

@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if livro.usuario != request.user:
        return redirect('livros')

    if request.method == 'POST':
        form = LivroForm(request.POST, instance = livro)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.descricao = livro.descricao or request.POST.get('descricao', '')
            livro.capa_url = livro.capa_url or request.POST.get('capa_url', '')
            livro.save()
            messages.success(request, "Livro atualizado com sucesso!")
            return redirect('livros')
    else:
        form = LivroForm(instance = livro)
    return render(request, 'livros/editar_livro.html', {'form': form, 'livro': livro})

@login_required
def confirmar_exclusao(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    if livro.usuario != request.user:
        return redirect('livros')
    if request.method == 'POST':
        livro.delete()
        messages.success(request, "Livro excluído com sucesso!")
        return redirect('livros')
    
@login_required
def alternar_favorito(request, livro_id):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, id=livro_id, usuario=request.user)
        livro.favorito = not livro.favorito
        livro.save()
        return JsonResponse({'favorito': livro.favorito})
    return JsonResponse({'erro': 'Requisição inválida'}, status=400)