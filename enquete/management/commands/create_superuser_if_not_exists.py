import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    """
    Comando para criar um superusuário apenas se ele não existir.
    Usa as variáveis de ambiente DJANGO_SUPERUSER_USERNAME, etc.
    """
    help = 'Cria um superusuário de forma não-interativa, mas apenas se ele não existir.'

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.environ.get('DJANGO_SUPERUSER_USERNAME')).exists():
            User.objects.create_superuser(
                username=os.environ.get('DJANGO_SUPERUSER_USERNAME'),
                email=os.environ.get('DJANGO_SUPERUSER_EMAIL'),
                password=os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            )
            self.stdout.write(self.style.SUCCESS('Superusuário criado com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING('Superusuário já existe, nenhum foi criado.'))