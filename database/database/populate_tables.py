from faker import Faker
from sqlalchemy import create_engine, MetaData
from hashlib import sha256
import os
import pg8000
from google.cloud.sql.connector import Connector, IPTypes
from dotenv import load_dotenv


class GenerateData:
    faker = Faker("pt_BR")
    if os.getenv("ENV") == "dev":
        engine = create_engine("postgresql://postgres:postgres@localhost:5432/fakedata")
        metadata = MetaData()
    elif os.getenv("ENV") == "prd":
        def get_conn() -> pg8000.dbapi.Connection:
            project_id = os.getenv("PROJECT_ID", "")
            region = os.getenv("REGION", "southamerica-east1")
            instance = os.getenv("INSTANCE", "apoena-database")
            instance_connection_name = f"{project_id}:{region}:{instance}"
            db_user = os.getenv("DB_USER", "")
            db_pass = os.getenv("DB_PASS", "")
            db_name = os.getenv("DB_NAME", "")

            ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

            connector = Connector(ip_type)

            conn = connector.connect(
                instance_connection_name,
                "pg8000",
                user=db_user,
                password=db_pass,
                db=db_name
            )
            return conn

        load_dotenv()

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('SA_KEYFILE')
        engine = create_engine("postgresql+pg8000://", creator=get_conn)

        # Create a metadata object
        metadata = MetaData()

    def __init__(self, table_name, n_records) -> None:
        self.table_name = table_name
        self.n_records_to_generate = n_records

        with self.engine.connect() as conn:
            self.metadata.reflect(conn)

    def create_data(self):
        if self.table_name not in self.metadata.tables.keys():
            return print(f"{self.table_name} does not exist")

        if self.table_name == "customers":
            with self.engine.begin() as conn:
                for _ in range(self.n_records_to_generate):
                    fake_customer_to_insert = self.__insert_fake_customer()
                    conn.execute(fake_customer_to_insert) 

    def __insert_fake_customer(self):
        table = self.metadata.tables[self.table_name]

        insert_command = table.insert().values(
            cd_customer=sha256(self.faker.cpf().encode("utf8")).hexdigest(),
            nm_customer=self.faker.name(),
            st_email=self.faker.email(),
            st_phone=self.faker.phone_number(),
            sg_state=self.faker.state()[0],
            dt_birth=self.faker.date_of_birth(minimum_age=18,
                                              maximum_age=80)
        )

        return insert_command


if __name__ == "__main__":
    generate_data = GenerateData("customers", 100)
    generate_data.create_data()
