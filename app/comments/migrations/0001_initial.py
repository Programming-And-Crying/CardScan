import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Comment', fields=[('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)), ('target_type', models.CharField(max_length=16)), ('target_id', models.UUIDField()), ('text', models.TextField()), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)), ('is_deleted_soft', models.BooleanField(default=False)), ('created_by', models.ForeignKey(null=True, on_delete=models.SET_NULL, to=settings.AUTH_USER_MODEL))]),
    ]
