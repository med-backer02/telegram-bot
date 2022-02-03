import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
import app.config as config

class Psycho:

    def __init__(self):
        # self.connection = psycopg2.connect(dbname=config.dbname, user=config.user,
        #                        password=config.password, host=config.host)
        self.connection = psycopg2.connect(config.DB_URL, sslmode="require")

        self.cursor = self.connection.cursor()

    def create_bd_for_tests(self):
        # self.cursor.execute("""CREATE TABLE IF NOT EXISTS Tests(
        #                                     id SERIAL PRIMARY KEY,
        #                                     name VARCHAR(255) NOT NULL,
        #                                     file_id BIGINT NOT NULL
        #                                     );""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Tests(
                                                id SERIAL PRIMARY KEY,
                                                name VARCHAR(255) NOT NULL UNIQUE
                                                );""")
        self.connection.commit()

    def create_bd_for_questions(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Questions(
                                                t_id SERIAL,
                                                q_number SERIAL,
                                                question VARCHAR(255) NOT NULL,
                                                q_options text NOT NULL, 
                                                q_answer text NOT NULL,
                                                PRIMARY KEY (t_id,q_number),
                                                FOREIGN KEY (t_id) REFERENCES Tests
                                                );""")
        self.connection.commit()

    def filling_in_tests_bd(self, tests):
        """

        :param tests: List
        :return:
        """
        for test in tests:
            try:
                self.cursor.execute("INSERT INTO Tests(name) VALUES(%s);", (test.name,))
            except Exception as e:
                print("log:ERROR in filling_in_tests_bd")
                print("Exception",e)

        self.connection.commit()

    def get_test_id(self, test_name):
        self.cursor.execute("SELECT id FROM Tests WHERE name=%s",(test_name,))
        test_id = self.cursor.fetchone()
        return test_id


    def filling_in_questions_bd(self, questions):
        """

        :param questions: List
        :return:
        """
        for question in questions:
            self.cursor.execute("INSERT INTO Questions VALUES(%s, %s, %s, %s, %s);",
                                (question.test_id, question.q_id, question.text, question.answers, question.correct))
        self.connection.commit()

    def get_id_and_name_from_bd(self):
        self.cursor.execute("SELECT id,name FROM Tests")
        tests_id_and_name = self.cursor.fetchall()
        return tests_id_and_name

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.cursor.close()
        self.connection.close()

if __name__=="__main__":
    database = Psycho()


    print(database.get_id_and_name_from_bd())


    database.close()

