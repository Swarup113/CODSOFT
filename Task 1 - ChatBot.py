import tkinter as tk

def chatbot_response(user_input):
    """
    Enhanced chatbot logic with more responses and follow-up questions.
    """
    user_input = user_input.lower()
    
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you today? Do you want to know about the weather, news, or something else?"
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm here to help you! What would you like to know?"
    elif "who are you" in user_input:
        return "I'm just a bot, but I'm here to help you! What would you like to know?"
    elif "what are you" in user_input:
        return "I'm just a bot, but I'm here to help you! What would you like to know?"
    elif "weather" in user_input:
        return "I can't provide real-time weather updates yet, but I'm here to chat! Would you like to talk about something else?"
    elif "news" in user_input:
        return "I don't have the latest news, but feel free to ask me about simple facts or general information!"
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! Have a great day!"
    elif "your name" in user_input:
        return "I'm a simple chatbot created to assist you with basic questions. What else would you like to know?"
    elif "help" in user_input:
        return "I'm here to assist you! You can ask me about the weather, news, or any general information."
    elif "thank you" in user_input or "thanks" in user_input:
        return "You're welcome! Feel free to ask me anything else."
    elif "who created you" in user_input:
        return "I was created by a developer to help answer your questions. What else would you like to know?"
    elif "joke" in user_input:
        return "Why don't scientists trust atoms? Because they make up everything!"
    elif "color" in user_input:
        return "I don't have a favorite color, but I think all colors are wonderful. What's your favorite?"
    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"

def send_message(event=None):
    """
    Function to handle sending messages.
    """
    user_input = user_entry.get()
    if user_input.strip() != "":  # Ensure input is not empty
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + '\n', 'user')
        chat_window.insert(tk.END, "Bot: " + chatbot_response(user_input) + '\n\n', 'bot')
        chat_window.config(state=tk.DISABLED)
        user_entry.delete(0, tk.END)

def close_chat():
    """
    Function to close the chat window.
    """
    root.destroy()

# Setting up the GUI window
root = tk.Tk()
root.title("Enhanced Chatbot")
root.configure(bg='#080826')

# Chat window to display the conversation
chat_window = tk.Text(root, bd=1, bg="#161616", width=50, height=20, font=("Arial", 12), state=tk.DISABLED)
chat_window.tag_configure('user', foreground='#FFD4AC')
chat_window.tag_configure('bot', foreground='#ECF9FC')
chat_window.pack(padx=10, pady=10)

# Entry widget to accept user input
user_entry = tk.Entry(root, bd=1, bg="white", width=50, font=("Arial", 12))
user_entry.pack(padx=10, pady=10)
user_entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

# Frame to hold the buttons
button_frame = tk.Frame(root, bg='#161616')
button_frame.pack(padx=10, pady=5)

# Close button to close the chat window
close_button = tk.Button(button_frame, text="Close", font=("Arial", 12), bg="#7A3B0F", fg="white", width=12, command=close_chat)
close_button.grid(row=0, column=0, padx=5)

# Submit button to send the user input
send_button = tk.Button(button_frame, text="Submit", font=("Arial", 12), bg="#4E6F61", fg="white", width=12, command=send_message)
send_button.grid(row=0, column=1, padx=5)

# Run the GUI loop
root.mainloop()
