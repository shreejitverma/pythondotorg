# Generated by Django 1.11.4 on 2017-09-23 10:13

from django.db import migrations

MARKER = '.. Migrated from Release.release_page field.\n\n'


def migrate_old_content(apps, schema_editor):
    Release = apps.get_model('downloads', 'Release')
    db_alias = schema_editor.connection.alias
    releases = Release.objects.using(db_alias).filter(
        release_page__isnull=False,
    )
    for release in releases:
        content = '\n'.join(release.release_page.content.raw.splitlines()[3:])
        release.content = MARKER + content
        release.release_page = None
        release.save()


def delete_migrated_content(apps, schema_editor):
    Release = apps.get_model('downloads', 'Release')
    Page = apps.get_model('pages', 'Page')
    db_alias = schema_editor.connection.alias
    releases = Release.objects.using(db_alias).filter(
        release_page__isnull=True,
        content__startswith=MARKER,
    )
    for release in releases:
        try:
            name = release.name
            if 'Release' not in name:
                name = f'{release.name} Release'
            page = Page.objects.get(title=name)
        except (Page.DoesNotExist, Page.MultipleObjectsReturned):
            continue
        else:
            release.release_page = page
            release.content = ''
            release.save()


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0004_auto_20170821_2000'),
    ]

    operations = [
        migrations.RunPython(migrate_old_content, delete_migrated_content),
    ]
