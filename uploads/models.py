from django.db import models


class DocFile(models.Model):
    title = models.CharField(max_length=50)
    agreement = models.FileField(upload_to='')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.agreement.delete()
        super().delete(*args, **kwargs)
