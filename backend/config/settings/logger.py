import logging
import logging.config
import sys
import json
import os
from typing import Optional


class LoggingConfiguration:
    """Handles logging functionality."""

    def __init__(
            self,
            base_dir:str,
            log_dir:Optional[str]=None
):
        self._base_dir= base_dir
        if not self._base_dir:
            raise ValueError(
                'Base directory reference not set!'
            )
        self._log_dir= log_dir

    def create_log_dirs(self):
        """Creates log directories if not existing."""
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)
            print(f'Created log directory: {self._log_dir}')

    def logging_conf(self):
        """Custom logging configurations."""
        return {
            'version':1,
            'disable_existing_handlers':False,
            'formatters':{
                'json':{
                    '()': lambda:self.get_formatter(),
                },
            },
            'handlers':{
                'info_file':{
                    'class':'logging.handlers.RotatingFileHandler',
                    'level':'INFO',
                    'filename':os.path.join(self._log_dir, 'info.log'),
                    'maxBytes':1024*1024*5,
                    'backupCount':5,
                    'formatter':'json',
                },
                'error_file':{
                    'class':'logging.handlers.RotatingFileHandler',
                    'level':'ERROR',
                    'filename':os.path.join(self._log_dir, 'error.log'),
                    'maxBytes':1024*1024*5,
                    'backupCount':5,
                    'formatter':'json',
                },
                'warning_file':{
                    'class':'logging.handlers.RotatingFileHandler',
                    'level':'WARNING',
                    'filename':os.path.join(self._log_dir, 'warning.log'),
                    'maxBytes':1024*1024*5,
                    'backupCount':5,
                    'formatter':'json',
                },
                'console':{
                    'class':'logging.SteamHandler',
                    'level':'INFO',
                    'formatter':'json',
                },
            },
            'loggers':{
                '':{
                    'handlers':['info_file', 'error_file', 'warning_file', 'console'],
                    'level':'INFO',
                    'propagate':True,
                },
            },
        }

    @staticmethod
    def get_formatter():
        """Returns a JSON formatter for structured formatting."""
        def json_formatter(record):
            log_entry={
                'timestamp':record.created,
                'level':record.levelname,
                'name':record.name,
                'message':record.getMessage(),
            }
            if record.exc_info:
                log_entry['exception']= record.exc_info
                return json.dumps(log_entry)

            return json_formatter


class ContextLogger:
    """Adds contextual information to logs."""

    def __init__(
            self,
            logger:logging.Logger,
            context:dict
    ):
        self.logger= logger
        self.context= context

    def log(
            self,
            level:int,
            message:str,
            **kwargs
    ):
        """Logs a message with context."""
        extra= {**self.context, **kwargs}
        self.logger.log(level, message, extra=extra)