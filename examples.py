from automile_api import AutomileAPI


api = AutomileAPI(username="XX", password="XX", api_client="XX", api_secret="XX")

def example1(api):
    """List all trips
    """
    # First create a query object for the items class
    qry = api.items.query()
    # Set up some query parameters
    qry.filter_search('title', 'gadget')  # items with "gadget" in somewhere their title

    # print some status
