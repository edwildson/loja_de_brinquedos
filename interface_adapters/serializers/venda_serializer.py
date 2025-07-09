from rest_framework import serializers
from infra.models.venda_model import VendaModel


class VendaSerializer(serializers.ModelSerializer):
    cliente_id = serializers.IntegerField(write_only=True, required=False)
    cliente_nome = serializers.CharField(source='cliente.nome_completo', read_only=True)

    class Meta:
        model = VendaModel
        fields = ['id', 'cliente_id', 'cliente_nome', 'data', 'valor', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_cliente_id(self, value):
        """Valida se o cliente_id existe"""
        if value:
            from infra.models.cliente_model import ClienteModel
            try:
                ClienteModel.objects.get(id=value)
            except ClienteModel.DoesNotExist:
                raise serializers.ValidationError("Cliente não encontrado")
        return value

    def create(self, validated_data):
        cliente_id = validated_data.pop('cliente_id', None)
        if cliente_id:
            from infra.models.cliente_model import ClienteModel
            validated_data['cliente'] = ClienteModel.objects.get(id=cliente_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        cliente_id = validated_data.pop('cliente_id', None)
        if cliente_id:
            from infra.models.cliente_model import ClienteModel
            validated_data['cliente'] = ClienteModel.objects.get(id=cliente_id)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Se instance é um dicionário (do to_representation do ModelSerializer)
        if isinstance(instance, dict):
            cliente = instance.get('cliente')
            data['cliente_id'] = cliente.id if cliente else None
        else:
            # Se instance é um objeto do modelo
            data['cliente_id'] = instance.cliente.id if instance.cliente else None
        return data
