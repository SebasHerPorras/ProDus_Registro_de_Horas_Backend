from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_normalize_role_codes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name='assistant',
                        serialize=False,
                        to='users.user',
                        verbose_name='Usuario',
                    ),
                ),
                ('start_date', models.DateField(verbose_name='Fecha de inicio')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Fecha de finalización')),
                ('weekly_hours', models.IntegerField(verbose_name='Horas semanales')),
            ],
            options={
                'verbose_name': 'Asistente',
                'verbose_name_plural': 'Asistentes',
                'db_table': 'assistant',
                'constraints': [
                    models.CheckConstraint(
                        condition=models.Q(weekly_hours__gt=0),
                        name='assistant_weekly_hours_gt_0',
                    ),
                ],
            },
        ),
    ]
