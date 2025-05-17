import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model_columns.pkl', 'rb') as file:
    model = pickle.load(file)

st.title('Earthquake Damage Prediction')

feature1 = st.number_input('Enter value for geo_level_1_id:', value=1)
feature2 = st.number_input('Enter value for geo_level_2_id:', value=1)
feature3 = st.number_input('Enter value for geo_level_3_id:', value=1)

if st.button('Predict'):
    # Create a DataFrame with all columns set to 0
    input_df = pd.DataFrame(np.zeros((1, len(model))), columns=model)
    # Set the user input values
    if 'geo_level_1_id' in input_df.columns:
        input_df['geo_level_1_id'] = feature1
    if 'geo_level_2_id' in input_df.columns:
        input_df['geo_level_2_id'] = feature2
    if 'geo_level_3_id' in input_df.columns:
        input_df['geo_level_3_id'] = feature3

    try:
        prediction = model.predict(input_df)
        st.write('Predicted damage grade:', int(prediction[0]) + 1)
    except Exception as e:
        st.error(f"Error in prediction: {e}")