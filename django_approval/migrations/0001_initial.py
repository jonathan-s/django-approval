# Generated by Django 2.2.7 on 2019-11-12 08:48

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('action', models.CharField(choices=[('new', 'New'), ('update', 'Update'), ('deleted', 'Deleted')], max_length=8)),
                ('status', models.CharField(blank=True, choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('', 'No action taken')], default='', max_length=8)),
                ('comment', models.CharField(blank=True, help_text='The reason for this change', max_length=255)),
                ('source', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, help_text='The fields as they would be saved.')),
                ('diff', models.TextField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'approval',
                'verbose_name_plural': 'approvals',
                'ordering': ('content_type__app_label', 'content_type__model', 'object_id'),
            },
        ),
    ]