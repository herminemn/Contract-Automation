from django.db import models
from .validators import validate_file_extension


class DocFile(models.Model):
    title = models.CharField(max_length=100)
    agreement = models.FileField(upload_to='uploaded_files', validators=[validate_file_extension])

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.agreement.delete()
        super().delete(*args, **kwargs)


# class NewDocFile(models.Model):
#     new_agreement = models.ForeignKey('DocFile', on_delete=models.CASCADE)
# 
#     def delete(self, *args, **kwargs):
#         self.new_agreement.delete()
#         super().delete(*args, **kwargs)


class VarFields(models.Model):
    var_fields = models.CharField(max_length=100)
