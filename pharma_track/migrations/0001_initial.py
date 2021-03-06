# Generated by Django 2.0.5 on 2018-09-11 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=400, null=True)),
                ('subName', models.CharField(blank=True, max_length=400, null=True)),
                ('indication', models.CharField(blank=True, max_length=400, null=True)),
                ('phase', models.CharField(choices=[('1', 'Phase 1'), ('2', 'Phase 2'), ('3', 'Phase 3'), ('4', 'Phase 4')], default='1', max_length=400)),
            ],
            options={
                'verbose_name': 'Drug',
                'verbose_name_plural': 'Drugs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='drug',
            unique_together={('name', 'subName', 'indication')},
        ),
    ]
