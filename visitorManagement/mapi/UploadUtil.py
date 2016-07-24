'''

from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2



from google.appengine.api import images
from google.appengine.ext import ndb


from google.appengine.api import blobstore
from google.appengine.api import images
bkey = blobstore.create_gs_key('/gs/bucket/object')
url = images.get_serving_url(bkey)



from google.appengine.api import images
if self.request.get("id"):
            photo = Photo.get_by_id(int(self.request.get("id")))

            if photo:
                img = images.Image(photo.full_size_image)
                img.resize(width=80, height=100)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return

'''
