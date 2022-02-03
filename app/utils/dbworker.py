import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
import app.config as config
from app.utils.question_and_tests import Question

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

    def get_tests_id_and_name_from_bd(self):
        self.cursor.execute("SELECT id,name FROM Tests")
        tests_id_and_name = self.cursor.fetchall()
        return tests_id_and_name


    def filling_in_questions_bd(self, questions):
        """

        :param questions: List
        :return:
        """
        for question in questions:
            self.cursor.execute("INSERT INTO Questions VALUES(%s, %s, %s, %s, %s);",
                                (question.test_id, question.q_id, question.text, question.answers, question.correct))
        self.connection.commit()

    def get_question_from_bd(self,test_id, offset=0, limit=5):
        self.cursor.execute("SELECT t_id, q_number, question, q_options, q_answer FROM Questions "
                            "WHERE t_id = %s"
                            "ORDER BY random()"
                            "OFFSET %s"
                            "LIMIT %s",(test_id, offset, limit))
        questions = self.cursor.fetchall()
        return questions

    def close(self):
        """ Закрываем текущее соединение с БД """
        #self.cursor.close()
        self.connection.close()

if __name__=="__main__":
    database = Psycho()


    question_db = database.get_question_from_bd(1)
    questions_response=[]
    for q in question_db:
        t_id, q_number, question, q_options, q_answer = q
        q_class=Question(t_id, q_number, question, q_options, q_answer)
        questions_response.append(q_class)

    print(questions_response)
    database.close()
