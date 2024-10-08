# Generated by Django 5.1.1 on 2024-09-12 11:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_alter_policy_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="policy",
            name="coverage_amount",
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
        migrations.AlterField(
            model_name="policy",
            name="premium_amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=15, null=True
            ),
        ),
    ]
