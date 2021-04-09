from django.db import models


class Job(models.Model):

    STATUS = (
       ('new', 'new'),
       ('running', 'running'),
       ('success', 'success')
    )

    request = models.CharField(verbose_name='OTL request', max_length=2048)

    status = models.CharField(
        verbose_name='Request status',
        max_length=12,
        choices=STATUS,
        default=STATUS[0][0]
    )

    result = models.ForeignKey(
        'JobResult',
        verbose_name='Result',
        related_name='job',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    completed = models.BooleanField(
        verbose_name='Job completed',
        null=False,
        default='False'
    )

    class Meta:
        verbose_name = 'Dispatcher job',
        verbose_name_plural = 'Dispatcher jobs'


class JobResult(models.Model):

    payload = models.JSONField(
        verbose_name='Payload',
        blank=True,
        null=True
    )

    ttl = models.DateTimeField(
        verbose_name='TTL',
        null=True
    )

    class Meta:
        verbose_name = 'Dispatcher job result',
        verbose_name_plural = 'Dispatcher jobs results'
