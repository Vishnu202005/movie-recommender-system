import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Download similarity.pkl from Google Drive if not present
if not os.path.exists('similarity.pkl'):
    with st.spinner('Downloading model data, please wait...'):
        gdown.download(
            'https://drive.google.com/uc?id=1zRGkhAQ7kb57B2Wz9UJ5QLT-ecg-lVQC',
            'similarity.pkl',
            quiet=False
        )

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict).reset_index(drop=True)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=f0e72b665e63ccc82719bbc443e671e9'.format(movie_id)
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])