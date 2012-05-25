# Django settings for omm project.
from lingcod.common.default_settings import *

APP_NAME = "Regional Aquatic Prioritization and Mapping Tool"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'watersheds',
        'USER': 'postgres', }
}

GEOMETRY_DB_SRID = 99997

TIME_ZONE = 'America/Vancouver'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

#SECRET_KEY = 'keep_the_one_autogenerated_by_django-admin'

ROOT_URLCONF = 'wp.urls'

TEMPLATE_DIRS = ( os.path.realpath(os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')), )

INSTALLED_APPS += ( 'arp', 
                    'djkombu',
                    #'django_extensions', 
                    'lingcod.analysistools',
                    'django.contrib.humanize',) 

COMPRESS_JS['application']['source_filenames'] += (
    'common/js/treeview/jquery.treeview.js',
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

MARXAN_BIN =  '/usr/local/marxan243/MarOpt_v243_Linux32' # or 64 bit?
MARXAN_OUTDIR =  os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'marxan_output'))
MARXAN_TEMPLATEDIR = os.path.join(MARXAN_OUTDIR, 'template')
MARXAN_NUMREPS = 20
MARXAN_NUMITNS = 1000000

LOG_FILE =  os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'wp.log'))
LOGFILE =  os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'wp.log'))
USE_CACHE = False

# ecotrust.org
GOOGLE_API_KEY = 'ABQIAAAAIcPbR_l4h09mCMF_dnut8RQbjMqOReB17GfUbkEwiTsW0KzXeRQ-3JgvCcGix8CM65XAjBAn6I0bAQ'

TEMPLATE_DEBUG = False
LOGIN_REDIRECT_URL = '/tool/'
HELP_EMAIL = 'ksdev@ecotrust.org'
STATIC_URL = ADMIN_MEDIA_PREFIX

from settings_local import *

# makes djcelery and djkombu happy?
DATABASE_ENGINE = DATABASES['default']['ENGINE']
DATABASE_NAME = DATABASES['default']['NAME']
DATABASE_USER = DATABASES['default']['USER']


