x = ['poule', 'herisson']
questions = {}
questions['poule'] = 'poule'
questions['herisson'] = 'herisson'
def asking_questions(x):
    answers = {}
    for item in x:
        answer = 'dummy'
        while answer.lower() not in ['yes', 'no']:
            answer = raw_input(questions[item] + "\nyes/no: ")
            if answer.lower() not in ['yes', 'no']:
                print('Please enter [yes] or [no]')
        answers[item] = answer
    return answers
    
asking_questions(x)