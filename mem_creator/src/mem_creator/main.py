import streamlit as st
from crew import MemCreator  # Import your CrewAI setup

# Streamlit UI
st.set_page_config(page_title="😂 AI Meme Creator", layout="centered")

st.title("🤖 AI Meme Creator")
st.write("Generate hilarious memes using AI! Enter a topic, and let the AI do the rest.")

# User input
meme_idea = st.text_input("Enter a meme topic or trending event", "")

# Button to generate meme
if st.button("Generate Meme"):
    if meme_idea:
        st.write("🔍 Generating Meme... Please wait...")

        # Initialize CrewAI Meme Creator
        meme_creator = MemCreator()

        # Run the AI workflow
        crew_result = meme_creator.crew().kickoff(inputs={"meme_idea": meme_idea})

        # Debug: print the entire result to understand its structure
        st.write("Crew Result:", crew_result)

        # Assuming the task result is a dictionary, check the format first
        meme_concepts = crew_result.get("ideation_task", [])
        image_selection = crew_result.get("image_selection_task", {})
        caption_result = crew_result.get("caption_task", {})

        # Debugging: print out the task results
        st.write("Meme Concepts:", meme_concepts)
        st.write("Image Selection:", image_selection)
        st.write("Caption Result:", caption_result)

        # Display results
        if meme_concepts:
            st.subheader("💡 Meme Concept:")
            if isinstance(meme_concepts, list) and len(meme_concepts) > 0:
                st.write(meme_concepts[0])  # Display the first generated idea
            else:
                st.write("No meme concepts found.")

        if image_selection:
            meme_template = image_selection.get("name", "Unknown Template")
            meme_url = image_selection.get("url", "")

            st.subheader("🖼 Meme Template:")
            if meme_url:
                st.image(meme_url, caption=meme_template, use_column_width=True)
            else:
                st.write("No meme template found.")

        if caption_result:
            st.subheader("✍ Meme Caption:")
            st.write(f"**Top Text:** {caption_result.get('top_text', '')}")
            st.write(f"**Bottom Text:** {caption_result.get('bottom_text', '')}")

    else:
        st.warning("⚠ Please enter a meme topic before generating.")

st.markdown("---")
st.write("Powered by CrewAI 🚀 & Gemini API 🔥")
