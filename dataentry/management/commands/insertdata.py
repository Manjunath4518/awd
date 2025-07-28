from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help = 'It will insert data into DB'

    def handle(self, *args, **kwargs):
        roll_no = 6773
        if not Student.objects.filter(roll_no=roll_no).exists():
            Student.objects.create(roll_no=roll_no, name='rinku', age=20)
            self.stdout.write(self.style.SUCCESS('Data inserted successfully'))
        else:
            self.stdout.write(self.style.WARNING('Student already exists'))
