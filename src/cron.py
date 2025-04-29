import logging

from django.core.management import call_command

logger = logging.getLogger(__name__)

def perform_backup():
    try:
        call_command('dbbackup')
    except Exception as e:
        logger.error(f"Error during backup: {e}", exc_info=True)
    else:
        logger.info("Backup completed successfully.")