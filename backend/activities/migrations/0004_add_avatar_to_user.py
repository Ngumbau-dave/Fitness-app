from django.db import migrations
from django.db.models import ImageField

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # Latest auth migration
        ('activities', '0001_initial'),  # Replace with your last migration name
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=ImageField(upload_to='avatars/', blank=True, null=True),
        ),
    ]