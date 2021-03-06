from django.db import models


class DABSSubmissionWindowSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    period_start_date = models.DateTimeField()
    period_end_date = models.DateTimeField()
    submission_start_date = models.DateTimeField()
    submission_due_date = models.DateTimeField()
    certification_due_date = models.DateTimeField()
    submission_reveal_date = models.DateTimeField()
    submission_fiscal_year = models.IntegerField()
    submission_fiscal_quarter = models.IntegerField()
    submission_fiscal_month = models.IntegerField()
    is_quarter = models.BooleanField()

    class Meta:
        managed = True
        db_table = "dabs_submission_window_schedule"
        unique_together = (
            "submission_fiscal_year",
            "submission_fiscal_quarter",
            "submission_fiscal_month",
            "is_quarter",
        )
