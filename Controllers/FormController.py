from pymongo import ReturnDocument
import storage as st


def censusNight(formAnswerCollection, AnswerMembersCollection, formAnswerCollection_CN,
                AnswerMembersCollection_CN) -> tuple:
    messages = "Census Night Start "
    success = True
    formAnswerConfirm = formAnswerCollection.find(
        {'Confirmado': True})
    formAnswerCollection_CN.insert(formAnswerConfirm)
    formAnswerConfirmAux = formAnswerCollection_CN.find()
    aux = list(formAnswerConfirmAux)
    print(aux)
    for AnswerMember in aux:
        ECN = AnswerMember['ECN']
        CFN = AnswerMember['CFN']
        answer = AnswerMembersCollection.find(
            {'ECN': ECN, 'CFN': CFN}, {'_id': False})
        array = list(answer)
        print(array)

        if len(array) > 0:
            AnswerMembersCollection_CN.insert(array)
    return messages, success


def getFormByPeople(AnswerMembersCollection, data):
    Form = "null"
    try:
        Form = AnswerMembersCollection.find_one({
            'ECN': data['ECN'],
            'CFN': data['CFN']
        }, {'_id': False, 'ECN': False, 'CFN': False})
    except Exception as e:
        print(e)
    return Form


# Validar que traiga todo los campos de las preguntas


def insertAnswersPeople(AnswerMembersCollection, ECN, CFN, form) -> tuple:
    messages = ""
    success = False
    try:
        response = AnswerMembersCollection.find_one_and_update({
            'ECN': ECN,
            'CFN': CFN
        }, {

            '$set': {'questions': form['questions']}
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
    print((ECN, CFN, number))
    response = formAnswersCollection.find_one({
        'ECN': ECN,
        'CFN': CFN
    }, {'_id': False, 'seccion': {'$elemMatch': {'number': int(number)}}})
    if response:
        return response
    else:
        return None


def updateSection(formAnswersSection, CFN, ECN, number, form):
    message = ''
    success = False
    response = formAnswersSection.find_one_and_update({
        'ECN': ECN,
        'CFN': CFN
    }, {
        '$set': {
            'seccion.' + str(int(number) - 1) + '.respuestas': form
        }
    }, return_document=ReturnDocument.AFTER,
        projection={'_id': False},
        upsert=True)

    if response:
        message = 'Actualización hecha con éxito'
        success = True
    else:
        message = 'No se pudo actualizar el formulario'
        success = False

    return message, success


def getStatistics(formAnswersSection, code_collectors):
    response = formAnswersSection.find({})
    cnt = response.count()
    response = formAnswersSection.find({'Confirmado': False})
    cntp = response.count()

    confirmados = cnt - cntp
    noconfirmados = cntp

    response = code_collectors.find({})
    cnt = response.count()
    response = code_collectors.find({'entregado': False})
    cntp = response.count()

    entregados = cnt - cntp
    noentregados = cntp

    return {
        'confirmed_forms': confirmados,
        'no_confirmed_forms': noconfirmados,
        'delivered_forms': entregados,
        'no_delivered_forms': noentregados
    }


def confirmForm(formAnswersSection, ECN, CFN):
    response = formAnswersSection.find_one_and_update({
        'ECN': ECN,
        'CFN': CFN
    }, {
        '$set': {
            'Confirmado': True
        }
    }, return_document=ReturnDocument.AFTER,
        projection={'_id': False}
    )
    message = ""
    success = False
    if response:
        success = True
        message = "Formulario confirmado con éxito"
    else:
        success = False
        message = "No se ha podido confirmar el formulario"
    return message, success


def familyIdentifiers(ECN, CFN, AnswerMembersCollection):
    family_identifiers = (list(AnswerMembersCollection.find(
        {'ECN': ECN, 'CFN': CFN}, {'_id': False, 'idNumber': 1})))

    family_identifiersAux = []

    for faux in family_identifiers:
        family_identifiersAux.append(faux['idNumber'])

    return family_identifiersAux
