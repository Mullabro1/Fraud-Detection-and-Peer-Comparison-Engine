import re

def eliza_response(user_input):
    responses = [
        (r"hello|hi", "Hello! How can I help you today?"),
        (r"i feel (.*)", "Why do you feel \1?"),
        (r"my name is (.*)", "Nice to meet you, \1!"),
        (r"i need (.*)", "Why do you need \1?"),
        (r"i am (.*)", "How long have you been \1?"),
        (r"i want (.*)", "What would it mean to you if you got \1?"),
        (r"i like (.*)", "Why do you like \1?"),
        (r"i hate (.*)", "Why do you hate \1?"),
        (r"i dream (.*)", "What does that dream signify to you?"),
        (r"why don't you (.*)", "Do you wish I could \1?"),
        (r"are you (.*)", "Why does it matter if I am \1?"),
        (r"can you (.*)", "Perhaps you can \1 yourself?"),
        (r"you are (.*)", "How do you feel about me being \1?"),
        (r"always", "Can you think of a specific example?"),
        (r"never", "Are you sure it's never happened?"),
        (r"because", "Is that the real reason?"),
        (r"sorry", "Don't be sorry, tell me more."),
        (r"yes", "I see, can you elaborate on that?"),
        (r"no", "Why not?"),
        (r"maybe", "What makes you uncertain?"),
        (r"if (.*)", "What would happen if \1?"),
        (r"what", "What do you think?"),
        (r"how", "How do you feel about that?"),
        (r"where", "Where would you like to go with that?"),
        (r"when", "When do you think this might happen?"),
        (r"who", "Who comes to mind when you think about this?"),
        (r"why", "Why do you think that is?"),
        (r"could you (.*)", "Could you do \1?"),
        (r"should i (.*)", "What would happen if you did \1?"),
        (r"i think (.*)", "Why do you think \1?"),
        (r"i believe (.*)", "What makes you believe \1?"),
        (r"i remember (.*)", "What does that memory mean to you?"),
        (r"i forget (.*)", "Why do you think you've forgotten \1?"),
        (r"friend", "Tell me more about your friend."),
        (r"family", "How does your family feel about this?"),
        (r"love", "What does love mean to you?"),
        (r"lonely", "Why do you feel lonely?"),
        (r"happy", "What makes you happy?"),
        (r"sad", "What has made you sad?"),
        (r"angry", "What has caused your anger?"),
        (r"bye", "Goodbye! Take care."),
        (r".*", "Tell me more about that.")  # Default response
    ]

    for pattern, response in responses:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            return response.replace(r"\1", match.group(1)) if match.groups() else response

    return "Can you elaborate?"

# Chat loop
print("chatbot: Hello! Type 'bye' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "bye":
        print("chatbot: Goodbye!")
        break
    print(f"chatbot: {eliza_response(user_input)}")