# Standard library imports
import collections
import inspect

# Local imports
from uplink import interfaces, utils


def get_api_definitions(service):
    """
    Returns all attributes with type
    `uplink.interfaces.RequestDefinitionBuilder` defined on the given
    class.

    Note:
        Only attributes defined directly on the class are considered. In
        other words, inherited `RequestDefinitionBuilder` attributes
        are ignored.

    Args:
        service: A class object.
    """
    predicate = interfaces.RequestDefinitionBuilder.__instancecheck__
    definitions = inspect.getmembers(service, predicate)
    local_members = service.__dict__
    return [(k, v) for k, v in definitions if k in local_members]


class RequestBuilder(object):
    def __init__(self, converter_registry):
        self._method = None
        self._uri_builder = None
        self._return_type = None
        self._info = collections.defaultdict(dict)
        self._converter_registry = converter_registry

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        self._method = method

    @property
    def uri(self):
        return self._uri_builder

    @uri.setter
    def uri(self, uri):
        self._uri_builder = utils.URIBuilder(uri)

    @property
    def info(self):
        return self._info

    def get_converter(self, converter_key, *args, **kwargs):
        return self._converter_registry[converter_key](*args, **kwargs)

    def set_return_type(self, return_type):
        self._return_type = return_type

    def build(self):
        # TODO: Should we assert that all URI variables are set?
        # assert not self._uri_builder.remaining_variables():
        return utils.Request(
            self._method,
            self._uri_builder.build(),
            self._info,
            self._return_type
        )
