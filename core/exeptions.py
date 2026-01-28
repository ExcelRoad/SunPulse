

class SolarMonitoringException(Exception):
    """Base exception for project"""
    pass


class APIAdapterException(SolarMonitoringException):
    """ Manufacturer API connection error """
    pass


class SyncException(SolarMonitoringException):
    """ Sync Process Error """
    pass


class AlertProcessingException(SolarMonitoringException):
    """ Alert Proccess Error """
    pass