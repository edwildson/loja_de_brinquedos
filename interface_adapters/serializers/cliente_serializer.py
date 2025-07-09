from rest_framework import serializers
from infra.models.cliente_model import ClienteModel


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteModel
        fields = ['id', 'nome_completo', 'email', 'data_nascimento', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
