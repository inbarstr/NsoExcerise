from json import JSONEncoder


class Message:
    def __init__(self, application_id, session_id, message_id, participants, content):
        self.application_id = application_id
        self.session_id = session_id
        self.message_id = message_id
        self.participants = participants
        self.content = content

    def get_application_id(self):
        return self.application_id

    def get_session_id(self):
        return self.session_id

    def get_message_id(self):
        return self.message_id

    def get_participants(self):
        return self.participants

    def get_content(self):
        return self.content


class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
