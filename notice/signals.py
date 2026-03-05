from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notice
from pdf2image import convert_from_path
from pathlib import Path
from django.conf import settings

@receiver(post_save, sender=Notice)
def generate_thumbnail(sender, instance, created, **kwargs):
    if created and instance.file_upload and instance.file_upload.name.lower().endswith('.pdf'):
        try:
            pdf_path = Path(instance.file_upload.path)
            pages = convert_from_path(str(pdf_path), first_page=1, last_page=1)
            if pages:
                thumb_filename = f"notice_{instance.pk}.jpg"
                thumb_path = Path(settings.MEDIA_ROOT) / "thumbnails" / thumb_filename
                thumb_path.parent.mkdir(parents=True, exist_ok=True)
                pages[0].save(str(thumb_path), "JPEG")
                instance.thumbnail = f"thumbnails/{thumb_filename}"
                instance.save(update_fields=["thumbnail"])
                print("✅ Thumbnail created successfully!")
        except Exception as e:
            print("❌ Thumbnail generation failed:", e)