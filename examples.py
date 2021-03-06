from automile.automile_api import AutomileAPI

api = AutomileAPI(username="xx", password="xx",
                  api_client="xx.automile.com", api_secret="xx")

def example0():
    """ Create a test user in automile to get credentials
    :return:
    """
    pass


def example1(api):
    """List all trips
    """
    # First create a query object for the trips class
    qry = api.trips.query()
    # Set up some query parameters
    qry.filter_field('title', 'gadget')  # items with "gadget" in somewhere their title

    # print some status


def example2(api):
    """Get vehicle by id
    """
    vehicle_id = 12345
    try:
        vehicle = api.vehichles.get(vehicle_id)
    except Exception as e:
      print(e)
    # print some status

