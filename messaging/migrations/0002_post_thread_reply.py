# Generated by Django 4.1.3 on 2022-11-19 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='messaging.post')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.board')),
            ],
            bases=('messaging.post',),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='messaging.post')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.thread')),
            ],
            bases=('messaging.post',),
        ),
    ]