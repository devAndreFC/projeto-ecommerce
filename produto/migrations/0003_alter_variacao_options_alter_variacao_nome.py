# Generated by Django 4.1 on 2022-08-31 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_variacao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variacao',
            options={'verbose_name': 'Variação', 'verbose_name_plural': 'Variações'},
        ),
        migrations.AlterField(
            model_name='variacao',
            name='nome',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
