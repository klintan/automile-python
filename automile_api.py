import oauth2client

class AutomileAPI():
    """Pseudo-connection to the Automile v1 API
       Objects of this class provide a call interface to the Automile
       v1 HTTP API.
       API based on Billograms API SDK and Automile PHP SDK.
       """
    def __init__(self, password, username, apiclient, apisecret):
        self._password = password
        self._username = username
        self._apiclient = apiclient
        self._apisecret = apisecret



    @property
    def vehicles(self):
        "Provide access to the vehicles database"
        if self._items is None:
            self._items = SimpleClass(self, 'item', 'item_no')
        return self._items



class SimpleClass():
    """Represents a collection of remote objects on the Automile service
    Provides methods to search, fetch and create instances of the object type.
    See the online documentation for the actual structure of remote objects.
    """
    _object_class = SimpleObject

    def __init__(self, api, url_name, object_id_field):
        self._api = api
        self._url_name = url_name
        self._object_id_field = object_id_field

    def _url_of(self, obj=None, obj_id=None):
        if obj_id is None:
            obj_id = obj[self._object_id_field]
        return '{}/{}'.format(self.url_name, obj_id)

    @property
    def url_name(self):
        return self._url_name

    @property
    def api(self):
        return self._api

    def query(self):
        "Create a query for objects of this type"
        return Query(self)

    def get(self, object_id):
        "Fetch a single object by its identification"
        resp = self.api.get(self._url_of(obj_id=object_id))
        return self._object_class(self.api, self, resp['data'])

    def create(self, data):
        "Create a new object with the given data"
        resp = self.api.post(self.url_name, data)
        return self._object_class(self.api, self, resp['data'])





class SingletonObject():
    """Represents a remote singleton object on Automile
    Implements __getattr__ for dict-like access to the data of the remote
    object, or use the 'data' property to access the backing dict object.
    The data in this dict and all sub-objects should be treated as read-only,
    the only way to change the remote object is through the 'update' method.
    The represented object is initially "lazy" and will only be fetched on the
    first access. If the remote data are changed, the local copy can be updated
    by the 'refresh' method.
    See the online documentation for the actual structure of remote objects.
    """
    def __init__(self, api, url_name):
        self._api = api
        self._object_class = url_name
        self._data = None

    __slots__ = ('_api', '_object_class', '_data')

    def __getitem__(self, key):
        "Dict-like access to object data"
        return self.data[key]

    def __repr__(self):
        return _printable_repr(
            "<Automile object '{}'{}>".format(
                self._url,
                (self._data is None) and ' (lazy)' or ''
            )
        )

    @property
    def _url(self):
        return self._object_class

    @property
    def data(self):
        "Access the data of the actual object"
        if self._data is None:
            self.refresh()
        return self._data

    def refresh(self):
        "Refresh the local copy of the object data from remote"
        resp = self._api.get(self._url)
        self._data = resp['data']
        return self

    def update(self, data):
        "Modify the remote object with a partial or complete structure"
        resp = self._api.put(self._url, data)
        self._data = resp['data']
        return self

class SimpleObject(SingletonObject):
    """Represents a remote object on the Automile service
    Implements __getattr__ for dict-like access to the data of the remote
    object, or use the 'data' property to access the backing dict object.
    The data in this dict and all sub-objects should be treated as read-only,
    the only way to change the remote object is through the 'update' method.
    If the remote data are changed, the local copy can be updated by
    the 'refresh' method.
    The 'delete' method can be used to remove the backing object.
    See the online documentation for the actual structure of remote objects.
    """
    def __init__(self, api, object_class, data):
        self._api = api
        self._object_class = object_class
        self._data = data

    __slots__ = ()

    @property
    def _url(self):
        return self._object_class._url_of(self)

    def __getattr__(self, key):
        return self._data[key]

    def delete(self):
        "Remove the remote object from the database"
        self._api.delete(self._url)
        return None

class Query(object):
    """Builds queries and fetches pages of remote objects
    """
    def __init__(self, type_class):
        self._type_class = type_class
        self._filter = {}
        self._count_cached = None
        self._page_size = 100
        self._order = {}

    def _make_query(self, page_number=1, page_size=None):
        query_args = {
            'page_size': page_size or self._page_size,
            'page': page_number,
        }
        query_args.update(self._get_queryargs())
        resp = self._type_class.api.get(self._type_class._url_name, query_args)
        self._count_cached = resp['meta']['total_count']
        return resp

    def _get_queryargs(self):
        args = {}
        args.update(self.filter)
        args.update(self.order)
        return args

    @property
    def count(self):
        """Total amount of objects matched by the current query, reading this
        may cause a remote request"""
        if self._count_cached is None:
            # make a query for a single result,
            # this will update the cached count
            self._make_query(1, 1)
        return self._count_cached

    @property
    def total_pages(self):
        """Total number of pages required for all objects based on current
        pagesize, reading this may cause a remote request"""
        return (self.count + self.page_size - 1) // self.page_size

    @property
    def page_size(self):
        "Number of objects to return per page"
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        value = int(value)
        assert value >= 1
        self._page_size = value
        return self

    @property
    def filter(self):
        "Filter to apply to query"
        return self._filter

    @filter.setter
    def filter(self, value):
        if value == self._filter:
            return
        if value:
            assert 'filter_type' in value and \
                'filter_field' in value and \
                'filter_value' in value
            assert value['filter_type'] in (
                'field',
                'field-prefix',
                'field-search',
                'special'
                )
            self._filter = dict(value)
        else:
            self._filter = {}
        self._count_cached = None
        return self

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        if value:
            assert 'order_field' in value and 'order_direction' in value
            assert value['order_direction'] in ('asc', 'desc')
            self._order = dict(value)
        else:
            self._order = {}
        return self

    def make_filter(self, filter_type=None, filter_field=None,
                    filter_value=None):
        if None in (filter_type, filter_field, filter_value):
            self.filter = {}
        else:
            self.filter = {
                'filter_type': filter_type,
                'filter_field': filter_field,
                'filter_value': filter_value
            }
        return self

    def remove_filter(self):
        "Remove any filter currently set"
        self.filter = {}
        return self

    def filter_field(self, filter_field, filter_value):
        "Filter on a basic field, look for exact matches"
        return self.make_filter('field', filter_field, filter_value)

    def filter_prefix(self, filter_field, filter_value):
        "Filter on a basic field, look for prefix matches"
        return self.make_filter('field-prefix', filter_field, filter_value)

    def filter_search(self, filter_field, filter_value):
        "Filter on a basic field, look for substring matches"
        return self.make_filter('field-search', filter_field, filter_value)

    def filter_special(self, filter_field, filter_value):
        "Filter on a special query"
        return self.make_filter('special', filter_field, filter_value)

    def search(self, search_terms):
        "Filter by a full data search (exact meaning depends on object type)"
        return self.make_filter('special', 'search', search_terms)

    def get_page(self, page_number):
        "Fetch objects for the one-based page number"
        resp = self._make_query(int(page_number))
        return [
            self._type_class._object_class(
                self._type_class.api,
                self._type_class,
                o
            ) for o in resp['data']
        ]

    def iter_all(self):
        "Iterate over all matched objects"
        # make a copy of ourselves so parameters can't be changed behind
        # our back
        import copy
        qry = copy.copy(self)
        # iterate over every object on every page
        for page_number in range(1, qry.total_pages+1):
            page = qry.get_page(page_number)
            for obj in page:
                yield obj


# just the AutomileAPI class and the exceptions are really part
# of the call API of this module
__all__ = ['AutomileAPI']
