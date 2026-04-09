import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='ChangeHistory', fields=[('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)), ('target_type', models.CharField(max_length=32)), ('target_id', models.UUIDField()), ('action_type', models.CharField(max_length=32)), ('field_name', models.CharField(blank=True, max_length=100)), ('old_value_json', models.JSONField(blank=True, default=dict)), ('new_value_json', models.JSONField(blank=True, default=dict)), ('created_at', models.DateTimeField(auto_now_add=True)), ('actor', models.ForeignKey(null=True, on_delete=models.SET_NULL, to=settings.AUTH_USER_MODEL))]),
    ]
