from domain.repositories.venda_repository import VendaRepository
from application.dtos.estatisticas_dto import EstatisticasVendasPorDiaDTO, ClienteDestaqueDTO
from typing import List, Optional
from infra.models.venda_model import VendaModel
from infra.models.cliente_model import ClienteModel
from django.db.models import Sum, Avg, Count, F
from datetime import datetime, timedelta
from django.utils import timezone


class EstatisticasUseCase:
    def __init__(self, venda_repository: VendaRepository):
        self.__venda_repository = venda_repository

    def vendas_por_dia(self, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> EstatisticasVendasPorDiaDTO:
        # Se não houver filtros de data, retorna todas as vendas
        if not data_inicio and not data_fim:
            vendas = (
                VendaModel.objects
                .values('data')
                .annotate(total_vendas=Sum('valor'))
                .order_by('data')
            )
        else:
            # Se apenas uma data for fornecida, usa a outra como padrão
            if data_inicio and not data_fim:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                data_fim = data_inicio + timedelta(days=30)
            elif data_fim and not data_inicio:
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
                data_inicio = data_fim - timedelta(days=30)
            else:
                # Ambas as datas fornecidas
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

            # Usando o ORM diretamente para agregação com filtro de datas
            vendas = (
                VendaModel.objects
                .filter(data__gte=data_inicio, data__lte=data_fim)
                .values('data')
                .annotate(total_vendas=Sum('valor'))
                .order_by('data')
            )
        
        vendas_por_dia = [
            {'data': v['data'], 'total_vendas': float(v['total_vendas'])} for v in vendas
        ]
        return EstatisticasVendasPorDiaDTO(vendas_por_dia=vendas_por_dia)

    def clientes_destaque(self) -> dict:
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
