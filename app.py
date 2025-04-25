from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset (ensure you have a 'average_rating' column)
books_df = pd.read_csv(r"C:\Users\tripa\Desktop\project\book reccomendation system\dataa.csv\books.csv")  # adjust path if needed
books_df.dropna(subset=["title", "authors", "average_rating"], inplace=True)

# Home route
@app.route('/')
def home():
    return render_template("index.html")

# Recommendation route
@app.route('/recommend', methods=['POST'])
def recommend():
    book_title = request.form['book_title']
    try:
        # Find the book's author
        book_info = books_df[books_df['title'].str.lower() == book_title.lower()]
        
        if book_info.empty:
            return render_template("result.html", input_title=book_title, recommendations=[], error="Book not found!")
        
        author_name = book_info.iloc[0]['authors']
        
        # Get books by the same author and sort by average_rating
        author_books = books_df[books_df['authors'] == author_name]
        author_books_sorted = author_books.sort_values(by='average_rating', ascending=False)
        
        # Get the top 5 books of the author (excluding the input book)
        recommendations = author_books_sorted[author_books_sorted['title'].str.lower() != book_title.lower()].head(5)
        
        recommendations = recommendations[['title', 'authors', 'average_rating']].to_dict(orient='records')
        
        return render_template("result.html", input_title=book_title, recommendations=recommendations)
    
    except IndexError:
        return render_template("result.html", input_title=book_title, recommendations=[], error="Book not found!")

if __name__ == '__main__':
    app.run(debug=True)
