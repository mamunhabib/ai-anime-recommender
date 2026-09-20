import streamlit as st
import os
import sys

# We need this to ensure the app can find the pipeline folder!
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pipeline.pipeline import get_anime_recommendation

# 1. Setup the Web Page Tab
st.set_page_config(
    page_title="AI Anime Recommender",
    page_icon="🎬",
    layout="centered"
)

# 2. Build the UI 
st.title("🎬 AI Anime Recommender")
st.write("Welcome! Describe the kind of anime you want to watch, and our Llama-3 AI will find the perfect match for you.")

# 3. Create a Search Box
user_input = st.text_input(
    "What are you in the mood for?", 
    placeholder="e.g., A funny anime about high school students with magic powers..."
)

# 4. The Action Button
if st.button("Get Recommendation", type="primary"):
    if user_input:
        # Show a loading spinner while Groq is thinking
        with st.spinner("Searching the database and asking Llama-3..."):
            try:
                # Call our pipeline!
                recommendation = get_anime_recommendation(user_input)
                
                # Display the answer in a nice green box
                st.success("Here is your recommendation:")
                st.write(recommendation)
            except Exception as e:
                st.error(f"Oops! Something went wrong: {e}")
    else:
        st.warning("Please type a description first!")
