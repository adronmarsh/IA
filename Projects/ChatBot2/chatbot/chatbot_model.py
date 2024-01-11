import random
import nltk
from nltk.chat.util import Chat, reflections

class SimpleChatbot:
    def __init__(self):
        self.set_pairs()
        self.chatbot = Chat(self.pairs, reflections)

    def set_pairs(self):
        self.pairs = [
            [
                r"hi|hello|hey",
                ["Hello!", "Hi there!", "Hey!"]
            ],
            [
                r"how are you?",
                ["I'm doing well, thank you.", "I am fine, how about you?"]
            ],
            [
                r"(.*)",
                ["I am not sure how to respond to that.", "Can you clarify?"]
            ],
        ]

    def respond(self, message):
        return self.chatbot.respond(message)

# Create an instance of the chatbot
chatbot_instance = SimpleChatbot()
