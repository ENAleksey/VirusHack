import datetime as dt
from fuzzywuzzy import fuzz


class Command:
    def __init__(self, action, required, optional, synonyms):
        self.pushable = True
        self.action = action
        self.required = required
        self.optional = optional
        self.synonyms = synonyms

    @staticmethod
    def get_eventID():
        timestamp = int(dt.datetime.now().timestamp())
        return "sco" + str(timestamp)

    def expand(self, synonyms):
        return Command(self.action,
                       self.required,
                       self.optional,
                       self.synonyms + synonyms)

    def get_message(self, **kwargs):
        required = {key: kwargs[key] for key in self.required}
        optional = {key: kwargs[key] for key in self.optional if key in kwargs}

        message = {
            "action": self.action,
            "eventId": self.get_eventID(),
            **required,
            **optional
        }

        return message

    def recognize(self, phrase):
        for word in self.synonyms:
            if fuzz.ratio(word, phrase) >= 80:
                return True
        return False


class StubCommand:
    def __init__(self, action, synonyms, data=None):
        self.pushable = False
        self.action = action
        self.synonyms = synonyms
        self.data = data

    def expand(self, synonyms):
        return StubCommand(self.action,
                           self.synonyms + synonyms)

    def get_message(self):
        return self.data

    def recognize(self, phrase):
        for word in self.synonyms:
            if fuzz.ratio(word, phrase) >= 80:
                return True
        return False


addItem = Command('addItem',
                  ['itemCode'],
                  ['quantity'],
                  ['добавить', 'добавьте', 'добавь'])

addLoyalty = Command('addLoyalty',
                     ['itemCode'],
                     ['type'],
                     ['???'])


cancel = Command('cancel',
                 [],
                 [],
                 ['отменить', 'назад'])


start = StubCommand('start', ['начать', 'запуск', 'старт', 'начнем'])


