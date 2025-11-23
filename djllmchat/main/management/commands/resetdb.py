import subprocess
import djclick as click
from django.contrib.auth import get_user_model


@click.command()
def reset_db():
    subprocess.run("rm db.sqlite3", shell=True)
    subprocess.run("uv run manage.py makemigrations", shell=True)
    subprocess.run("uv run manage.py migrate", shell=True)
    User = get_user_model()
    User.objects.create_superuser(username="motk", password="mokt")
