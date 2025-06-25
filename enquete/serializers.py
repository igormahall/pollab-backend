from rest_framework import serializers
from .models import Enquete, Opcao
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema_field, extend_schema_serializer, OpenApiExample


class OpcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcao
        fields = ['id', 'texto_opcao', 'votos']
        read_only_fields = ['id', 'votos']

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Exemplo de criação de enquete",
            value={
                "titulo": "Qual seu framework favorito?",
                "duracao_horas": 48,
                "opcoes_input": ["Django", "Flask", "FastAPI"]
            },
            request_only=True
        )
    ]
)

class EnqueteSerializer(serializers.ModelSerializer):
    # Este campo é para LEITURA (quando pedimos os detalhes de uma enquete)
    opcoes = OpcaoSerializer(many=True, read_only=True)

    # Entrada: lista de strings para criar opções
    opcoes_input = serializers.ListField(
        child=serializers.CharField(max_length=255),
        write_only=True,
        help_text="Lista de strings representando as opções da enquete."
    )

    # Entrada: duração em horas fornecida pelo frontend
    duracao_horas = serializers.IntegerField(
        write_only=True,
        help_text="Duração da enquete em horas (ex: 24 para um dia)."
    )

    # Saída: status calculado dinamicamente
    status = serializers.SerializerMethodField(
        help_text="Status dinâmico da enquete: 'Aberta' ou 'Encerrada'."
    )

    class Meta:
        model = Enquete
        fields = [
            'id', 'titulo', 'data_criacao',
            'expires_at', 'delete_at', 'status',
            'opcoes', 'opcoes_input', 'duracao_horas'
        ]
        read_only_fields = ['expires_at', 'delete_at', 'data_criacao']
        examples = [
            OpenApiExample(
                "Exemplo de criação de enquete",
                value={
                    "titulo": "Qual sua linguagem preferida?",
                    "duracao_horas": 48,
                    "opcoes_input": ["Python", "JavaScript", "Kotlin"]
                },
                request_only=True,
                response_only=False
            )
        ]

    @extend_schema_field(serializers.CharField())
    def get_status(self, obj) -> str:
        return "Aberta" if obj.expires_at > timezone.now() else "Encerrada"


    def create(self, validated_data):
        """
        Criação customizada da Enquete com suas opções e datas calculadas.
        """

        opcoes_data = validated_data.pop('opcoes_input')
        duracao_horas = validated_data.pop('duracao_horas')

        now = timezone.now()
        expires_at = now + timedelta(hours=duracao_horas)
        delete_at = expires_at + timedelta(hours=72)  # 3 dias após expiração

        validated_data['expires_at'] = expires_at
        validated_data['delete_at'] = delete_at

        # Cria o objeto Enquete principal
        enquete = Enquete.objects.create(**validated_data)

        # Itera sobre os textos das opções e cria cada objeto Opcao
        for texto_opcao in opcoes_data:
            Opcao.objects.create(enquete=enquete, texto_opcao=texto_opcao)

        return enquete

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Exemplo de voto",
            value={
                "id_opcao": 3,
                "id_participante": "user_abc_123"
            },
            request_only=True
        )
    ]
)

class VotoInputSerializer(serializers.Serializer):
    """
    Serializer para validar a entrada de um voto. Não está ligado a um modelo.
    """
    id_opcao = serializers.IntegerField(
        help_text="ID da opção selecionada para votar."
    )

    # O id_participante virá do frontend, então apenas o definimos aqui.
    # Não vamos criar um campo para ele no formulário da API Navegável,
    # pois a ideia é que ele seja gerado pelo cliente (navegador).
    # Vamos pegá-lo diretamente do request.data na view.
    # Mas para o teste, vamos deixá-lo visível por enquanto.
    id_participante = serializers.CharField(
        max_length=100,
        help_text="Identificador único do participante. Ex: UUID ou token do navegador."
    )

    class Meta:
        examples = [
            OpenApiExample(
                "Exemplo de voto válido",
                value={
                    "id_opcao": 5,
                    "id_participante": "usuario_abc123"
                },
                request_only=True
            )
        ]