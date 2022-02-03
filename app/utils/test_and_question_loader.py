from app.utils import dbworker
from app.utils.question_and_tests import Question

def get_tests_name():
    TESTS=[]

    psql = dbworker.Psycho()
    tests_id_and_name = psql.get_tests_id_and_name_from_bd()
    psql.close()

    for test_id_and_name in tests_id_and_name:
        test_name = test_id_and_name[1]
        TESTS.append(test_name)

    return TESTS

def get_questions(test_id, offset, limit):
    psql = dbworker.Psycho()
    questions = psql.get_question_from_bd(test_id, offset=offset, limit = limit)
    psql.close()
    questions_response=[]

    for question in questions:
        t_id, q_number, question, q_options, q_answer = question
        q_class=Question(t_id, q_number, question, q_options, q_answer)
        questions_response.append(q_class)

    return questions_response

if __name__=="__main__":
    print(get_questions(1))