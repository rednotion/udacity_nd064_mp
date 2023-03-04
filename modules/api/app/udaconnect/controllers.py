from datetime import datetime

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService
from flask import request, current_app
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List
import json

# kafka & grpc
from app import g
import grpc
import app.udaconnect.person_pb2 as person_pb2
import app.udaconnect.person_pb2_grpc as person_pb2_grpc

# temporary
from kafka import KafkaConsumer
from app import db
from geoalchemy2.functions import ST_AsText, ST_Point

import logging
log = logging.getLogger('controllers.py')

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
        current_app.logger.info("request received")

        # location: Location = LocationService.create(request.get_json())

        # data = request.get_json()
        # current_app.logger.info(data)
        # new_location = Location()
        # current_app.logger.info("new location class created")
        # new_location.person_id = data["person_id"]
        # current_app.logger.info("person ID appended")
        # new_location.creation_time = datetime.strptime(data["creation_time"], "%Y-%m-%d %H:%M:%S")
        # current_app.logger.info("creation time")
        # new_location.coordinate = ST_Point(data["latitude"], data["longitude"])
        # current_app.logger.info("STpoint")

        # sample_response = request.get_json()
        # sample_response["id"] = 10
        # return sample_response  # location

        # post to kafka queue
        kafka_data = json.dumps(request.get_json())
        producer = g.kafka_producer
        producer.send("locations", value=kafka_data)
        current_app.logger.info("sent to kafka_producer")
        producer.flush()
        current_app.logger.info("flushed producer")

        # sample_response = request.get_json()
        # sample_response["id"] = 10
        # return sample_response  # location

        # kafka
        consumer = KafkaConsumer(
            "locations",
            bootstrap_servers="kafka:9092"
        )
        current_app.logger.info("loaded consumer")
        index = 0
        for message in consumer:
            current_app.logger.info(f"processing message {index}")
            # current_app.logger.info(message.value.decode('utf-8'))
            data = json.loads(message.value.decode('utf-8'))
            current_app.logger.info(data)
            current_app.logger.info(type(data))
            if type(data) == str:
                current_app.logger.info("data is string type")
                # data = dict(data)
            current_app.logger.info(data)
            current_app.logger.info(data["person_id"])
            new_location = Location()
            current_app.logger.info("new location class created")
            new_location.person_id = int(data["person_id"])
            current_app.logger.info("person ID appended")
            try:
                new_location.creation_time = data["creation_time"]
                current_app.logger.info("creation_time appended")
            except:
                datetime.strptime(data["creation_time"], "%Y-%m-%d %H:%M:%S")
                current_app.logger.info("had to convert")
            try:
                new_location.coordinate = ST_Point(data["latitude"], data["longitude"])
                current_app.logger.info("st point appended")
            except:
                current_app.logger.info("pass point")
            db.session.add(new_location)
            current_app.logger.info("added to db")
            db.session.commit()
            current_app.logger.info("commit to DB")

        return "exited"

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        current_app.logger.info("post person request received")
        payload = request.get_json()

        # grpc implementation
        payload = person_pb2.PersonDetails(
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            company_name=payload["company_name"]
        )

        channel = grpc.insecure_channel("grpc:5005")
        stub = person_pb2_grpc.PersonEndpointStub(channel)
        results = stub.Create(payload)

        current_app.logger.info("connections retrieved")
        current_app.logger.info(results)

        return results
        # new_person: Person = PersonService.create(payload)
        # return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        # grpc implementation
        channel = grpc.insecure_channel("grpc:30002")
        current_app.logger.info("connected to grpc channel")
        stub = person_pb2_grpc.PersonEndpointStub(channel)
        current_app.logger.info("initialized stub")
        payload = person_pb2.Empty()
        results = stub.GetConnections(payload)
        current_app.logger.info("connections retrieved")
        current_app.logger.info(results)

        # persons: List[Person] = PersonService.retrieve_all()
        return results


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


# @api.route("/persons/<person_id>/connection")
@api.route("/connections")
@api.param("person_id", "Given user ID", _in="query")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self) -> ConnectionSchema:
        person_id = int(request.args["person_id"])
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
