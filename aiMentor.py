import streamlit as st
import openai
import requests
import json

# Set your OpenAI API Key
openai.api_key = '<add your key here>'

# Set your Google Cloud Translation API Key
GOOGLE_TRANSLATE_API_KEY = '<add your key here>'

# Function to translate text using Google Cloud Translation API
def translate_text(text, target_language):
    url = f'https://translation.googleapis.com/language/translate/v2?key={GOOGLE_TRANSLATE_API_KEY}'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'q': text,
        'target': target_language
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    translated_text = result['data']['translations'][0]['translatedText']
    detected_language = result['data']['translations'][0]['detectedSourceLanguage']
    return translated_text, detected_language

# Function to generate response from GPT-3.5
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or whatever engine you're using
        prompt=prompt,
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].text.strip()

st.title('Language Translation and Chatbot')

user_input = st.text_input('Enter your text here')

if user_input:
    # Step 1: Translate user input to English
    translated_text, detected_language = translate_text(user_input, 'en')
    st.write(f'Translated Text: {translated_text}')

    # Step 2: Ask GPT-3.5 to review the translated text
    review_prompt_1 = f'This text was translated from {detected_language} to English: "{translated_text}". Original text: {user_input}. Make any changes to the translated text and respons back just with the updated translated text.'
    reviewed_translated_text = generate_response(review_prompt_1)
    st.write(f'Reviewed Translation: {reviewed_translated_text}')

    # Step 3: Generate a response using GPT-3.5
    response = generate_response(reviewed_translated_text)
    st.write(f'GPT-3.5 Response in English: {response}')

    # Step 4: Translate the response back to the detected language
    translated_response, _ = translate_text(response, detected_language)
    st.write(f'GPT-3.5 Response translated back to Original Language: {translated_response}')

