import os


AUTHOR = 'your name'
AUTHOR_EMAIL = 'your email'

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PUBLIC_DIR = os.path.join(PROJECT_DIR, 'public')
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')

ROUTES = '{project}.routes'

SITE_ROOT = ''

MODULES = (
    # 'staticsauce.modules.gallery',
)
