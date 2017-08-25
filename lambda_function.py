import json
import os
import requests

print('Loading function')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    #print("value1 = " + event['queryStringParameters']["foo"])
    #print("value2 = " + event['key2'])
    #print("value3 = " + event['key3'])
    #return event['queryStringParameters']["foo"]  # Echo back the first key value
    #raise Exception('Something went wrong')
    try:
        if(event['httpMethod'] == 'GET'):
            key = verifyFB(event['queryStringParameters'])
            if(key):
                return {"isBase64Encoded": False,
                "statusCode": 200,
                "body":key
                }
            else:
                return {"isBase64Encoded": False,
                "statusCode": 401,
                "body":"Verification Failed"
                }

        elif(event['httpMethod'] == 'POST'):
            res,msg = sendSimpleText(json.loads(event['body']))
            if(res==200):
                print("Message echoed back")
            else:
                print("Error while echoing back-",msg)
            return {"isBase64Encoded": False,
                    "statusCode": 200,
                    "body":"Message Echoed back"
                    }
    except Exception as ex:
        print("exception Occured-",ex)
        msg = "Exception occured"
    
    return {"isBase64Encoded": False,
    "statusCode": 200,
    "body":msg
    }

def verifyFB(data):
    if(data['hub.mode']=="subscribe" and data['hub.verify_token'] == os.environ['fb_token']):
        key = data['hub.challenge']
    else:
        key =''
    return key

def sendSimpleText(data):
    senderID = data['entry'][0]['messaging'][0]['sender']['id']
    if(senderID== os.environ['myID']):
        messageData = { "recipient": {"id": senderID},"message": {"text": data['entry'][0]['messaging'][0]['message']['text']}}
    else:
        messageData = { "recipient": {"id": senderID},"message": {"text": "I\'m not meant to serve you, Sorry :)"}}
    url = "https://graph.facebook.com/v2.6/me/messages?access_token={0}".format(os.environ['fb_token'])
    res = requests.post(url,json=messageData)
    return res.status_code,res.text