import grpc
import person_pb2
import person_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

channel = grpc.insecure_channel("localhost:30002")
stub = person_pb2_grpc.PersonEndpointStub(channel)


# print("Testing get all")
# empty = person_pb2.Empty()
# response = stub.GetAll(empty)
# print(response)

# print("Testing Retrieve")
# retrieve = person_pb2.PersonID(id=2)
# response = stub.Get(retrieve)
# print(response)

# print("Testing Retrieve -- Failed")
# retrieve = person_pb2.PersonID(id=3)
# response = stub.Get(retrieve)
# print(response)

print("Testing Create...")
item = person_pb2.PersonDetails(
    first_name="help",
    last_name="me",
    company_name="soon"
)
response = stub.Create(item)
print(response)