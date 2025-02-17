# GHW Valentines Recommendation System

A recommendation system for matching people based on their answers to a set of personal questions. The system uses **cosine similarity** to match users by comparing their responses' embeddings generated from a pre-trained model. The system stores the responses and embeddings in MongoDB, allowing users to find their best match from the database.

## Technologies Used

- **Streamlit**: For building the web app interface.
- **MongoDB**: For storing responses and embeddings.
- **SentenceTransformer**: For generating embeddings using pre-trained models.
- **Scikit-learn**: For calculating cosine similarity.

## Features
- **User Input**: Users fill out a form with their personal preferences and traits.
- **Embedding Generation**: The app generates embeddings from user responses using a language model.
- **Cosine Similarity**: The system matches users by comparing the cosine similarity between their response embeddings.
- **MongoDB Storage**: Responses and embeddings are stored in a MongoDB database for easy retrieval.
- **Real-Time Matching**: After a user submits their responses, the system searches for the best match in real-time.

## Prerequisites

- Python 3.x
- MongoDB (Cloud or local instance)
- Streamlit for the front-end interface
- Sentence Transformer for embedding generation

## Installation

1. Clone the repository:
  ```bash
   git clone https://github.com/wyl987/recommend_system.git
  ```
2. Install the required packages:
  ```bash
   pip install -r requirements.txt
  ```
3. Set up MongoDB (either local or use MongoDB Atlas) and store your MongoDB URI in Streamlit secrets.

4. Create a .streamlit/secrets.toml file and add your MongoDB URI:
  ```toml
    [general_secrets]
    mongo_URI = "your-mongo-uri"  
  ```
5. Run the app using Streamlit:
  ```bash
   streamlit run home.py
  ```
## Usage

1. Open the application by running the following command:

   ```bash
   streamlit run home.py
   ```
2. Fill out the form with your personal information and submit the form to see your match! The app will search the MongoDB collection for the most similar responses and display the top match.

## Acknowledgements

Special thanks to **MLH** for organizing the amazing Global Hack Week and providing many useful workshops for AI/ML.

## License

This project is licensed under the MIT License.