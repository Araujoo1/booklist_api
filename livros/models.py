from django.db import models

class Livro (models.Model):
    titulo = models.CharField(max_length=70)
    autor = models.CharField(max_length=70)
    descricao = models.TextField(blank=True)
    capa_url = models.URLField(blank=True)
    data_publicacao = models.CharField(max_length=50, blank=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
