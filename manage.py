import psycopg2
import os
from psycopg2.extras import RealDictCursor
from sys import modules
from werkzeug.security import generate_password_hash

from instance.config import db_url, test_url


class DbSetup():
    def __init__(self):
        self.connection = None

    def createConnection(self):
        try:
            if "pytest" in modules:
                url = test_url
            if os.getenv("APP_SETTINGS") == "development":
                url = db_url
            self.connection = psycopg2.connect(url)
        except Exception:
            try:
                if os.getenv("APP_SETTINGS") == "production":
                    self.connection = psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")
            except Exception:
                res = "Database connection failed"
        self.connection.autocommit = True
        res = self.connection
        return res

    def createTables(self):
        cursor = self.createConnection().cursor(cursor_factory=RealDictCursor)

        table1 = """
                CREATE TABLE IF NOT EXISTS user_accounts(
                    user_id SERIAL PRIMARY KEY NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    other_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone_number VARCHAR(100) NOT NULL,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    registered TIMESTAMP with time zone DEFAULT ('now'::text)::date NOT NULL,
                    isAdmin BOOLEAN NOT NULL
                )
                """

        table2 = """
                CREATE TABLE IF NOT EXISTS meetups(
                    meetup_id SERIAL PRIMARY KEY NOT NULL,
                    createdOn TIMESTAMP with time zone DEFAULT ('now'::text)::date NOT NULL,
                    location VARCHAR(100) NOT NULL,
                    images VARCHAR(250) NOT NULL,
                    topic VARCHAR(100) NOT NULL,
                    happeningOn VARCHAR(100) NOT NULL,
                    tags VARCHAR(100) NOT NULL
                )
                """

        table3 = """
                CREATE TABLE IF NOT EXISTS questions(
                    question_id SERIAL PRIMARY KEY NOT NULL,
                    createdOn TIMESTAMP with time zone DEFAULT ('now'::text)::date NOT NULL,
                    createdBy INTEGER NOT NULL,
                    meetup_id INTEGER NOT NULL,
                    title VARCHAR(250) UNIQUE NOT NULL,
                    body VARCHAR(2000) UNIQUE NOT NULL,
                    votes INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (createdBy) REFERENCES user_accounts(user_id),
                    FOREIGN KEY (meetup_id) REFERENCES meetups(meetup_id)
                )
                """

        table4 = """
                CREATE TABLE IF NOT EXISTS rsvp(
                    rsvp_id SERIAL PRIMARY KEY NOT NULL,
                    meetup_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    response VARCHAR(50) NOT NULL,
                    FOREIGN KEY (meetup_id) REFERENCES meetups(meetup_id),
                    FOREIGN KEY (user_id) REFERENCES user_accounts(user_id)
                )
                """

        table5 = """
                CREATE TABLE IF NOT EXISTS comments(
                    comment_id SERIAL PRIMARY KEY NOT NULL,
                    question_id INTEGER NOT NULL,
                    title VARCHAR(250) NOT NULL,
                    body VARCHAR(2000) NOT NULL,
                    comment VARCHAR(2000) NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )
                """

        table6 = """
                CREATE TABLE IF NOT EXISTS blacklist(
                    token_id SERIAL PRIMARY KEY NOT NULL,
                    token VARCHAR(500) NOT NULL
                )
                """

        table7 = """
                CREATE TABLE IF NOT EXISTS votes(
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    votes varchar(10),
                    FOREIGN KEY (user_id) REFERENCES user_accounts(user_id),
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )
                """

        tables = [table1, table2, table3, table4, table5, table6, table7]
        for table in tables:
            cursor.execute(table)
        self.connection.commit()
        self.connection.close()

    def create_default_admin(self):
        cursor = self.createConnection().cursor(cursor_factory=RealDictCursor)
        pwd_hashed = generate_password_hash("admin1234")
        query = """
                SELECT * FROM user_accounts where isAdmin=%s
                """
        cursor.execute(query, (True,))
        default_admin = cursor.fetchone()
        if not default_admin:
            new_query = """
                        INSERT INTO user_accounts(first_name, last_name, other_name, email, phone_number, username, password, isAdmin)\
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                        """

            cursor.execute(new_query, ("Admin", "Admin", "Admin", "admin@questioner.com", "0745745745", "default_admin", pwd_hashed, True))
            self.connection.commit()
    
    def drop_tables(self):
        cursor = self.createConnection().cursor()
        query1 = """DROP TABLE IF EXISTS user_accounts CASCADE"""
        query2 = """DROP TABLE IF EXISTS meetups CASCADE"""
        query3 = """DROP TABLE IF EXISTS questions CASCADE"""
        query4 = """DROP TABLE IF EXISTS rsvp CASCADE"""
        query5 = """DROP TABLE IF EXISTS comments CASCADE"""
        query6 = """DROP TABLE IF EXISTS votes CASCADE"""
        query7 = """DROP TABLE IF EXISTS blacklist CASCADE"""

        queries = [query1, query2, query3, query4, query5, query6, query7]
        for query in queries:
            cursor.execute(query)
            self.connection.commit()