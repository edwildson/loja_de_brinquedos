from django.db import models
from infra.models.cliente_model import ClienteModel


class VendaModel(models.Model):
    cliente = models.ForeignKey(ClienteModel, on_delete=models.CASCADE, related_name='vendas')
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales'
        ordering = ['-data']

    def __str__(self):
        return f'Venda {self.id} - Cliente: {self.cliente.nome_completo}'
