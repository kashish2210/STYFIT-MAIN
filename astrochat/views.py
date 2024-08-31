from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import json
from django.http import JsonResponse

# In-memory storage for chat history (for demonstration purposes)
chat_history = []
genai.configure(api_key="AIzaSyA2i4KZU4YzGty_GN0-obC07e_ufWPlxdg")

model = genai.GenerativeModel("gemini-1.5-flash")


@csrf_exempt
def chatbot_view(request):
    global chat_history  # Access the global chat history

    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("user_message")

        if user_message:

            prompt = f""""Here's a questions from a user in my Styfit, which is an ecommerce site. '{user_message}'. And here a list of all the previous quetions asked by user and answers given by gemini previous.
              The list follows this order, it first contains dictionary of the user's question and then a dictionary containing the answer of gemini.In each dictionary the user key specifies 
              whose response is it, user for user and bot for gemini. '{str(chat_history)}'\n Provide the answer only so that your generated response looks more like a person 
              talking and a not a bot or llm. The question of the user may not be a question, it may be a greeting or something else as your response is going to be used in my chatbot, so make the response appropriate as if you're talking to the user. 
              It is possible that you might not get any list containing the previous conversation of the user. That means the user is just starting the conversation, so answer appropriately."""
            response = model.generate_content(prompt)
            # Add user message to chat history
            chat_history.append({"user": "user", "text": user_message})

            # Your chatbot logic goes here, replace this with your logic
            bot_response = response.text

            # Add bot response to chat history
            chat_history.append({"user": "bot", "text": bot_response})

        # Redirect to the same page to clear the form data
        return JsonResponse({"response": bot_response})

    # Pass the chat history to the template
    return render(request, "chatbot.html", {"chat_history": chat_history})