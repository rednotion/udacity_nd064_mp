# main.py
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc

# for services
from sqlalchemy import create_engine, insert, select, MetaData, Table, String, Column, Integer
import psycopg2

# Shared variables
DBNAME = "geoconnections"
HOST = "postgres"
PORT = "5432"
USER = "ct_admin"
# PASSWORD = "d293aW1zb3NlY3VyZQ=="
PASSWORD = "wowimsosecure"
# init db
## dialect+driver://username:password@host:port/database
engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')

## for local testing
# engine = create_engine('postgresql://localhost:5432/postgres')

metadata = MetaData()
person_table = Table(
    'Person',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
    Column("company_name", String)
)


# Server
class PersonService(person_pb2_grpc.PersonEndpointServicer):
    def Create(self, request, context):
        print("request received")
        conn = psycopg2.connect(
            dbname="geoconnections",
            host="postgres",
            port="5432",
            user="ct_admin",
            password="db_password"
        )
        cursor = conn.cursor()
        print("curosr established")
        postgres_insert_query = """ INSERT INTO Person (ID, FIRST_NAME, LAST_NAME, COMPANY_NAME) VALUES (%s,%s,%s)"""
        record_to_insert = (
            request.first_name,
            request.last_name,
            request.company_name
        )
        cursor.execute(postgres_insert_query, record_to_insert)
        print("executed")

        # stmt = insert(person_table).values(
        #     first_name=request.first_name,
        #     last_name=request.last_name,
        #     company_name=request.company_name
        # )
        # with engine.connect() as conn:
        #     # print("connection estab")
        #     result = conn.execute(stmt)

        response = person_pb2.PersonRow(
            id=100, #result.inserted_primary_key[0],
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name
        )
        return response

    def Get(self, request, context):
        stmt = select([person_table]).where(person_table.c.id == request.id)
        with engine.connect() as conn:
            result = conn.execute(stmt)
        try:
            (rid, first_name, last_name, company_name) = result.first()
            response = person_pb2.PersonRow(
                id=rid,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name
            )
            return response
        except:
            print("ID not found")
            raise LookupError("ID not found in DB")

    def GetAll(self, request, context):
        list_of_person_rows = []
        stmt = select([person_table])
        with engine.connect() as conn:
            results = conn.execute(stmt)
        for row in results:
            (rid, first_name, last_name, company_name) = row
            person = person_pb2.PersonRow(
                id=rid,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name
            )
            list_of_person_rows.append(person)

        response = person_pb2.AllPersons(
            results=list_of_person_rows
        )
        return response


# Initialize grpc server
def serve():

    print("starting serve")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    person_pb2_grpc.add_PersonEndpointServicer_to_server(PersonService(), server)

    print("Server starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()


# psycopg versions
# conn = psycopg2.connect(
#     dbname="geoconnections",
#     host="postgres",
#     port="5432",
#     user="ct_admin",
#     password="d293aW1zb3NlY3VyZQ=="
# )
# cursor = conn.cursor()
# postgres_insert_query = """ INSERT INTO Person (ID, FIRST_NAME, LAST_NAME, COMPANY_NAME) VALUES (%s,%s,%s)"""
# record_to_insert = (
#     request.first_name,
#     request.last_name,
#     request.company_name
# )
# cursor.execute(postgres_insert_query, record_to_insert)
