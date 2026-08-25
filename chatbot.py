import os
from google import genai

def main():
    # Initialize the client (it automatically picks up GEMINI_API_KEY from the environment)
    client = genai.Client()

    # Create a chat session using a recommended Gemini model
    # gemini-2.5-flash is fast and well-suited for general conversation
    chat = client.chats.create(model="gemini-3.6-flash")

    print("🤖 Gemini Chatbot Initialized! Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        try:
            # Get user input from the terminal
            user_input = input("You: ")
            
            # Check if the user wants to quit
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            # Skip empty inputs
            if not user_input.strip():
                continue

            # Send the message to the chat session
            response = chat.send_message(user_input)
            
            # Print the model's response
            print(f"\nBot: {response.text}\n")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")

if __name__ == "__main__":
    main()