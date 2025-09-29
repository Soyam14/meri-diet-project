from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()

    # --- CHANGE YOUR NEW ADMIN DETAILS HERE ---
    if not User.objects.filter(username='AMIN@14').exists():
        User.objects.create_superuser(
            username='ADMIN@11',
            email='zues60860@gmail.com',
            password='Soyam@14'
        )

class Migration(migrations.Migration):

    dependencies = [
        # This now correctly points to your previous migration
        ('accounts', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]