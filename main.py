import streamlit as st
from crew import meme_crew

st.title("AI Meme Creator 🤖🎭")

# User input for meme topic
user_input = st.text_input("Enter a meme topic or keyword:", "")

if st.button("Generate Meme"):
    if user_input:
        st.write("Generating meme ideas... Please wait.")
        result = meme_crew.kickoff(inputs={"ideation_task": user_input})
        
        # Display results
        st.subheader("Meme Concept:")
        st.write(result[0])  # Meme ideas
        
        st.subheader("Selected Meme Image:")
        st.write(result[1])  # Image template details
        
        st.subheader("Meme Captions:")
        st.write(result[2])  # Caption suggestions
    else:
        st.warning("Please enter a meme topic.")
