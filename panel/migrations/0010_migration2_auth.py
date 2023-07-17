from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0009_migration_auth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telefono_contacto',
            field=models.CharField(max_length=10, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='anexo',
            field=models.CharField(max_length=10, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.CharField(max_length=10, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='id_red',
            field=models.CharField(max_length=10, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='doc_ide',
            field=models.CharField(max_length=10, blank=True, default=''),
        ),
    ]