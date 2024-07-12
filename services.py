from flask import jsonify, session
from models import Question, Questionares, Answers, Choices, db

def get_users():
    questions = db.session.query(Question).all()
    data = []
    for question in questions:
        question_data = {
            'question_text': question.question_text,
            'rest': {
                'questionnaire': {
                    'title': question.questionare.title,
                    'description': question.questionare.description,
                    'topic': question.questionare.topic,
                    'total_audience': question.questionare.total_audience
                },
                'choices': [],
                'answers': []
            }
        }

        choices = db.session.query(Choices).filter(Choices.question_id == question.id).all()
        for choice in choices:
            question_data['rest']['choices'].append(choice.choice_text)

        answers = db.session.query(Answers).filter(Answers.question_id == question.id).all()
        for answer in answers:
            question_data['rest']['answers'].append(answer.answer)

        data.append(question_data)

    return jsonify(data)

def get_user(user_id):
    question = session.query(Question).filter(Question.questionnaire_id == user_id).all()
    question_data = {
        'question_text': question.question_text,
        'rest': {
            'questionnaire': {
                'title': question.questionare.title,
                'description': question.questionare.description,
                'topic': question.questionare.topic,
                'total_audience': question.questionare.total_audience
            },
            'choices': [],
            'answers':[]
        }
    }

    choices = db.session.query(Choices).filter(Choices.question_id == question.id).all()
    for choice in choices:
        question_data['rest']['choices'].append(choice.choice_text)

    answers = db.session.query(Answers).filter(Answers.question_id == question.id).all()
    for answer in answers:
         question_data['rest']['answers'].append({
            'email': answer.user.email,
            'name': answer.user.name,
            'answer': answer.answer
        })

    return jsonify(question_data)



def get_by_questioner_id(questoner_id):
    questionnaire = Questionares.query.get_or_404(questoner_id)
    
    # Initialize the main structure for the response
    response_data = {
        'questionnaire': {
            'title': questionnaire.title,
            'description': questionnaire.description,
            'topic': questionnaire.topic,
            'total_audience': questionnaire.total_audience,
            'zdata': {
                'questions': []  # Create a list to hold question data
            }
        }
    }

    # Fetch questions related to the questionnaire
    questions = questionnaire.questions
    # questions = db.session.query(Question).filter(Question.questionarie_id == questoner_id).all()
    
    for question in questions:
        question_data = {
            'question_text': question.question_text,
            'rest': {
                'choices': [],
                'answers': []
            }
        }
        
        # Fetch choices for the question
        choices = question.choices
        # choices = db.session.query(Choices).filter(Choices.question_id == question.id).all()
        for choice in choices:
            question_data['rest']['choices'].append(choice.choice_text)

        # Fetch answers for the question
        answers = question.answers
        # answers = db.session.query(Answers).filter(Answers.question_id == question.id).all()
        for answer in answers:
            question_data['rest']['answers'].append({
                'email': answer.user.email,
                'name': answer.user.name,
                'answer': answer.answer
            })
        
        # Append the question data to the questionnaire data
        response_data['questionnaire']['zdata']['questions'].append(question_data)
    return response_data