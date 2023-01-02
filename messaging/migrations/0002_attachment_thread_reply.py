# Generated by Django 4.1.4 on 2023-01-01 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(max_length=59)),
                ('name', models.CharField(max_length=256)),
                ('mimetype', models.CharField(max_length=36)),
                ('size', models.PositiveIntegerField()),
                ('width', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('height', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('length', models.PositiveIntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='messaging.board')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attachments', models.ManyToManyField(to='messaging.attachment')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='messaging.thread')),
            ],
        ),
    ]
