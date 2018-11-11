from pymongo import ReturnDocument


def getFormByPeople(AnswerMembersCollection, data):
    Form = "null"
    try:
        Form = AnswerMembersCollection.find_one({
            'ECN': data.ECN,
            'CFN': data.CFN,
            'idNumber': data.idNumber
        }, {'_id': False})
    except Exception as e:
        print(e)
    return Form

# Validar que traiga todo los campos de las preguntas


def insertAnswersPeople(AnswerMembersCollection, ECN, CFN, idNumber, form) -> tuple:
    messages = ""
    success = False
    print(ECN)
    try:
        response = AnswerMembersCollection.find_one_and_update({
            'ECN': ECN,
            'CFN': CFN,
            'idNumber': idNumber
        }, {
            '$set': form
        },
            projection={'_id': False},
            upsert=True,
            return_document=ReturnDocument.AFTER)
        if response:
            success = True
    except Exception as e:
        print(e)
        messages = str(e)
    else:
        success = True
        messages = 'responses of the person recorded successfully'
    return messages, success


def findSection(formAnswersCollection, ECN, CFN, number):
    response = formAnswersCollection.find_one({
        'ECN': ECN,
        'CFN': CFN
    }, {'_id': False, 'seccion': {'$elemMatch': {'number': int(number)}}})
    print(response)
    if response:
        return response
    else:
        return None


def updateSection(formAnswersSection, CFN, ECN, number, form):
    response = formAnswersSection.find_one_and_update({
        'ECN': ECN,
        'CFN': CFN
    }, {
        '$set': form
    }, return_document=ReturnDocument.AFTER,
        projection={'_id': False})
    if response:
        return response
    else:
        return None
