from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Enquete, Opcao, Voto
from .serializers import EnqueteSerializer, VotoInputSerializer
from django.db.models import Case, When, Value, IntegerField


class EnqueteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar e recuperar enquetes.
    """

    serializer_class = EnqueteSerializer

    def get_queryset(self):
        """
        Lista todas as enquetes, abertas primeiro, ordenadas pela data de criação.
        A prioridade é calculada dinamicamente com base no vencimento (`expires_at`).
        """
        base_qs = Enquete.objects.all().prefetch_related('opcoes')

        if self.action == 'retrieve':
            return base_qs

        now = timezone.now()
        return base_qs.annotate(
            prioridade=Case(
                When(expires_at__gt=now, then=Value(0)),  # Abertas primeiro
                default=Value(1),                         # Depois as encerradas
                output_field=IntegerField()
            )
        ).order_by('prioridade', '-data_criacao')

    @action(detail=True, methods=['post'])
    def votar(self, request, pk=None):
        """
        Permite votar em uma enquete, desde que ainda não esteja expirada.
        """
        enquete = self.get_object()
        serializer = VotoInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id_participante = serializer.validated_data['id_participante']
        id_opcao = serializer.validated_data['id_opcao']

        # Impede votos em enquetes já expiradas
        if enquete.expires_at <= timezone.now():
            return Response({'error': 'Esta enquete está encerrada.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Impede múltiplos votos
        if Voto.objects.filter(enquete=enquete, id_participante=id_participante).exists():
            return Response({'error': 'Este participante já votou nesta enquete.'},
                            status=status.HTTP_409_CONFLICT)

        try:
            opcao_selecionada = Opcao.objects.get(id=id_opcao, enquete=enquete)
        except Opcao.DoesNotExist:
            return Response({'error': 'Opção inválida para esta enquete.'},
                            status=status.HTTP_400_BAD_REQUEST)

        opcao_selecionada.votos += 1
        opcao_selecionada.save(update_fields=['votos'])

        Voto.objects.create(
            enquete=enquete,
            opcao_escolhida=opcao_selecionada,
            id_participante=id_participante
        )

        return Response(EnqueteSerializer(enquete).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def limpar_enquetes_expiradas(self, request):
        """
        Deleta enquetes cuja data de exclusão programada (`delete_at`) já passou.
        """
        now = timezone.now()
        expiradas = Enquete.objects.filter(delete_at__lte=now)
        count = expiradas.count()
        expiradas.delete()
        return Response({'message': f'{count} enquetes deletadas com sucesso.'})
