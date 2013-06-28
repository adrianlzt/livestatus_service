from __future__ import absolute_import
try:  # pragma: no cover
    import ConfigParser
    configparser = ConfigParser
except ImportError:  # pragma: no cover
    import configparser


def get_current_configuration():
    configuration = Configuration(Configuration.DEFAULT_CONFIGURATION_FILE)
    return configuration


class Configuration(object):
    DEFAULT_CONFIGURATION_FILE = '/etc/livestatus.cfg'

    DEFAULT_LOG_FILE = '/var/log/livestatus-service.log'
    DEFAULT_LIVESTATUS_SOCKET = '/var/lib/nagios/rw/live'
    DEFAULT_ICINGA_COMMAND_FILE = '/usr/local/icinga/var/rw/icinga.cmd'

    OPTION_LOG_FILE = 'log_file'
    OPTION_LIVESTATUS_SOCKET = 'livestatus_socket'
    OPTION_ICINGA_COMMAND_FILE = 'icinga_command_file'

    SECTION = 'livestatus-service'

    def __init__(self, config_file_name):
        self._config_parser = configparser.RawConfigParser()
        self._load_config_file(config_file_name)
        self._verify_config()

    @property
    def log_file(self):
        return self._get_option(Configuration.OPTION_LOG_FILE, Configuration.DEFAULT_LOG_FILE)

    @property
    def livestatus_socket(self):
        return self._get_option(Configuration.OPTION_LIVESTATUS_SOCKET, Configuration.DEFAULT_LIVESTATUS_SOCKET)

    @property
    def icinga_command_file(self):
        return self._get_option(Configuration.OPTION_ICINGA_COMMAND_FILE, Configuration.DEFAULT_ICINGA_COMMAND_FILE)

    def _get_option(self, option, default_value=None):
        if not self._config_parser.has_option(Configuration.SECTION, option):
            if default_value:
                return default_value
            raise ValueError("Missing configuration option '%s' in section '%s", option, Configuration.SECTION)
        return self._config_parser.get(Configuration.SECTION, option)

    def _load_config_file(self, config_file_name):
        try:
            if self._config_parser.read(config_file_name) != [config_file_name]:
                raise ValueError("Failed to load config file '{0}'".format(config_file_name))
        except configparser.Error as e:
            raise ValueError('Error loading config file: {0}'.format(e))

    def _verify_config(self):
        if not self._config_parser.has_section(Configuration.SECTION):
            raise ValueError("Invalid config file: No such section '{0}'".format(Configuration.SECTION))
