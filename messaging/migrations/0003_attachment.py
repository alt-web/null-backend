# Generated by Django 4.1.3 on 2022-11-19 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_post_thread_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.post')),
            ],
        ),
    ]