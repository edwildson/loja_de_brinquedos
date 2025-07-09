from django.db import models


class ClienteModel(models.Model):
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clientes'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo
