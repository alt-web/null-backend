# Generated by Django 4.1.4 on 2023-01-02 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_reply_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='preview',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='messaging.attachment'),
        ),
    ]
