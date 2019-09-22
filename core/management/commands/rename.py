import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = 'Renames Django Project'

    def add_arguments(self, parser):
        parser.add_argument('new_project_name', type=str, help='The new project name')

    def handle(self, *args, **kwargs):
        new_project_name = kwargs['new_project_name']
        files_to_rename = [
            'dj_blueprint/settings.py',
            'dj_blueprint/wsgi.py',
            'manage.py'
        ]
        folder_to_rename = 'dj_blueprint'

        for f in files_to_rename:
            with open(f, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace('dj_blueprint', new_project_name)

            with open(f, 'w') as file:
                file.write(filedata)

        os.rename(folder_to_rename, new_project_name)
        self.stdout.write(self.style.SUCCESS(f'Project has been renamed to {new_project_name}'))
