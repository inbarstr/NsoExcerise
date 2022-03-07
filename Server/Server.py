from flask import Flask, request, abort
from Server.Message import Message
from Server.MessagesHandler import MessagesHandler

messages_handler = MessagesHandler()

app = Flask(__name__)


# api = App(app)
# api.run()

@app.route('/')
def hello():
    return "hello"


@app.route('/AddMessage', methods=['POST'])
def AddMessage():
    print("Api AddMessage has started")
    # messages_dict = json.loads(request.json)
    # message = Message(**messages_dict)
    added = False
    if request.json is not None:
        messages_dict = request.json
        message = Message(messages_dict["application_id"], messages_dict["session_id"], messages_dict["message_id"],
                          messages_dict["participants"], messages_dict["content"])
        messages_handler.add_message(message)
        added = True
    print("Api AddMessage has finished")
    if added:
        return '200'
    else:
        abort(500, description="request.args is incorrect")


@app.route('/GetMessage', methods=['GET'])
def GetMessage():
    messages = None
    if len(request.args) == 0 or len(request.args) > 1:
        abort(500, description="request.args is incorrect")
    if request.args.__contains__("applicationId"):
        messages = messages_handler.get_messages_by_application_id(request.args["applicationId"])
    if request.args.__contains__("sessionId"):
        messages = messages_handler.get_messages_by_session_id(request.args["sessionId"])
    if request.args.__contains__("messageId"):
        messages = messages_handler.get_message_by_message_id(request.args["messageId"])
    print("Api GetMessage has finished")
    if messages is not None:
        return messages
    else:
        abort(500, description="request.args is incorrect")


@app.route('/DeleteMessage', methods=['DELETE'])
def DeleteMessage():
    if len(request.args) == 0 or len(request.args) > 1:
        abort(500, description="request.args is incorrect")
    deleted = False
    if request.args.__contains__("applicationId"):
        messages_handler.delete_message_by_application_id(request.args["applicationId"])
        deleted = True
    if request.args.__contains__("sessionId"):
        messages_handler.delete_message_by_session_id(request.args["sessionId"])
        deleted = True
    if request.args.__contains__("messageId"):
        messages_handler.delete_message_by_message_id(request.args["messageId"])
        deleted = True
    print("Api DeleteMessage has finished")
    if deleted:
        return '200'
    else:
        abort(500, description="request.args is incorrect")
