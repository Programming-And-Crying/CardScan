import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='ImportJob', fields=[('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)), ('adapter_name', models.CharField(max_length=64)), ('status', models.CharField(default='running', max_length=32)), ('created_at', models.DateTimeField(auto_now_add=True)), ('finished_at', models.DateTimeField(blank=True, null=True)), ('summary', models.JSONField(blank=True, default=dict)), ('created_by', models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='ImportJobRow', fields=[('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)), ('external_id', models.CharField(max_length=255)), ('status', models.CharField(max_length=32)), ('message', models.TextField(blank=True)), ('payload', models.JSONField(blank=True, default=dict)), ('created_at', models.DateTimeField(auto_now_add=True)), ('job', models.ForeignKey(on_delete=models.CASCADE, related_name='rows', to='imports.importjob'))]),
    ]
