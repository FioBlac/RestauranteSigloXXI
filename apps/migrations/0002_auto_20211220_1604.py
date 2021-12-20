from django.db import migrations

def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'Admin'),
        Group(name=u'Bodega'),
        Group(name=u'Cajero'),
        Group(name=u'Cliente'),
        Group(name=u'Cocinero'),
        Group(name=u'Contador'),
        Group(name=u'Garzon'),
    ])


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(
        name__in=[
            u'Admin',
            u'Bodega',
            u'Cajero',
            u'Cliente',
            u'Cocinero',
            u'Contador',
            u'Garzon',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]