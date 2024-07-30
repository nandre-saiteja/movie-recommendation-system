import streamlit as st
import pickle
import requests


def fetch_movie_images(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c0865b73a17dcc94f3bcd1e2531356e3&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

def recommend(movie_name):
    movie_index = movies_list[movies_list['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_list = []
    recommended_movies_images = []
    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].id
        recommended_list.append(movies_list.iloc[i[0]].title)
        recommended_movies_images.append(fetch_movie_images(movie_id))
    return recommended_list,recommended_movies_images


movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies = movies_list['title'].values

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'How wpuld you like to be contacted?',
    movies
)

if st.button('Recommend'):
    recommendations,recommendations_images = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)


    def render_recommendation(col, text, image_path):
        with col:
            st.markdown(
                f"<div style='text-align: center; height: 250px; display: flex; flex-direction: column; justify-content: center;'>"
                f"<p style='margin: 0;'>{text}</p>"
                f"<img src='{image_path}' style='max-width: 100%; height: auto;' />"
                f"</div>", unsafe_allow_html=True)


    render_recommendation(col1, recommendations[0], recommendations_images[0])
    render_recommendation(col2, recommendations[1], recommendations_images[1])
    render_recommendation(col3, recommendations[2], recommendations_images[2])
    render_recommendation(col4, recommendations[3], recommendations_images[3])
    render_recommendation(col5, recommendations[4], recommendations_images[4])