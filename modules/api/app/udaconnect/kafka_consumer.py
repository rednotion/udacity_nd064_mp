from kafka import KafkaConsumer
from app.udaconnect.services import LocationService
from app.udaconnect.schemas import LocationSchema

TOPIC_NAME = 'locations'

consumer = KafkaConsumer(TOPIC_NAME)
for message in consumer:
    # save locations to DB
    location: Location = LocationService.create(request.get_json())
    print(location)