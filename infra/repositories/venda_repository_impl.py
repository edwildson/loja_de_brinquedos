from domain.repositories.venda_repository import VendaRepository
from domain.entities.venda import Venda
from infra.models.venda_model import VendaModel
from infra.models.cliente_model import ClienteModel
from typing import List, Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)

class VendaRepositoryImpl(VendaRepository):
    def add(self, venda: Venda) -> Venda:
        logger.info('Persistindo nova venda', extra={'cliente_id': venda.cliente_id, 'valor': venda.valor})
        
        # Verifica se o cliente existe
        try:
            ClienteModel.objects.get(id=venda.cliente_id)
        except ClienteModel.DoesNotExist:
            raise ValueError(f"Cliente com id {venda.cliente_id} não encontrado")
        
        obj = VendaModel.objects.create(
            cliente_id=venda.cliente_id,
            data=venda.data,
            valor=venda.valor
        )
        return self._to_entity(obj)

    def get(self, venda_id: int) -> Optional[Venda]:
        logger.info(f'Buscando venda id={venda_id}')
        try:
            obj = VendaModel.objects.get(id=venda_id)
            return self._to_entity(obj)
        except VendaModel.DoesNotExist:
            return None

    def update(self, venda: Venda) -> Venda:
        logger.info(f'Atualizando venda id={venda.id}', extra={'cliente_id': venda.cliente_id, 'valor': venda.valor})
        try:
            obj = VendaModel.objects.get(id=venda.id)
            obj.cliente_id = venda.cliente_id
            obj.data = venda.data
            obj.valor = venda.valor
            obj.save()
            return self._to_entity(obj)
        except VendaModel.DoesNotExist:
            raise ValueError(f"Venda com id {venda.id} não encontrada")

    def delete(self, venda_id: int) -> bool:
        logger.info(f'Deletando venda id={venda_id}')
        try:
            obj = VendaModel.objects.get(id=venda_id)
            obj.delete()
            return True
        except VendaModel.DoesNotExist:
            return False

    def list_by_cliente(self, cliente_id: int) -> List[Venda]:
        logger.info(f'Listando vendas do cliente id={cliente_id}')
        qs = VendaModel.objects.filter(cliente_id=cliente_id)
        return [self._to_entity(obj) for obj in qs]

    def list_by_period(self, start_date: Optional[date], end_date: Optional[date]) -> List[Venda]:
        logger.info('Listando vendas por período', extra={'start_date': start_date, 'end_date': end_date})
        qs = VendaModel.objects.all()
        if start_date:
            qs = qs.filter(data__gte=start_date)
        if end_date:
            qs = qs.filter(data__lte=end_date)
        return [self._to_entity(obj) for obj in qs]

    def _to_entity(self, obj: VendaModel) -> Venda:
        return Venda(
            id=obj.id,
            cliente_id=obj.cliente_id,
            data=obj.data,
            valor=float(obj.valor)
        )

    def get_clientes_destaque(self) -> dict:
        """Retorna estatísticas dos clientes com maior volume, média e frequência"""
        from django.db.models import Sum, Avg, Count
        
        # Maior volume de vendas
        maior_volume = (
            ClienteModel.objects
            .annotate(total_vendas=Sum('vendas__valor'))
            .order_by('-total_vendas')
            .values('id', 'nome_completo', 'total_vendas')
            .first()
        )
        
        # Maior média de valor por venda
        maior_media = (
            ClienteModel.objects
            .annotate(media_vendas=Avg('vendas__valor'))
            .order_by('-media_vendas')
            .values('id', 'nome_completo', 'media_vendas')
            .first()
        )
        
        # Maior frequência de compras (dias únicos)
        maior_frequencia = (
            ClienteModel.objects
            .annotate(freq=Count('vendas__data', distinct=True))
            .order_by('-freq')
            .values('id', 'nome_completo', 'freq')
            .first()
        )
        
        return {
            'maior_volume': {
                'cliente_id': maior_volume['id'] if maior_volume else None,
                'nome_completo': maior_volume['nome_completo'] if maior_volume else None,
                'valor': float(maior_volume['total_vendas'] or 0) if maior_volume else 0
            },
            'maior_media': {
                'cliente_id': maior_media['id'] if maior_media else None,
                'nome_completo': maior_media['nome_completo'] if maior_media else None,
                'valor': float(maior_media['media_vendas'] or 0) if maior_media else 0
            },
            'maior_frequencia': {
                'cliente_id': maior_frequencia['id'] if maior_frequencia else None,
                'nome_completo': maior_frequencia['nome_completo'] if maior_frequencia else None,
                'valor': float(maior_frequencia['freq'] or 0) if maior_frequencia else 0
            }
        }
