from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from enquete.models import Enquete, Opcao


class Command(BaseCommand):
    help = 'Cria enquetes de teste com expiração automática e múltiplas opções.'

    def handle(self, *args, **kwargs):
        agora = timezone.now()

        enquetes = [
            {
                "titulo": "Qual seu sistema operacional favorito?",
                "opcoes": ["Windows", "Linux", "macOS"],
                "duracao_horas": 12
            },
            {
                "titulo": "Qual linguagem você mais usa?",
                "opcoes": ["Python", "JavaScript", "Java", "C#"],
                "duracao_horas": 24
            },
            {
                "titulo": "Qual seu editor de código preferido?",
                "opcoes": ["VS Code", "PyCharm", "Vim", "Sublime Text"],
                "duracao_horas": 48
            },
        ]

        for dados in enquetes:
            expires_at = agora + timedelta(hours=dados["duracao_horas"])
            delete_at = expires_at + timedelta(hours=72)

            enquete = Enquete.objects.create(
                titulo=dados["titulo"],
                data_criacao=agora,
                expires_at=expires_at,
                delete_at=delete_at
            )

            for texto in dados["opcoes"]:
                Opcao.objects.create(enquete=enquete, texto_opcao=texto)

            self.stdout.write(self.style.SUCCESS(f'✔️ Enquete criada: "{enquete.titulo}"'))

        self.stdout.write(self.style.SUCCESS("✅ Enquetes de teste criadas com sucesso."))
