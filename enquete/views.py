from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Enquete, Opcao, Voto
from .serializers import EnqueteSerializer, VotoInputSerializer


class EnqueteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar e recuperar enquetes.
    """

    queryset = Enquete.objects.all().prefetch_related('opcoes')

    serializer_class = EnqueteSerializer

    def get_queryset(self):

        # Se a ação for 'retrieve' (buscar um único item pelo ID)...
        if self.action == 'retrieve':
            # ... permite buscar em TODAS as enquetes, independente do status
            return Enquete.objects.all().prefetch_related('opcoes')

        # Para a ação 'list' e outras, usa o queryset padrão (apenas 'Aberta')
        return super().get_queryset()

    @action(detail=True, methods=['post'])
    def votar(self, request, pk=None):
        enquete = self.get_object()
        id_participante = request.data.get('id_participante')
        id_opcao = request.data.get('id_opcao')

        if not id_participante or not id_opcao:
            return Response({'error': 'id_participante e id_opcao são obrigatórios.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if enquete.status == 'Fechada':
            return Response({'error': 'Esta enquete está fechada.'}, status=status.HTTP_403_FORBIDDEN)

        if Voto.objects.filter(enquete=enquete, id_participante=id_participante).exists():
            return Response({'error': 'Este participante já votou nesta enquete.'}, status=status.HTTP_409_CONFLICT)

        try:
            opcao_selecionada = Opcao.objects.get(id=id_opcao, enquete=enquete)
        except Opcao.DoesNotExist:
            return Response({'error': 'Opção inválida para esta enquete.'}, status=status.HTTP_400_BAD_REQUEST)

        opcao_selecionada.votos += 1
        opcao_selecionada.save(update_fields=['votos'])  # Otimização para atualizar apenas o campo de votos

        Voto.objects.create(
            enquete=enquete,
            opcao_escolhida=opcao_selecionada,
            id_participante=id_participante
        )

        serializer = EnqueteSerializer(enquete)
        return Response(serializer.data, status=status.HTTP_200_OK)