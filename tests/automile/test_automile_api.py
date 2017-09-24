import unittest

from automile.automile_api import AutomileAPI


class AutomileTests(unittest.TestCase):
    api = AutomileAPI(username="XX", password="XX",
                      api_client="xx.automile.com", api_secret="XX")

    def test_auth(self):
        pass

    def test_get_vehicle(self):
        # First create a query object for the trips class
        vehicle = self.api.vehicles.get("33553")
        self.assertTrue(vehicle.Make == "Audi")

    def test_list_vehicle(self):
        # First create a query object for the trips class
        qry = self.api.vehicles.query()
        # Set up some query parameters
        vehicles = qry.get_results()
        for vehicle in vehicles:
            self.assertTrue(vehicle.Make == "Audi")

    def test_create_vehicle(self):
        vehicle_data = {
            "NumberPlate": "ABC123",
            "Make": "Audi",
            "Model": "S4",
            "ModelYear": 2016,
            "BodyStyle": "Sedan",
            "OwnerContactId": 0,
            "OwnerCompanyId": 0,
            "CreateRelationshipToId": 0,
            "VehicleRelationshipType": 0
        }
        vehicle = self.api.vehicle.create(vehicle_data)

    def test_list_trips(self):
        qry = self.api.trips.query()
        # TODO required field
        qry.filter_field('lastNumberOfDays', '2')
        trips = qry.get_results()
        for trip in trips:
            print(trip)

    def test_list_trips_by_vehicleid(self):
        # First create a query object for the trips class
        qry = self.api.trips.query()
        # Set up some query parameters
        # TODO required field
        qry.filter_field('lastNumberOfDays', '2')
        trips = qry.get_results()
        for trip in trips:
            print(trip)

    def test_list_contacts(self):
        qry = self.api.contacts.query()
        contacts = qry.get_results()
        for contact in contacts:
            print(contact)
