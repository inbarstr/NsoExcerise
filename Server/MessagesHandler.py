import json
from Server.Message import MessageEncoder
from flask import abort


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MessagesHandler(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.application_messages = {}
        self.session_messages = {}
        self.messages = {}

    def add_message(self, message):
        if not self.messages.__contains__(message.get_message_id()):
            self.add_to_dictionary(self.application_messages, message.get_application_id(), message)
            self.add_to_dictionary(self.session_messages, message.get_session_id(), message)
            self.messages[message.get_message_id()] = message
        else:
            raise abort(409, "message_id = " + message.get_message_id() + " already exist")
        print("message added")

    def add_to_dictionary(self, my_dictionary, key, message):
        print("add_to_dictionary")
        if key not in my_dictionary:
            my_dictionary[key] = []
        my_dictionary[key].append(message)

    # return list of messages with the application_id
    def get_messages_by_application_id(self, application_id):
        print("get_messages_by_application_id")
        if self.application_messages.__contains__(int(application_id)):
            list_of_messages = self.application_messages[int(application_id)]
            json_list_of_messages = json.dumps(list_of_messages, cls=MessageEncoder)
            return json_list_of_messages
        else:
            abort(404, description="messages with application_id = " + application_id + " do not exist")

    # return list of messages with that session_id
    def get_messages_by_session_id(self, session_id):
        print("get_messages_by_session_id")
        if self.session_messages.__contains__(session_id):
            list_of_messages = self.session_messages[session_id]
            json_list_of_messages = json.dumps(list_of_messages, cls=MessageEncoder)
            return json_list_of_messages
        else:
            abort(404, description="messages with session_id = " + session_id + " do not exist")

    # return list with single message with the message_id
    def get_message_by_message_id(self, message_id):
        print("get_message_by_message_id")
        if self.messages.__contains__(message_id):
            message = self.messages[message_id]
            list_of_messages = [message]
            json_messages = json.dumps(list_of_messages, cls=MessageEncoder)
            return json_messages
        else:
            abort(404, description="message with message_id = " + message_id + " does not exist")

    # remove all messages with the application_id
    def delete_message_by_application_id(self, application_id):
        print("delete_message_by_application_id")
        if self.application_messages.__contains__(int(application_id)):
            messages_to_delete = self.application_messages[int(application_id)]
            self.delete_from_session_id(messages_to_delete)  # deleting from session_id dictionary
            self.delete_from_message_id(messages_to_delete)  # deleting from messages dictionary
            del self.application_messages[int(application_id)]  # deleting from application_id dictionary
        else:
            abort(404, description="messages with application_id = " + application_id + " do not exist, for removal")

    # remove all messages with the session_id
    def delete_message_by_session_id(self, session_id):
        print("delete_message_by_session_id")
        if self.session_messages.__contains__(session_id):
            messages_to_delete = self.session_messages[session_id]
            self.delete_from_application_id(messages_to_delete)  # deleting from application_id dictionary
            self.delete_from_message_id(messages_to_delete)  # deleting from messages dictionary
            self.session_messages.pop(session_id)  # deleting from session_id dictionary
        else:
            abort(404, description="messages with session_id = " + session_id + " do not exist, for removal")

    # remove single message with the message_id
    def delete_message_by_message_id(self, message_id):
        print("delete_message_by_message_id")
        if self.messages.__contains__(message_id):
            messages_to_delete = [self.messages[message_id]]
            self.delete_from_application_id(messages_to_delete)  # deleting from application_id dictionary
            self.delete_from_session_id(messages_to_delete)  # deleting from session_id dictionary
            self.messages.pop(message_id)
        else:
            abort(404, description="message with message_id = " + message_id + " does not exist, for removal")

    def delete_from_application_id(self, messages_to_delete):
        for message_to_delete in messages_to_delete:
            application_id = message_to_delete.get_application_id()
            list_of_application_id = self.application_messages[application_id]

            for message in list_of_application_id:
                if message.get_message_id() == message_to_delete.get_message_id():
                    message_to_remove = message

            list_of_application_id.remove(message_to_remove)

    def delete_from_session_id(self, messages_to_delete):
        for message_to_delete in messages_to_delete:
            session_id = message_to_delete.get_session_id()
            list_of_session_id = self.session_messages[session_id]

            for message in list_of_session_id:
                if message.get_message_id() == message_to_delete.get_message_id():
                    message_to_remove = message

            list_of_session_id.remove(message_to_remove)

    def delete_from_message_id(self, messages_to_delete):
        for message_to_delete in messages_to_delete:
            self.messages.pop(message_to_delete.get_message_id())