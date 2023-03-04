from datetime import datetime

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
import json
from geoalchemy2.functions import ST_AsText, ST_Point

from app import g logger

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    # @responds(schema=LocationSchema)
    def post(self) -> Location:
        # request.get_json() # why is this useless get json here
        logger.info("request received")

        # location: Location = LocationService.create(request.get_json())

        data = request.get_json()
        logger.info(data)
        new_location = Location()
        logger.info("new location class created")
        new_location.person_id = data["person_id"]
        logger.info("person ID appended")
        new_location.creation_time = datetime.strptime(data["creation_time"], "%Y-%m-%d %H:%M:%S")
        logger.info("creation time")
        new_location.coordinate = ST_Point(data["latitude"], data["longitude"])
        logger.info("STpoint")
        return "works!"

        # sample_response = request.get_json()
        # sample_response["id"] = 10
        # return sample_response  # location

        # # post to kafka queue
        # kafka_data = json.dumps(request.get_json())
        # producer = g.kafka_producer
        # producer.send("locations", value=kafka_data)
        # producer.flush()

        # sample_response = request.get_json()
        # sample_response["id"] = 10
        # return sample_response  # location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
