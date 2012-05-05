import logging

#logger
logger = logging.getLogger('pyark')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#registry
registry = {}
def register(k, v):
    registry[k] = v

def get_registry(k):
    return registry.has_key(k) and registry[k] or None