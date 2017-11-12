from flask import Flask
from flask_ask import Ask, statement, question, session,convert_errors
import json
import logging
from logging.handlers import RotatingFileHandler
import template as helper

app = Flask(__name__)
ask = Ask(app, "/riddle_for_kids")
app.config['ASK_VERIFY_REQUESTS'] = False

ANSWER=''
QUESTION=''
session_attributes = {}
session_attributes['isQuestionAsked']=False
session_attributes['ANSWER']=''
session_attributes['QUESTION']=''


@app.route('/')
def homepage():
    quiz_question=helper.get_quiz_map()
    s=""
    for k,v in quiz_question.items():
        s+=v+"<br/>"

    # QUESTION=quiz_question[0]
    # ANSWER=quiz_question[1]
    return s
    # return QUESTION +"</BR>Answer:"+ANSWER







@ask.launch
def start_skill():
    welcome_message = "Welcome to riddle kids," \
                        "Tell me start to start the quiz!" 
                        

    return question(welcome_message) \
     .reprompt("I didn't get that. Can you tell me the restaurant name again?")





@ask.intent("QuizIntent")
def start_intent():
    quiz_question=helper.get_question()
    session_attributes['QUESTION']=quiz_question[0]
    session_attributes['ANSWER']=quiz_question[1]
    session_attributes['isQuestionAsked']=True
    print "Question is:"+session_attributes['QUESTION']
    print "Answer is:"+session_attributes['ANSWER']
    return question(session_attributes['QUESTION'])

@ask.intent("AnswerIntent",mapping={'Answer':'Answer'})
def answer_intent(Answer):
    result=''
    isQuestionAsked=session_attributes['isQuestionAsked']
    ANSWER=session_attributes['ANSWER']
    QUESTION=session_attributes['QUESTION']
    print 'isQuestionAsked:'+str(isQuestionAsked)
    print 'User Answered:'+str(Answer)
    print 'Correct Answer:'+str(ANSWER)
    if isQuestionAsked:
        if Answer == ANSWER:
            result='Good Job! The answer is correct'
            session_attributes['isQuestionAsked']=False
        else:
            result='I am sorry the answer is wrong, the correct answer is '+ANSWER
    else:
        quiz_question=helper.get_question()
        QUESTION=quiz_question[0]
        ANSWER=quiz_question[1]
        print "Question is:"+QUESTION
        print "Answer is:"+ANSWER
    return statement(result).simple_card(title="Riddle Time", content=QUESTION+"\n"+ANSWER)
    
if __name__ == '__main__':

    app.run(debug=True)
