
# from dotenv import load_dotenv
# import streamlit as st
# import os
# import requests
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure the Gemini API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Function to load Gemini Pro model and get responses
# model = genai.GenerativeModel("gemini-pro") 
# chat = model.start_chat(history=[])

# def get_gemini_response(question):
#     response = chat.send_message(question, stream=True)
#     return response

# # Fetch data from your custom API
# def fetch_custom_api_data():
#     api_url = "https://cwbackend-a3332a655e1f.herokuapp.com/api"  # Example API endpoint
#     try:
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": "Failed to fetch data from the API"}
#     except Exception as e:
#         return {"error": str(e)}

# # Fetch food product details (calories, ingredients, harmful substances)
# def fetch_food_info(product_name):
#     food_api_url = f"https://api.spoonacular.com/food/products/search?query={product_name}&apiKey={os.getenv('SPOONACULAR_API_KEY')}"
#     try:
#         response = requests.get(food_api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": "Failed to fetch food data"}
#     except Exception as e:
#         return {"error": str(e)}

# # Streamlit app setup
# st.set_page_config(page_title="Q&A & Food Info Demo")

# st.header("Gemini LLM & Food Product Information Application")

# # Initialize session state for chat history if it doesn't exist
# if 'chat_history' not in st.session_state:
#     st.session_state['chat_history'] = []

# # Input form for the question and description
# product_name = st.text_input("Product Name: ", key="product_name")
# product_description = st.text_input("Product Description: ", key="product_description")
# submit = st.button("Submit")

# if submit and product_name and product_description:
#     query = f"{product_name}\n{product_description}"
    
#     # Fetch response from Gemini LLM
#     response = get_gemini_response(query)
    
#     # Fetch response from your custom API
#     api_data = fetch_custom_api_data()
    
#     st.subheader("Response Received")
    
#     # Display verdict and response based on API or Gemini
#     for chunk in response:
#         st.write("Verdict: Misleading")  # Example static verdict
#         st.write(chunk.text)
#         st.session_state['chat_history'].append(("Bot", chunk.text))
    
#     # Display API data if fetched successfully
#     if "error" not in api_data:
#         st.subheader("Detailed Information")
#         st.write(api_data)
#     else:
#         st.write(api_data["error"])

# # Section for Chatbot to ask questions about the food product
# st.subheader("Ask Questions About the Product")

# user_question = st.text_input("Ask a question about the product: ", key="user_question")
# ask_question = st.button("Ask")

# if ask_question and user_question:
#     chat_response = get_gemini_response(user_question)
    
#     st.subheader("Chatbot Response")
    
#     # Display chatbot response
#     for chunk in chat_response:
#         st.write(chunk.text)
#         st.session_state['chat_history'].append(("Bot", chunk.text))

# # Button to delete chat history
# if st.button("Clear Chat History"):
#     st.session_state['chat_history'] = []
#     st.write("Chat history cleared.")

# # Display chat history
# st.subheader("Chat History")
# for role, text in st.session_state['chat_history']:
#     st.write(f"{role}: {text}")










from dotenv import load_dotenv 
import streamlit as st
import os
import requests
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

# Fetch Gemini response
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        return [{"error": str(e)}]

# Fetch data from your custom API
@st.cache_data
def fetch_custom_api_data():
    api_url = "https://cwbackend-a3332a655e1f.herokuapp.com/api"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data from the API"}
    except Exception as e:
        return {"error": str(e)}

# Fetch food product details (calories, ingredients, harmful substances)
def fetch_food_info(product_name):
    food_api_url = f"https://api.spoonacular.com/food/products/search?query={product_name}&apiKey={os.getenv('SPOONACULAR_API_KEY')}"
    try:
        response = requests.get(food_api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch food data"}
    except Exception as e:
        return {"error": str(e)}

# Streamlit app setup
st.set_page_config(page_title="Q&A & Food Info Demo")

# Inject CSS with st.markdown
st.markdown(
    """
    <style>
    html, body {
        background-color: #e6ffe6;  /* Very light green background */
        height: 100%; /* Ensure the body takes full height */
        margin: 0;    /* Remove default margin */
    }
    
    h2 {
        color: #007BFF !important;  /* Blue color for header */
        text-align: center;
    }
     
    .main {
        
        padding: 20px;
        border-radius: 100px;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Other CSS rules remain unchanged */
    .stTextInput input {
        border: 2px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
        font-family: 'Arial', sans-serif;
    }

    button, .stButton>button {
    background-color: #ddd; /* Grey color for button */
    color: black;           /* Text color */
    border: none;           /* No border */
    padding: 10px 20px;     /* Padding */
    font-size: 16px;        /* Font size */
    cursor: pointer;        /* Pointer cursor on hover */
    border-radius: 10px;    /* Rounded corners */
    transition: background-color 0.3s; /* Smooth transition */
    font-family: 'Arial', sans-serif;  /* Font family */
}

button:hover, .stButton>button:hover {
    background-color: #007BFF; /* Blue color on hover */
}


    .chat-history {
        background-color: white;
        border: 10px solid #ddd;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .bot-message {
        background-color: #e9f5e9;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-family: 'Arial', sans-serif;
    }

    .user-message {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Main app structure
st.header("Consumer Products Information Application")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input form for product
product_name = st.text_input("Product Name: ", key="product_name")
product_description = st.text_input("Product Description: ", key="product_description")
submit = st.button("Submit")

if submit and product_name and product_description:
    query = f"{product_name}\n{product_description}"
    
    # Fetch responses
    with st.spinner('Fetching data...'):
        response = get_gemini_response(query)
        api_data = fetch_custom_api_data()
    
    st.subheader("Response Received")
    
    # Display verdict and response from Gemini
    for chunk in response:
        st.write("Verdict: Misleading")  # Example verdict
        st.markdown(f'<div class="bot-message">{chunk.text}</div>', unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", chunk.text))
    
    # Display API data
    if "error" not in api_data:
        st.subheader("Detailed Information")
        st.write(api_data)
    else:
        st.write(api_data["error"])

# Section for Chatbot to ask questions
st.subheader("Ask Questions About the Product")
user_question = st.text_input("Ask a question about the product: ", key="user_question")
ask_question = st.button("Ask")

if ask_question and user_question:
    chat_response = get_gemini_response(user_question)
    
    st.subheader("Chatbot Response")
    for chunk in chat_response:
        st.markdown(f'<div class="bot-message">{chunk.text}</div>', unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Button to clear chat history
if st.button("Clear Chat History"):
    st.session_state['chat_history'] = []
    st.write("Chat history cleared.")

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    role_class = "bot-message" if role == "Bot" else "user-message"
    st.markdown(f'<div class="{role_class}">{role}: {text}</div>', unsafe_allow_html=True)









 