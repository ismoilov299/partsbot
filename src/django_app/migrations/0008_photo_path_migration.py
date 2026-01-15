# Generated migration to replace photo_file_id with photo_path

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0007_ustaxona'),
    ]

    operations = [
        # Add photo_path field to Shop
        migrations.AddField(
            model_name='shop',
            name='photo_path',
            field=models.CharField(blank=True, help_text='Local path to shop photo file', max_length=500, null=True),
        ),
        # Add photo_path field to UstaXona
        migrations.AddField(
            model_name='ustaxona',
            name='photo_path',
            field=models.CharField(blank=True, help_text='Local path to service center photo file', max_length=500, null=True),
        ),
        # Remove photo_file_id from Shop (optional - can keep for backward compatibility)
        # migrations.RemoveField(
        #     model_name='shop',
        #     name='photo_file_id',
        # ),
        # migrations.RemoveField(
        #     model_name='ustaxona',
        #     name='photo_file_id',
        # ),
    ]

