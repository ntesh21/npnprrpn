import sqlite3
import json
from functions.sqlquery import sql_delete
intent=''
query=''
response=''
check_presence=0
existing_intents=[]



def data_prepare():
    print(" iam fine")
    global intent
    global query
    global response
    global check_presence
    global existing_intents
    conn=sqlite3.connect('./datasets/user_log.db')
    qry = "Select intent, query, reply From dataset Order By intent, query, reply"
    # Assumes conn is a database connection.
    cursor = conn.cursor()
    cursor.execute(qry)
    rows = [x for x in cursor]
    cols = [x[0] for x in cursor.description]
    #data = []
    header=[]
    values=[]
    intention=[]
    question=[]
    answer=[]


    for row in rows:
        data = {}
        for prop, val in zip(cols, row):
            header.append(prop)
            values.append(val)

    for head,value in zip(header,values):
        #print(head)
        if head=='intent':
            intention.append(value)
            print(intent)
        elif head=='query':
            question.append(value)
            #print("i am qery",query)
        elif head=='reply':
            answer.append(value)
            #print(response)



    for user_intent,user_query,bot_reply in zip(intention,question,answer):

        with open('nrn.json', mode='r', encoding='UTF-8') as feedsjson:
            feeds = json.load(feedsjson)
            list_data = ((feeds['intents']))
            print(list_data)

            for intents in list_data:
                if intents['intent'] not in existing_intents:
                    existing_intents.append(intents['intent'])
                else:
                    continue
            if user_intent in existing_intents:
                print("iam in")
                for intents in list_data:
                    if user_intent== intents['intent']:
                        qstn=[w for w in [user_query] if w not in intents['query']]
                        rep=[x for x in [bot_reply] if x not in intents['response']]
                        try:
                            intents['query'].append(qstn[0])
                        except:
                            print("query already present in the dataset")

                        try:
                            intents['response'].append(rep[0])
                            # print(intents['response'])
                        except:
                            print("response already present")

                        matched_content = {'intents': feeds['intents']}
                        print(matched_content)
                        with open('nrn.json', 'w')as file:
                            json.dump(matched_content, file)
                        sql_delete(''' DELETE FROM dataset where query = ? and reply = ?''', (user_query,bot_reply))




                    else:
                        continue
            else:
                entry={'intent':user_intent,'query':[user_query],'response':[bot_reply]}
                list_data.append(entry)
                content={'intents':list_data}
                with open('nrn.json', 'w')as file:
                    json.dump(content, file)
                sql_delete(''' DELETE FROM dataset where query = ? and reply = ?''', (user_query, bot_reply))
            print(existing_intents)


    return 0

