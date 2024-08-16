import openai
from flask import Flask, request, jsonify

openai.api_key = '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'

conversation_summary = []

def generate_chat_response(message):
    response = openai.ChatCompletion.create(
        model='text-davinci-003',
        prompt=message,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()
# def generate_chat_response(conversation):
#     # Concatenate the conversation history into a single string
#     conversation_history = ""
#     for entry in conversation:
#         conversation_history += entry["user_message"] + "\n" + entry["bot_message"] + "\n"

#     # Generate a response based on the conversation history
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=conversation_history,
#         max_tokens=50,
#         temperature=0.7,
#         n=1,
#         stop=None
#     )
#     return response.choices[0].text.strip()

def feedback():
    data = request.get_json()
    message = data["message"]

    # Send user's message to OpenAI ChatGPT
    response = generate_chat_response(message)

    # Extract satisfaction rating from user's response
    satisfaction_rating = extract_satisfaction_rating(response)

    # Add conversation and satisfaction rating to the summary
    add_to_summary(message, response, satisfaction_rating)

    # Prepare response to be sent back to the user
    response_data = {
        "message": response,
        "satisfaction_rating": satisfaction_rating,
        "summary": get_summary()
    }

    return jsonify(response_data)

def extract_satisfaction_rating(response):
    # Implement logic to extract satisfaction rating from user's response
    # You can use regular expressions, keywords, or other techniques to extract the rating
    # In this example, we assume the rating is in the form of a number between 1 and 5
    satisfaction_rating = 0

    if "1" in response:
        satisfaction_rating = 1
    elif "2" in response:
        satisfaction_rating = 2
    elif "3" in response:
        satisfaction_rating = 3
    elif "4" in response:
        satisfaction_rating = 4
    elif "5" in response:
        satisfaction_rating = 5

    return satisfaction_rating

def add_to_summary(message, response, satisfaction_rating):
    # Implement logic to add the conversation and satisfaction rating to the summary
    # You can store the conversation and rating in a database, file, or any other storage method
    # In this example, we assume the conversation and rating are stored in a list of dictionaries
    conversation_summary.append({
        "message": message,
        "response": response,
        "satisfaction_rating": satisfaction_rating
    })

def get_summary():
    # Implement logic to generate the summary from the stored conversation and ratings
    # You can format the summary as desired, such as aggregating ratings and providing insights
    # In this example, we assume the summary is a string concatenating the conversation and ratings
    summary = ""
    for entry in conversation_summary:
        summary += f"User: {entry['message']}\nBot: {entry['response']}\nSatisfaction Rating: {entry['satisfaction_rating']}\n\n"

    return summary

if __name__ == "__main__":
    print('''Hello Good Morning! Hope you are doing good. I am the feedback bot for the food that you ordered.
      I would like to ask you three questions to get your feedback. Hope you are fine with it''')

    initial_questions = [
        "How satisfied are you with the food quality?",
        "How satisfied are you with the delivery boy services?",
        "How satisfied are you with our overall service?"
    ]

    conversation = []

    while len(conversation) < len(initial_questions) + 1:
        if len(conversation) < len(initial_questions):
            question = initial_questions[len(conversation)]
        else:
            question = generate_chat_response(conversation)
            # question = generate_response(message, conversation)

        user_message = input(f"User: {question}\n")

        if len(conversation) < len(initial_questions):
            conversation.append({"user_message": user_message, "bot_message": question})
        else:
            response = generate_chat_response(conversation)
            # response = generate_response(user_message, conversation)
            conversation.append({"user_message": user_message, "bot_message": response})

    summary = get_summary()
    # summary = get_summary(conversation)
    # satisfaction_ratings = generate_satisfaction_ratings(initial_questions, conversation)
    satisfaction_ratings = generate_chat_response(conversation)

    print("\nChat ended. Thank you for your feedback! ")
    print("Satisfaction Ratings:")

    for question, rating in satisfaction_ratings.items():
        print(f"{question}: {rating}")
    print("\nSummary:")
    print(summary)
