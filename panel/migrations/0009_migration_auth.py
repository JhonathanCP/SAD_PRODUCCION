from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0008_alter_registro_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dni',
            field=models.CharField(max_length=9, blank=True, default=''),
        ),
    ]