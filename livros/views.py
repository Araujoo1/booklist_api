from django.shortcuts import render,redirect,get_object_or_404
from .models import Livro
from .forms import LivroForm

def home(request):
    return render(request, 'home.html')

def livros(request):
    livros = Livro.objects.all()
    return render(request, 'livros.html', {'livros': livros})

def cadastrar_livro(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        data_publicacao = request.POST.get('data_publicacao')
        descricao = request.POST.get('descricao')
        capa_url = request.POST.get('capa_url')
        lido = 'lido' in request.POST

        Livro.objects.create(
            titulo=titulo,
            autor=autor,
            data_publicacao=data_publicacao,
            descricao=descricao,
            capa_url=capa_url,
            lido=lido
        )
        return redirect('livros')

    return render(request, 'cadastrar_livro.html')

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