import logging
import os
from django.conf import settings

def setup_logging():
    log_level = getattr(settings, 'LOG_LEVEL', 'INFO')
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(settings.BASE_DIR, 'logs', 'autoservice.log')),
            logging.StreamHandler()
        ]
    )