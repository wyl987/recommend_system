import streamlit as st
import pymongo
import openai
import pickle
from bson.binary import Binary


mongo_URI = st.secrets["mongo_URI"]

# 1. Create mongodb connection
db_client = pymongo.MongoClient(mongo_URI)
db = db_client["recommend_system"]
# like a table in SQL
collection = db["responses"]

# 2. Auth with openai and generwate embeddings
openai.api_key = st.secrets["​​OPENAI_API_KEY"]

st.title('GHW Valentines Recommendation System')

st.divider()

st.image('https://img.freepik.com/free-vector/couple-romantic-penguins-celebrating-saint-valentine_1150-40223.jpg?t=st=1739248566~exp=1739252166~hmac=9fff7fd7e5827db99baa37c6e33ece1e446703c3b3ab5ee68995af4a6f8491cf&w=360', width=300)

st.subheader('Fill the questions so you can get a match!')

name = st.text_input('What is your name?')
hobbies = st.text_input('What are your top three interests or hobbies?')
new_hobbies = st.text_input('What’s one hobby or activity you’ve always wanted to try but haven’t yet?')
cuisine = st.text_input('What’s your favorite type of cuisine?')
music = st.text_input('What type of music do you enjoy the most?')
partner_traits = st.text_area('What are you looking for in a partner?')
personalities = st.text_area('How would your friends describe your personality?')

# 3. Generate embeddings from openai model
def get_embeddings(text):
  response = openai.embeddings.create(
      input=text,
      model="text-embedding-ada-002"
  ) 
  return response.data[0].embedding

# 4. Save the responses to mongodb
def save_response_to_db(response, embedding):
  result = collection.insert_one({
    "responses": response,
    # Store embeddings as binary data
    "embedding": Binary(pickle.dumps(embedding))
  })
  return result.inserted_id


if st.button("Submit"):
  # recommendation function
  st.success("Match found!")
else:
  st.warning("Please fill in the questions above.")

