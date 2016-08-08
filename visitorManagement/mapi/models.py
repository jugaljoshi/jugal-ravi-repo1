from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from visitorManagement.mapi.utils import save_image_to_s3
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import datetime
from django.utils import timezone
import logging


class Member(models.Model):
    email = models.EmailField(_('Email Address'), unique=True)
    password = models.CharField(max_length=128, editable=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(_("Mobile Number"), max_length=13)
    address = models.TextField(max_length=250)
    package = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' % self.email


class WorkBookType(models.Model):
    type = models.CharField(max_length=50, unique=True)
    wb_icon = models.ImageField(upload_to='uploads/workbook_icon', blank=True, null=True) # todo change to media/uploads
    mandatory_fields = models.CharField(max_length=1250, null=True, blank=True,
                                        help_text='Keep it empty, will be filled while creating workbook')

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
    wb_type = models.ForeignKey(WorkBookType, editable=False)
    member = models.ForeignKey(Member, editable=False)

    def __unicode__(self):
        return '%s' % self.wb_name

    def save(self, force_insert=False, force_update=False, using=None):
        super(WorkBook, self).save(force_insert, force_update, using)
        icon_file = self.wb_icon.file
        icon_file.seek(0)

        if getattr(settings, 'MEDIA_FROM_S3', None):
            conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            key = Key(bucket)
            save_image_to_s3(key, icon_file)


class VisitorManager(models.Manager):
    def get_all_active_visitor(self, workbook):
        current_datetime = timezone.now()
        #current_datetime.astimezone(timezone.utc).replace(tzinfo=None)
        return self.filter(workbook=workbook, in_time__lte=current_datetime,
                           out_time__gte=current_datetime).values()

    def get_all_field_names(self):
        names = list()
        fields = self.model._meta.get_fields()
        for field in fields:
            if field.is_relation and field.many_to_one and field.related_model is None:
                continue
            if field.model != self.model and field.model._meta.concrete_model == self.concrete_model:
                continue

            if field.name in ['workbook', 'id', 'member']:
                continue
            if hasattr(field, 'attname'):
                names.append(field.attname)
        return names


class Visitor(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    mobile_no = models.CharField(_("Mobile Number"), max_length=13, blank=True, null=True)
    vehicle_no = models.CharField(_("Vehicle Number"), max_length=20, blank=True, null=True)
    from_place = models.CharField(max_length=50, blank=True, null=True)
    destination_place = models.CharField(max_length=50, blank=True, null=True)
    in_time = models.DateTimeField(editable=True, blank=True, null=True) #editable=False
    out_time = models.DateTimeField(editable=True, blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/member_photos', blank=True, null=True) # todo change to media/uploads
    signature = models.ImageField(upload_to='uploads/signature_photos', blank=True, null=True) # todo change to media/uploads
    workbook = models.ForeignKey(WorkBook, null=False, blank=False) #editable=False
    member = models.ForeignKey(Member, null=True) # editable=False

    # object = VisitorManager()
    #
    # @property
    # def is_live(self):
    #     current_datetime = timezone.now()
    #     current_datetime.astimezone(timezone.utc).replace(tzinfo=None)
    #     return self.in_time < current_datetime < self.out_time
    #
    # def save(self, force_insert=False, force_update=False, using=None):
    #     super(Visitor, self).save(force_insert, force_update, using)
    #     photo_file = self.photo.file
    #     photo_file.seek(0)
    #
    #     signature_file = self.signature.file
    #     signature_file.seek(0)
    #
    #     if getattr(settings, 'MEDIA_FROM_S3', None):
    #         conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    #         bucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
    #         key = Key(bucket)
    #         save_image_to_s3(key, photo_file)
    #         save_image_to_s3(key, signature_file)


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