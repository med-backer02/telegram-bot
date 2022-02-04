class Question:

    def __init__(self, test_id, q_id, question, answers, correct):

        if isinstance(answers, str):
            self.answers = list(answers[1:-1].split('","'))
            for i, answer in enumerate(self.answers):
                self.answers[i] = answer[:].strip('"')
                self.answers[i] = self.answers[i][:].strip("'")
        else:
            self.answers = answers
        self.correct = correct[:].strip('"')
        self.correct = self.correct[:].strip("'")

        self.test_id = test_id
        self.q_id = q_id
        self.text = question.strip('"')


class Test:

    def __init__(self, test_name):
        self.name = test_name


class User:
    def __init__(self, number_of_correct_answers, count_answers, questions, user_choice, test_name):
        self.number_of_correct_answers = number_of_correct_answers
        self.count_answers = count_answers
        self.number_of_wrong_answers = count_answers - number_of_correct_answers
        self.questions = questions
        self.user_choice = user_choice
        self.test_name = test_name

    def calculate(self):
        self.number_of_wrong_answers = self.count_answers - self.number_of_correct_answers