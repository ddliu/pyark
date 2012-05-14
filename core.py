import logging
ENTRY = 'pyark'

#logger
class ArkLogHandler(logging.Handler):
    def __init__(self, arklogger):
        logging.Handler.__init__(self)
        self.arklogger = arklogger

    def emit(self, record):
        for k in self.arklogger.handlers:
            self.arklogger.handlers[k](record)

class ArkLogger:
    """
    logger wrap
    """
    handlers = {}
    def __init__(self, name = ENTRY, format = None):
        self.logger = logging.getLogger(ENTRY)
        self.logger.setLevel(logging.DEBUG)
        arkloghandler = ArkLogHandler(self)
        arkloghandler.setLevel(logging.DEBUG)
        self.logger.addHandler(arkloghandler)
        if format is not None:
            self.setFormat(format)

    def __getattr__(self, attr):
        return getattr(self.logger, attr)

    def setHandler(self, name, handler):
        self.handlers[name] = handler

    def removeHandler(self, name = None):
        if name is None:
            self.handlers.clear()
        elif self.handlers.has_key(name):
            del(self.handlers[name])

    def setFormat(self, format):
        self.format = format
        self.formatter = logging.Formatter(format)

    def handlerEmpty(self, record):
        pass

    def handlerStream(self, record):
        print(self.formatter.format(record))

logger = ArkLogger(name = 'pyark', format = '[%(levelname)s] %(message)s')
logger.setHandler('stream', logger.handlerStream)

#registry
class Registry:
    def __init__(self, name = ENTRY):
        self.data = {}

    def get(self, name, default = None):
        if self.data.has_key(name):
            return self.data[name]
        else:
            return default

    def set(self, name, value):
        self.data[name] = value

registry = Registry()