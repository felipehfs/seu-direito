from direito.settings.base import *

DEBUG = True 

import dj_database_url

DATABASES = {
    'default': dj_database_url.config() 
}