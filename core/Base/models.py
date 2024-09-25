from mongoengine import Document, DateTimeField
from datetime import datetime, timezone

class TimestampedDocument(Document):
    created_at = DateTimeField(default=lambda: datetime.utcnow())
    updated_at = DateTimeField(default=lambda: datetime.utcnow())

    meta = {'abstract': True}

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        return super(TimestampedDocument, self).save(*args, **kwargs)
