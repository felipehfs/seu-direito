from direito.settings.base import *

DEBUG = False 

import dj_database_url

DATABASES = {
    'default': dj_database_url.config() 
}