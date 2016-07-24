from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import datetime
import logging


class Member(models.Model):
    email = models.EmailField(_('Email Address'), unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(_("Mobile Number"), max_length=13)
    address = models.TextField(max_length=250)
    package = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' % self.email


class WorkBookType(models.Model):
    type = models.CharField(max_length=50, unique=True)
    mandatory_fields = models.TextField(max_length=1250,
                                     help_text='Comma separated visitor table\'s column name (eg: name,mobile_no)',
                                     blank=False, null=False)

    def __unicode__(self):
        return '%s' % self.type


class WorkBook(models.Model):

    DEFAULT = 1
    VEHICLES = 2
    SERVANTS = 3

    WORK_BOOK_TYPE = (
        (VEHICLES, 'Vehicles'),
        (SERVANTS, 'Servants'),
        (DEFAULT, 'Default'),
    )

    wb_name = models.CharField(max_length=50)
    wb_icon = models.ImageField(upload_to='uploads/workbook_icon', blank=True, null=True)
    wb_type = models.ForeignKey(WorkBookType)
    member = models.ForeignKey(Member, blank=True, null=True, editable=False)


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(_("Mobile Number"), max_length=13)
    vehicle_no = models.CharField(_("Mobile Number"), max_length=20, blank=True, null=True)
    from_place = models.CharField(_("Mobile Number"), max_length=50)
    destination_place = models.CharField(_("Mobile Number"), max_length=50)
    in_time = models.DateTimeField(editable=False)
    out_time = models.DateTimeField(editable=True)
    photo = models.ImageField(upload_to='uploads/member_photos', blank=True, null=True)
    signature = models.ImageField(upload_to='uploads/signature_photos')
    workbook = models.ForeignKey(WorkBook, null=False, blank=False)

    @property
    def is_live(self):
        current_datetime = datetime.datetime.now()
        return self.in_time < current_datetime < self.out_time

    def save(self, force_insert=False, force_update=False, using=None):
        super(Visitor, self).save(force_insert, force_update, using)
        photo_file = self.photo.file
        photo_file.seek(0)

        signature_file = self.signature.file
        signature_file.seek(0)

        if getattr(settings, 'MEDIA_FROM_S3', None):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            key = Key(bucket)
            self.save_image_to_s3(key, photo_file)
            self.save_image_to_s3(key, signature_file)

    def save_image_to_s3(self, key, file_name):
        key.key = 'media/%s' % file_name.name
        key.set_contents_from_file(file)
        logging.debug("Image from S3 : %s" % key.key)


'''
class WorkBookTypeOptions():
    def add_to_query(self, query, aliases):
        try:
            choices = Member._meta.get_all_field_names()
        except:
            choices  = []
        query.add_q(models.Q(id__in=choices))
        query.distinct = True
'''

#c3 = [filter(lambda x: x in c1, sublist) for sublist in c2]
#set(b1).intersection(b2)