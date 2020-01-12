from django.db import models

# Create your models here.

class Fund(models.Model):
    ticker = models.CharField(unique=True, max_length=10)
    function = models.CharField(max_length=10)
    interval = models.CharField(max_length=10)
    days_to_store = models.IntegerField()

    low_freq_period = models.IntegerField()
    high_freq_period = models.IntegerField()
    low_streak_alert = models.IntegerField()
    high_streak_alert = models.IntegerField()

    status = models.CharField(max_length=10)
    status_duration = models.IntegerField()
    prev_status = models.CharField(max_length=10, null=True)
    holiday = models.BooleanField()

    def __str__(self):
        return f"ticker: {self.ticker} - {self.function} - {self.interval}\n\
        low_period: {self.low_freq_period}\n\
        low_streak_alert: {self.low_streak_alert}\n\
        high_period: {self.high_freq_period}\n\
        high_streak_alert: {self.high_streak_alert}\n\
        status: {self.status}\n\
        status_duration: {self.status_duration}\n\
        prev_status: {self.prev_status}\n\
        holiday: {self.holiday}\n"

class FundPrices(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    freq_type = models.CharField(max_length=10)
    date = models.DateField()
    price = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["fund", "freq_type", "date"],
                name="no_repeated_dates"
            )
        ]

    def __str__(self):
        return f"fund: {self.fund.ticker}\n\
        freq_type: {self.freq_type}\n\
        date: {self.date}\n\
        price: {self.price}\n\
        "