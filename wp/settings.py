# Django settings for omm project.
from lingcod.common.default_settings import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'watersheds',
        'USER': 'postgres',
     }
}

GEOMETRY_DB_SRID = 99999

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

#SECRET_KEY = 'keep_the_one_autogenerated_by_django-admin'

ROOT_URLCONF = 'wp.urls'

TEMPLATE_DIRS = ( os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')), )

INSTALLED_APPS += ( 'arp', 
                    'lingcod.analysistools',
                    'django.contrib.humanize',
                  )

COMPRESS_CSS['application']['source_filenames'] += (
    'common/css/wp.css',
)
# The following is used to assign a name to the default folder under My Shapes 
KML_UNATTACHED_NAME = 'Areas of Inquiry'

KML_ALTITUDEMODE_DEFAULT = 'clampToGround'

#These two variables are used to determine the extent of the zoomed in image in lingcod.staticmap
#If one or both are set to None or deleted entirely than zoom will default to a dynamic zoom generator
STATICMAP_WIDTH_BUFFER = None
STATICMAP_HEIGHT_BUFFER = None

CELERY_IMPORT = ('arp.tasks',)

MARXAN_EXE = "/home/mperry/Marxan/Marxan.exe"
MARXAN_OUTDIR = "/tmp/marxan_out/"
MARXAN_NUMREPS = 20
MARXAN_NUMITNS = 1000000

from settings_local import *

