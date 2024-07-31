import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

# Function to combine the important features
def combine_features(row):
    return row['genres'] + ' ' + row['keywords'] + ' ' + row['tagline'] + ' ' +  ' '+row['cast'] 

# Function to get the title from the index
def get_title_from_index(index, df):
    return df[df.index == index]["title"].values[0]

# Function to get the index from the title
def get_index_from_title(title, df):
    return df[df.title == title].index.values[0]

# Function to recommend movies
def recommend_movies(movie_title, df, similarity_matrix):
    movie_index = get_index_from_title(movie_title, df)
    similar_movies = list(enumerate(similarity_matrix[movie_index]))

    # Sort the list of similar movies according to similarity scores
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

    recommended_movies = []
    for i in range(10):  # Recommend top 10 movies
        index = sorted_similar_movies[i][0]
        title_from_index = get_title_from_index(index, df)
        recommended_movies.append(title_from_index)

    return recommended_movies

def main():
    # Custom CSS styling
    st.markdown("""
        <style>
        .main {
            background-color: #f8d7da;  /* Light pink background */
        }
        .title {
            color: #e83e8c;  /* Dark pink heading */
            font-size: 2.5em;
        }
        .stSelectbox, .stButton, .stWrite {
            background-color: #fce4ec;  /* Light pink button and text background */
            color: #e83e8c;  /* Dark pink text */
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h1 class="title">Movie Recommendation System</h1>', unsafe_allow_html=True)

    # Load the dataset
    file_path = r'C:\Users\shalu\Movie Reccomendation\MOVIE-RECCOMENDATION-SYSTEM\merged_movies_credits.csv'
    df = pd.read_csv(file_path)

    # Handle NaN values
    features = ['genres', 'keywords', 'tagline', 'cast']
    for feature in features:
        df[feature] = df[feature].fillna('')

    # Create a column to combine features
    df["combined_features"] = df.apply(combine_features, axis=1)

    # Create the Count Vectorizer matrix
    count_matrix = CountVectorizer().fit_transform(df["combined_features"])

    # Compute the Cosine Similarity based on the count_matrix
    cosine_sim = cosine_similarity(count_matrix)

    # Select a movie
    movie_list = df['title'].values
    selected_movie = st.selectbox("Select a movie you like", movie_list, key='movie_selectbox')

    # Add a unique key to the button
    if st.button('Recommend', key='recommend_button'):
        recommendations = recommend_movies(selected_movie, df, cosine_sim)
        st.write("Recommended Movies:")
        for movie in recommendations:
            st.write(movie)

if __name__ == '__main__':
    main()
