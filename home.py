import streamlit as st
import pymongo
from sentence_transformers import SentenceTransformer
import pickle
from bson.binary import Binary
from sklearn.metrics.pairwise import cosine_similarity

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

# 1. Create mongodb connection
mongo_URI = st.secrets["general_secrets"]["mongo_URI"]
db_client = pymongo.MongoClient(mongo_URI)
db = db_client["recommend_system"]
# like a table in SQL
collection = db["responses"]

# 2. Load Hugging Face sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Generate embeddings from sentence transformer model
def get_embeddings(text):
  embedding = model.encode(text)
  print(embedding)
  return embedding

# 4. Save the responses to mongodb
def save_response_to_db(response, embedding):
  result = collection.insert_one({
    "responses": response,
    # Store embeddings as binary data
    "embedding": Binary(pickle.dumps(embedding))
  })
  return result.inserted_id

# find and match using cosine similarity math formula
def find_match(current_user_id, current_embedding):
  # Get all the responses
  all_responses = collection.find({})
  similarities = []
  
  for doc in all_responses:
    if doc ['_id']  == current_user_id:
      continue
    stored_embedding = pickle.loads(doc['embedding'])
    similarity_score = cosine_similarity([current_embedding], [stored_embedding])[0][0]
    similarities.append((doc['_id'], similarity_score, doc['responses']))
  
  similarities.sort(reverse=True, key=lambda x:x[1])
  
  return similarities[0] if similarities else None
    
if st.button("Submit"):
  if name and hobbies and new_hobbies and cuisine and music and partner_traits and personalities:
    response = {
      "name": name,
      "hobbies": hobbies,
      "new_hobbies": new_hobbies,
      "cuisine": cuisine,
      "music": music,
      "partner_traits": partner_traits,
      "personalities": personalities
    }
    # generate embeddings
    response_text  = " ".join(response.values())
    actual_embedding = get_embeddings(response_text)
    
    #save the response to db
    current_user_id = save_response_to_db(response, actual_embedding)
    
    # find match
    match = find_match(current_user_id, actual_embedding)
    
    if match:
      top_match, top_score, top_response = match
      top_match_name = top_response["name"] 
      st.success(f"Match found! Top match: {top_match_name}, Score: {top_score}")
    else: 
      st.warning("You are the first one to fill in the form. Please wait for others to fill in the form.")
    
  else:
    st.warning("Please fill in all the questions above.")
    
  
else:
  st.warning("Please fill in the questions above.")

