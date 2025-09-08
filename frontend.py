import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Illustrated Story Generator",
    page_icon="📖",
    layout="wide",
)

# --- App Header ---
st.title("AI Illustrated Story Generator 📖")
st.markdown("Turn your simple idea into a rich, illustrated story with the help of AI.")

# --- Backend API URL ---
# This is the URL where our FastAPI backend is running.
# When running locally, it's usually at http://127.0.0.1:8000.
BACKEND_URL = "http://127.0.0.1:8000/generate_story"

# --- User Input Section ---
with st.form("story_form"):
    story_prompt = st.text_area(
        "Enter your story idea",
        "A lonely robot finds a flower in a post-apocalyptic city.",
        height=100
    )
    submitted = st.form_submit_button("Generate Story ✨")

# --- Story Generation and Display ---
if submitted:
    if not story_prompt.strip():
        st.error("Please enter a story idea.")
    else:
        # Show a loading spinner while we wait for the story.
        with st.spinner("Your story is being crafted and illustrated... Please wait."):
            try:
                # Prepare the data to send to the backend
                payload = {"prompt": story_prompt}
                
                # Make the POST request to our FastAPI backend
                response = requests.post(BACKEND_URL, json=payload, timeout=300) # 5-minute timeout

                # Check if the request was successful
                if response.status_code == 200:
                    story_data = response.json()
                    
                    # Display the story scene by scene
                    if "story" in story_data and story_data["story"]:
                        st.success("Your story is ready!")
                        for scene in story_data["story"]:
                            st.header(scene['title'])
                            st.image(scene['image_url'], caption=f"Illustration for '{scene['title']}'")
                            st.write(scene['text'])
                            st.divider()
                    else:
                        st.error("Failed to generate a valid story. The response was empty.")

                else:
                    # Handle errors from the backend
                    error_details = response.json().get('detail', 'Unknown error')
                    st.error(f"Error from backend (Status {response.status_code}): {error_details}")

            except requests.exceptions.RequestException as e:
                # Handle network-related errors (e.g., connection refused)
                st.error(f"Could not connect to the backend. Please ensure it's running. Error: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ using FastAPI, Streamlit, and OpenAI.")