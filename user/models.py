from mongoengine import signals
from flask import url_for
import os

from application import db
from utilities.common import utc_now_ts as now
from settings import STATIC_IMAGE_URL, AWS_BUCKET, AWS_CONTENT_URL

class User(db.Document):
    email = db.EmailField(db_field="e", required=True)
    first_name = db.StringField(db_field="fn", max_length=50)
    last_name = db.StringField(db_field="ln", max_length=50)
    created = db.IntField(db_field="c", default=now())
    company = db.StringField(db_field="y", max_length=50)
    phone = db.StringField(db_field="p", max_length=20)
    job = db.StringField(db_field="j", max_length=50)
    question = db.StringField(db_field="q", max_length=160)
    email_confirmed = db.BooleanField(db_field="ecf", default=False)
    change_configuration = db.DictField(db_field="cc")
    profile_image = db.StringField(db_field="i", default=None)
    event = db.StringField(db_field="v",default=None)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.email = document.email.lower()

    def profile_imgsrc(self, size):
        if self.profile_image:
            if AWS_BUCKET:
                return os.path.join(AWS_CONTENT_URL, AWS_BUCKET, 'user', '%s.%s.%s.png' % (self.id, self.profile_image, size))
            else:
                return url_for('static', filename=os.path.join(STATIC_IMAGE_URL, 'user', '%s.%s.%s.png' % (self.id, self.profile_image, size)))
        else:
            return url_for('static', filename=os.path.join(STATIC_IMAGE_URL, 'user', 'no-profile.%s.png' % (size)))

    meta = {
        'indexes': ['email', '-created']
    }

signals.pre_save.connect(User.pre_save, sender=User)
