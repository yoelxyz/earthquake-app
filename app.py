import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Streamlit app
st.title('Earthquake Damage Prediction')

# Add input fields for new data prediction
feature1 = st.number_input('Enter value for geo_level_1_id:')
feature2 = st.number_input('Enter value for geo_level_2_id:')
feature3 = st.number_input('Enter value for geo_level_3_id:')
# Add more input fields as needed

# Predict button
if st.button('Predict'):
    # Prepare input data
    input_data = np.array([[feature1, feature2, feature3]])
    
    # Ensure input data matches the model's expected shape
    # Example: input_data = preprocess_input(input_data)
    
    try:
        # Make prediction
        prediction = model.predict(input_data)
        # Display prediction
        st.write('Predicted damage grade:', prediction[0] + 1)  # Adjust prediction to match original labels
    except ValueError as e:
        st.error(f"Error in prediction: {e}")