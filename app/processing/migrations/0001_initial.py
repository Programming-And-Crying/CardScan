import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='ProcessingTask', fields=[('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)), ('task_type', models.CharField(max_length=32)), ('target_type', models.CharField(max_length=32)), ('target_id', models.UUIDField()), ('status', models.CharField(default='queued', max_length=32)), ('attempts', models.PositiveIntegerField(default=0)), ('started_at', models.DateTimeField(blank=True, null=True)), ('finished_at', models.DateTimeField(blank=True, null=True)), ('error_message', models.TextField(blank=True)), ('metadata_json', models.JSONField(blank=True, default=dict))]),
    ]
