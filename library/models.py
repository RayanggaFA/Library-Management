from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from barcode import Code39
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os

class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Kelas = models.CharField(max_length=40)
    # branch = models.CharField(max_length=40)

    def __str__(self):
        return self.user.first_name + '[' + str(self.Kelas) + ']'

    @property
    def get_name(self):
        return self.user.first_name

    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice = [
        ('karya umum', 'KARYA UMUM'),
        ('Filsafat dan psikologi', 'FILSAFAT DAN PSIKOLOGI'),
        ('Agama', 'AGAMA'),
        ('Ilmu sosial', 'ILMU SOSIAL'),
        ('Bahasa', 'BAHASA'),
        ('Ilmu alam dan matematika', 'ILMU ALAM DAN MATEMATIKA'),
        ('Teknologi dan ilmu terapan', 'TEKNOLOGI DAN ILMU TERAPAN'),
        ('Kesenian hiburan dan olahraga', 'KESENIAN HIBURAN DAN OLAHRAGA'),
        ('kesusastraan', 'KESUSASTRAAN'),
        ('Geografi dan sejarah', 'GEOGRAFI DAN SEJARAH'),
        ('Koleksi khusus', 'KOLEKSI KHUSUS')
    ]
    name = models.CharField(max_length=250)
    isbn = models.PositiveIntegerField(unique=True)
    copies = models.PositiveBigIntegerField()
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30, choices=catchoice, default='education')
    barcode = models.ImageField(upload_to='barcodes/', blank=True)

    def __str__(self):
        return str(self.name) + "[" + str(self.isbn) + ']'

    def save(self, *args, **kwargs):
        # Check if barcode is not set
        if not self.barcode:
            self.generate_barcode()
        super().save(*args, **kwargs)

    def generate_barcode(self):
        file_name = f'barcode_{self.isbn}.png'
        barcode_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
        file_path = os.path.join(barcode_dir, file_name)

        # Ensure the barcodes directory exists
        if not os.path.exists(barcode_dir):
            os.makedirs(barcode_dir)

        # Generate barcode if it doesn't already exist
        if not os.path.exists(file_path):
            barcode = Code39(str(self.isbn), writer=ImageWriter(), add_checksum=False)
            buffer = BytesIO()
            barcode.write(buffer)

            # Save barcode image in memory
            self.barcode.save(file_name, ContentFile(buffer.getvalue()), save=False)


def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):
    Kelas = models.CharField(max_length=30)
    isbn = models.CharField(max_length=30)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return self.Kelas
    
    def end_issue_early(self):
        self.expirydate = datetime.today().date()
        self.save
