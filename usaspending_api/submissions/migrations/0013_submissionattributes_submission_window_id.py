# Generated by Django 2.2.13 on 2020-09-01 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0012_submissionattributes_is_final_balances_for_fy'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissionattributes',
            name='submission_window',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='submissions.DABSSubmissionWindowSchedule'),
        ),
    ]
