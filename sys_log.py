#!/usr/bin/env python

import sys
import logging.handlers
import syslog
import socket

""" Macro for print format """
__print_format__= "self.project_id + ' %(levelname)-9s +%(lineno)-4d %(message)s'"

class MYException (Exception):
    def __init__ (self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class MYSysLogHandler:
    """SysLog handler for write to syslog/Fire UDP log msgs"""

    my_logger = logging.getLogger("MYSysLogHandler")
    handler = []
    log_attribute  = {
        'debug'     : (logging.DEBUG, __print_format__),
        'info'      : (logging.INFO, __print_format__),
        'warning'   : (logging.WARNING, __print_format__),
        'error'     : (logging.ERROR, __print_format__),
        'critical'  : (logging.CRITICAL, __print_format__)}

    def __init__ (self, attribute_type, project_id, type_of_log):
        self.project_id     = project_id
        self.type_of_log    = type_of_log

        if attribute_type is "UDP_SYSLOG":
            self.attribute_type = attribute_type
        else:
            raise MYException("Invalid attribute_type: "+ attribute_type)
    
        self.log_level, self.log_format   = self.log_attribute[self.type_of_log]
        self.my_logger.setLevel(self.log_level)

        self.handler = logging.handlers.SysLogHandler (
        address =('localhost', logging.handlers.SYSLOG_UDP_PORT),
        facility=syslog.LOG_USER,
        socktype=socket.SOCK_DGRAM) 

        formatter = logging.Formatter(self.log_format)
        self.handler.setFormatter(formatter)
        self.my_logger.addHandler(self.handler)

    def debug(self, msg):
        self.my_logger.debug(msg)

    def info(self, msg):
        self.my_logger.info(msg)

    def warning(self, msg):
        self.my_logger.warning(msg)

    def error(self, msg):
        self.my_logger.error(msg)

    def critical(self, msg):
        self.my_logger.critical(msg)

    def __del__ (self):
        print "MYSysLogHandler cleared!"

if __name__ == '__main__':
    """ Main() """

    obj = None
    try:
        obj = MYSysLogHandler("UDP_SYSLOG", "My project", "debug")
    except:
        """ Generic error handler """
        e = sys.exc_info()[0]
        v = sys.exc_info()[1]
        print 'Error creating MYSysLogHandler: [%s] %s' %(e, v)
        exit ()

    obj.debug("Hello world | DEBUG")
    obj.info("Hello world | INFO")
    obj.warning("Hello world | WARNING")
    obj.error("Hello world | ERROR")
    obj.critical("Hello world | CRITICAL")

    del obj
    print "Everything Ends"
