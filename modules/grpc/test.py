import grpc
import person_pb2
import person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = person_pb2_grpc.PersonEndpointStub(channel)

# Update this with desired payload
item = person_pb2.PersonDetails(
	first_name="help",
	last_name="me",
	company_name="soon"
)


response = stub.Create(item)
print(response)