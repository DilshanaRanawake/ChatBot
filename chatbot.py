!pip install spacy
!python -m spacy download en_core_web_sm

import random
import spacy

class ChatBot:
    ### Potential Negative Responses
    negative_responses = ("no", "nope", "nah", "not a chance", "sorry")
    ### Exit Conversation Keywords
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    ### Random starter questions
    random_questions = (
        "What brings you here today? ",
        "Tell me a bit about yourself. ",
        "What do you enjoy doing in your free time? ",
        "What's your favorite book or movie? ",
        "Do you have any hobbies? ",
        "What's your favorite place to visit? ",
        "What technology do you find fascinating? "
    )

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.conversation_patterns = {
            'describe_place_intent': r'describe.*place',
            'answer_why_intent': r'why.*are',
            'about_book_movie': r'harry potter|book|movie|film',
            'about_session': r'.*session'
        }
        self.default_responses = (
            "That's interesting! Can you tell me more?",
            "I see. What else can you share?",
            "Hmm, I would like to know more about that.",
            "Oh, really? Please elaborate.",
            "Can you explain a bit more?",
            "Why do you say that?",
            "How do you feel about it?"
        )

    def greet(self):
        self.name = input("What is your name?\n")
        will_help = input(
            f"Hi {self.name}, I am ChatBot. Would you like to chat with me?\n")
        if will_help.lower() in self.negative_responses:
            print("Ok, have a nice day!")
            return
        self.chat()

    def make_exit(self, reply):
        for command in self.exit_commands:
            if reply == command:
                print("Okay, have a nice day!")
                return True
        return False

    def chat(self):
        reply = input(random.choice(self.random_questions)).lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply)).lower()

    def match_reply(self, reply):
        doc = self.nlp(reply)
        for key, pattern in self.conversation_patterns.items():
            if re.search(pattern, reply):
                if key == 'describe_place_intent':
                    return self.describe_place_intent()
                elif key == 'answer_why_intent':
                    return self.answer_why_intent()
                elif key == 'about_book_movie':
                    return self.about_book_movie()
                elif key == 'about_session':
                    return self.about_session()
        return self.no_match_intent(doc, reply)

    def describe_place_intent(self):
        responses = ("I love visiting the mountains, they're so peaceful.\n",
                     "The beach is my favorite place to relax and unwind.\n")
        return random.choice(responses)

    def answer_why_intent(self):
        responses = ("I enjoy having meaningful conversations.\n",
                     "I'm here to learn more about you.\n",
                     "I love making new friends.\n")
        return random.choice(responses)

    def about_book_movie(self):
        responses = ("Harry Potter is a fascinating series! Which book or movie is your favorite?\n",
                     "I love the magical world of Harry Potter! Do you have a favorite character?\n",
                     "J.K. Rowling did an amazing job with Harry Potter. What do you like the most about it?\n")
        return random.choice(responses)

    def about_session(self):
        responses = ("The next session is on 14th Aug 2022.\n",
                     "The session is really informative and fun!\n")
        return random.choice(responses)

    def no_match_intent(self, doc, reply):
        # Check for negative response
        if any(neg in reply.lower() for neg in self.negative_responses):
            return "I see. Is there something else you'd like to talk about?"

        # Check if user indicates they want to continue
        if reply.strip().lower() in ("yes", "yep", "yah", "ofcourse"):
            return random.choice(self.random_questions)

        # Check if user indicates they have nothing more to share
        if reply.strip().lower() in ("nothing", "no", "nope", "nah"):
            return "Alright, feel free to ask me anything else!"

        # Extract entities and try to use them in responses
        entities = [ent.text for ent in doc.ents]
        if entities:
            return f"Tell me more about {entities[0]}.\n"

        return random.choice(self.default_responses)

ChatBot = ChatBot()
ChatBot.greet()