from django.db import migrations


def normalize_role_codes(apps, schema_editor):
    Role = apps.get_model('login', 'Role')
    for role in Role.objects.all():
        normalized = (role.code or '').strip().lower()
        if role.code != normalized:
            role.code = normalized
            role.save(update_fields=['code'])


class Migration(migrations.Migration):
    dependencies = [
        ('login', '0002_role_user_full_name_user_role'),
    ]

    operations = [
        migrations.RunPython(normalize_role_codes, migrations.RunPython.noop),
    ]
