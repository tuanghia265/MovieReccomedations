import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        # Lấy thông tin phim từ API
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c797cba6934544921f633bfc2cd7eb20')
        data = response.json()
        
        # Kiểm tra xem có poster không
        if 'poster_path' in data:
            return "https://image.tmdb.org/t/p/original/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

def reccomend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    reccomended_movies = []
    reccomended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from APIs
        reccomended_movies.append(movies.iloc[i[0]].title)
        reccomended_movies_posters.append(fetch_poster(movie_id))
        
    return reccomended_movies, reccomended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title("Movie Recommender System")
options = st.selectbox('Choose your option', movies['title'].values)

if st.button('Reccomend'):
    recommended_movie_names, recommended_movie_posters = reccomend(options)
    
    # Display recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
