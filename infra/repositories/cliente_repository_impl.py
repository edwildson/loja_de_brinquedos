import logging
from domain.repositories.cliente_repository import ClienteRepository
from domain.entities.cliente import Cliente
from infra.models.cliente_model import ClienteModel
from typing import List, Optional

logger = logging.getLogger(__name__)

class ClienteRepositoryImpl(ClienteRepository):
    def add(self, cliente: Cliente) -> Cliente:
        logger.info('Persistindo novo cliente', extra={'nome': cliente.nome_completo, 'email': cliente.email})
        obj = ClienteModel.objects.create(
            nome_completo=cliente.nome_completo,
            email=cliente.email,
            data_nascimento=cliente.data_nascimento
        )
        return self._to_entity(obj)

    def get(self, cliente_id: int) -> Optional[Cliente]:
        logger.info(f'Buscando cliente id={cliente_id}')
        try:
            obj = ClienteModel.objects.get(id=cliente_id)
            return self._to_entity(obj)
        except ClienteModel.DoesNotExist:
            return None

    def list(self, nome: Optional[str] = None, email: Optional[str] = None) -> List[Cliente]:
        logger.info('Listando clientes no repositório', extra={'nome': nome, 'email': email})
        qs = ClienteModel.objects.all()
        if nome:
            qs = qs.filter(nome_completo__icontains=nome)
        if email:
            qs = qs.filter(email__icontains=email)
        return [self._to_entity(obj) for obj in qs]

    def update(self, cliente: Cliente) -> Cliente:
        logger.info(f'Atualizando cliente id={cliente.id}', extra={'nome': cliente.nome_completo, 'email': cliente.email})
        obj = ClienteModel.objects.get(id=cliente.id)
        obj.nome_completo = cliente.nome_completo
        obj.email = cliente.email
        obj.data_nascimento = cliente.data_nascimento
        obj.save()
        return self._to_entity(obj)

    def delete(self, cliente_id: int) -> bool:
        logger.info(f'Deletando cliente id={cliente_id} no repositório')
        deleted_count, _ = ClienteModel.objects.filter(id=cliente_id).delete()
        return deleted_count > 0

    def _to_entity(self, obj: ClienteModel) -> Cliente:
        return Cliente(
            id=obj.id,
            nome_completo=obj.nome_completo,
            email=obj.email,
            data_nascimento=obj.data_nascimento
        )
