import tkinter as tk
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split

# Load the MovieLens dataset
movies_df = pd.read_csv(r'F:\Files\Projects\Reccomend System\ml-latest-small\movies.csv')
ratings_df = pd.read_csv(r'F:\Files\Projects\Reccomend System\ml-latest-small\ratings.csv')

# Prepare data for collaborative filtering
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# User-Based Collaborative Filtering Model
user_based_sim_options = {'name': 'cosine', 'user_based': True}
user_based_model = KNNBasic(sim_options=user_based_sim_options)
user_based_model.fit(trainset)

# Item-Based Collaborative Filtering Model
item_based_sim_options = {'name': 'cosine', 'user_based': False}
item_based_model = KNNBasic(sim_options=item_based_sim_options)
item_based_model.fit(trainset)

def get_movies_by_genre(genre, top_n=10):
    # Get movies based on genre without any year restriction
    genre_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
    return genre_movies[['movieId', 'title']].sample(n=top_n) if not genre_movies.empty else pd.DataFrame()

def recommend_movies_based_on_likes(liked_movie_ids, genre):
    if not liked_movie_ids:
        return []

    # Filter movies from the selected genre
    genre_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]

    # Use item-based collaborative filtering to recommend movies
    predictions = []
    for movie_id in genre_movies['movieId']:
        for liked_movie_id in liked_movie_ids:
            try:
                pred = item_based_model.predict(liked_movie_id, movie_id)
                predictions.append((movie_id, pred.est))
            except:
                continue

    # Sort predictions by estimated rating
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Get top 5 recommended movie IDs, ensuring diversity by year
    recommended_movie_ids = []
    for movie_id, _ in predictions:
        if len(recommended_movie_ids) >= 5:
            break
        if movie_id not in liked_movie_ids:
            recommended_movie_ids.append(movie_id)

    # Retrieve movie titles for the recommended IDs
    recommended_movies = movies_df[movies_df['movieId'].isin(recommended_movie_ids)]

    return recommended_movies[['title']].sort_values(by='title').values.flatten().tolist()

def handle_user_input():
    global current_genre
    user_text = user_input.get().strip().lower()
    conversation_text.insert(tk.END, f"User: {user_text}\n", 'user')
    user_input.delete(0, tk.END)
    
    if user_text == 'exit':
        conversation_text.insert(tk.END, "System: Thank you for using the Movie Recommendation System. Goodbye!\n", 'system')
        root.destroy()  # Close the application
        return

    if user_text.capitalize() in genres:
        current_genre = user_text.capitalize()
        genre_movies = get_movies_by_genre(current_genre)
        if not genre_movies.empty:
            conversation_text.insert(tk.END, f"System: Here are some {current_genre} movies:\n", 'system')
            for index, row in genre_movies.iterrows():
                conversation_text.insert(tk.END, f"- {row['title']}\n", 'system')
            conversation_text.insert(tk.END, "System: Please enter the titles of movies you liked from the list, separated by commas, or type 'None' if you haven't liked any of them.\n", 'system')
        else:
            conversation_text.insert(tk.END, "System: No movies found for this genre. Please try another genre.\n", 'system')
    else:
        if user_text == 'none':
            genre_movies = get_movies_by_genre(current_genre)  # Provide more movies from the same genre
            if not genre_movies.empty:
                conversation_text.insert(tk.END, f"System: Here are some more {current_genre} movies:\n", 'system')
                for index, row in genre_movies.iterrows():
                    conversation_text.insert(tk.END, f"- {row['title']}\n", 'system')
                conversation_text.insert(tk.END, "System: Please enter the titles of movies you liked from the list, separated by commas, or type 'None' if you haven't liked any of them.\n", 'system')
            else:
                conversation_text.insert(tk.END, "System: No more movies found for this genre. Please try another genre.\n", 'system')
        else:
            # Clean up user input and match against movie titles
            user_likes_list = [title.strip().lower() for title in user_text.split(',')]
            movies_df['title_clean'] = movies_df['title'].str.lower().str.strip()  # Standardize titles
            liked_movies_df = movies_df[movies_df['title_clean'].isin(user_likes_list)]
            
            if not liked_movies_df.empty:
                liked_movie_ids = liked_movies_df['movieId'].tolist()
                recommendations = recommend_movies_based_on_likes(liked_movie_ids, current_genre)
                if recommendations:
                    conversation_text.insert(tk.END, f"System: Based on your likes, you might enjoy:\n", 'system')
                    for movie in recommendations:
                        conversation_text.insert(tk.END, f"- {movie}\n", 'system')
                else:
                    conversation_text.insert(tk.END, "System: No recommendations available based on your likes. Please try again.\n", 'system')
            else:
                conversation_text.insert(tk.END, "System: No valid movies found from the list. Please enter titles from the list or type 'None' if you didn't like any of them.\n", 'system')
            
            conversation_text.insert(tk.END, "System: To get recommendations for a different genre, type the genre name. To exit, type 'Exit'.\n", 'system')

# Initialize Tkinter window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("600x720")
root.configure(bg='#080826')  # Set background color

# Chat-like text box for conversation display
conversation_text = tk.Text(root,bd=1, height=35, width=60, bg='#161616', fg='#080826', insertbackground='#080826')
conversation_text.pack(padx=10,pady=5)

# Entry field for user input
user_input = tk.Entry(root, width=50)
user_input.pack(pady=5)

# List of genres
genres = ['Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror', 'Romance', 'Thriller']
current_genre = None  # Variable to keep track of the current genre

# Display initial instructions
conversation_text.insert(tk.END, "System: Welcome to the Movie Recommendation System.\n", 'system')
conversation_text.insert(tk.END, "System: Please enter a genre from the following list: Action, Adventure, Comedy, Drama, Fantasy, Horror, Romance, Thriller.\n", 'system')

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='#080826')
button_frame.pack(pady=5, side=tk.BOTTOM, fill=tk.X)

# Button to submit user input
close_btn = tk.Button(button_frame, text="Close", font=("Arial", 12), bg="#7A3B0F", fg="white", width=12, command=root.destroy)
close_btn.grid(row=0, column=0, padx=125)

# Submit button to send the user input
send_btn = tk.Button(button_frame, text="Submit", font=("Arial", 12), bg="#4E6F61", fg="white", width=12, command=handle_user_input)
send_btn.grid(row=0, column=1)

# Bind the Enter key to submit user input
root.bind('<Return>', lambda event: handle_user_input())

# Add color tags to the text widget
conversation_text.tag_configure('system', foreground='#ECF9FC')
conversation_text.tag_configure('user', foreground='#FFD4AC') 

# Start the GUI loop
root.mainloop()
