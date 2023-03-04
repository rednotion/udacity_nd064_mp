# main.py
from concurrent import futures

import grpc
import person_pb2
import person_pb2_grpc
import time

# for services
import psycopg2
from sqlalchemy import create_engine, insert, MetaData, Table, String, Column, Integer

# Server
class PersonService(person_pb2_grpc.PersonEndpointServicer):
    def Create(self, request, context):
        # init db
        # conn = psycopg2.connect(
        #     dbname="geoconnections",
        #     host="postgres",
        #     port="5432",
        #     user="ct_admin",
        #     password="d293aW1zb3NlY3VyZQ=="
        # )
        DBNAME = "geoconnections"
        HOST = "postgres"
        PORT = "5432"
        USER = "ct_admin"
        PASSWORD = "d293aW1zb3NlY3VyZQ=="
        # conn = psycopg2.connect(
        #     dbname="postgres",
        #     host="postgresql://localhost",
        #     port="5432",
        #     user="elizabethlim",
        # )
        # dialect+driver://username:password@host:port/database
        # engine = create_engine('postgresql://127.0.0.1:5432/postgres')
        engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')
        metadata = MetaData()
        person_table = Table(
            'Person',
            metadata,
            Column("id", Integer, primary_key=True),
            Column("first_name", String),
            Column("last_name", String),
            Column("company_name", String)
        )

        print(metadata)
        stmt = insert(person_table).values(
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name
        )
        print(stmt)
        with engine.connect() as conn:
            print("connection estab")
            result = conn.execute(stmt)
            conn.commit()
            print(result)

        # cursor = conn.cursor()
        # postgres_insert_query = """ INSERT INTO Person (ID, FIRST_NAME, LAST_NAME, COMPANY_NAME) VALUES (%s,%s,%s)"""
        # record_to_insert = (
        #     request.first_name,
        #     request.last_name,
        #     request.company_name
        # )
        # cursor.execute(postgres_insert_query, record_to_insert)
        # conn.commit()

        # new_person = Person()
        # new_person.first_name = request["first_name"]
        # new_person.last_name = request["last_name"]
        # new_person.company_name = request["company_name"]

        # db.session.add(new_person)
        # db.session.commit()

        response = person_pb2.PersonRow(
            id=999,
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name
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