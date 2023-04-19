from django.db import models

class UploadNewFile(models.Model):
    csv_file = models.FileField(upload_to='csv_files/')

    def __str__(self):
        return self.csv_file.name