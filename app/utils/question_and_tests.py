class Question:

    def __init__(self, test_id, q_id, question, answers, correct):
        self.test_id = test_id
        self.q_id = q_id
        self.text = question
        self.answers = answers
        self.correct = correct


class Test:

    def __init__(self, test_name):
        self.name = test_name
    
