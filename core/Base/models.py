from mongoengine import Document, DateTimeField
from datetime import datetime
from django.utils import timezone

class TimestampedDocument(Document):
    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))

    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now(timezone.now)
        self.updated_at = datetime.now(timezone.now)
        return super(TimestampedDocument, self).save(*args, **kwargs)
