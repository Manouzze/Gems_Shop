# Generated by Django 4.0.5 on 2022-06-28 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0003_alter_cartitem_gem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='gem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.gem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
