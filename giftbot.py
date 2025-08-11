from openai import OpenAI
import streamlit as st


api_key = st.secrets["OPENAI_API_KEY"]
print("key", api_key[:10])

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key= "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",
)

st.set_page_config(page_title="GiftBot", page_icon = "🎁")
st.title("🎁 GiftBot: Find the Perfect Gift")

#Set up the form
with st.form("gift_form"):
    recipient = st.text_input("Who is this gift for?")
    interests = st.text_area("What do they like (i.e. hobbies, brands, lifestyle)?")
    history = st.text_area("What have you talked with this person about?")
    budget = st.text_input("What’s your budget? (e.g., $50, under $100, no limit)")
    submitted = st.form_submit_button("Find Gift Ideas")

if submitted:
    if not all([recipient, interests, history, budget]):
        st.error("Please fill out all the fields.")
    else:
        with st.spinner("Thinking... 🎁"):
            # Construct GPT prompt
            prompt = f""" You are a gifting expert. Based on the following information, suggest 5 creative, thoughtful gift ideas. Include a brief explanation for each.
            Recipient: {recipient}
            Interests: {interests}
            History: {history}
            Budget: {budget}"""

            response = client.chat.completions.create(
                model = "openai/gpt-oss-20b:free",
                messages=[
                          {"role": "system", "content": "You are a smart and thoughtful assistant. Think carefully."},{"role": "user", "content": prompt}]
            )

            gift_ideas = response.choices[0].message.content
            st.success("Here are some gift ideas!")
            st.markdown(gift_ideas)