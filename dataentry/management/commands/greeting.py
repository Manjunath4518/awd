from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'greet'
    
    def handle(self,*args, **kwargs):
        print('ho rinku')