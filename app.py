import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model_columns.pkl', 'rb') as file:
    model_columns = pickle.load(file)

st.title('Earthquake Damage Prediction')

# Numeric features
geo_level_1_id = st.number_input('geo_level_1_id', value=1)
geo_level_2_id = st.number_input('geo_level_2_id', value=1)
geo_level_3_id = st.number_input('geo_level_3_id', value=1)
count_floors_pre_eq = st.number_input('count_floors_pre_eq', value=1)
age = st.number_input('age', value=1)
area_percentage = st.number_input('area_percentage', value=1)
height_percentage = st.number_input('height_percentage', value=1)

# Categorical features
land_surface_condition = st.selectbox('land_surface_condition', ['n', 'o', 't'])
foundation_type = st.selectbox('foundation_type', ['r', 'u', 'w', 'i', 'h'])
roof_type = st.selectbox('roof_type', ['n', 'q', 'x'])
ground_floor_type = st.selectbox('ground_floor_type', ['f', 'm', 'v', 'x'])
other_floor_type = st.selectbox('other_floor_type', ['q', 's', 'x'])
position = st.selectbox('position', ['j', 'o', 's', 't'])
plan_configuration = st.selectbox('plan_configuration', ['a', 'c', 'd', 'f', 'm', 'n', 'o', 'q', 's', 'u'])

# Binary features
has_superstructure_adobe_mud = st.selectbox('has_superstructure_adobe_mud', [0, 1])
has_superstructure_mud_mortar_stone = st.selectbox('has_superstructure_mud_mortar_stone', [0, 1])
has_superstructure_stone_flag = st.selectbox('has_superstructure_stone_flag', [0, 1])
has_superstructure_cement_mortar_stone = st.selectbox('has_superstructure_cement_mortar_stone', [0, 1])
has_superstructure_mud_mortar_brick = st.selectbox('has_superstructure_mud_mortar_brick', [0, 1])
has_superstructure_cement_mortar_brick = st.selectbox('has_superstructure_cement_mortar_brick', [0, 1])
has_superstructure_timber = st.selectbox('has_superstructure_timber', [0, 1])
has_superstructure_bamboo = st.selectbox('has_superstructure_bamboo', [0, 1])
has_superstructure_rc_non_engineered = st.selectbox('has_superstructure_rc_non_engineered', [0, 1])
has_superstructure_rc_engineered = st.selectbox('has_superstructure_rc_engineered', [0, 1])
has_superstructure_other = st.selectbox('has_superstructure_other', [0, 1])
has_secondary_use = st.selectbox('has_secondary_use', [0, 1])
has_secondary_use_agriculture = st.selectbox('has_secondary_use_agriculture', [0, 1])
has_secondary_use_hotel = st.selectbox('has_secondary_use_hotel', [0, 1])
has_secondary_use_rental = st.selectbox('has_secondary_use_rental', [0, 1])
has_secondary_use_institution = st.selectbox('has_secondary_use_institution', [0, 1])
has_secondary_use_school = st.selectbox('has_secondary_use_school', [0, 1])
has_secondary_use_industry = st.selectbox('has_secondary_use_industry', [0, 1])
has_secondary_use_health_post = st.selectbox('has_secondary_use_health_post', [0, 1])
has_secondary_use_gov_office = st.selectbox('has_secondary_use_gov_office', [0, 1])
has_secondary_use_use_police = st.selectbox('has_secondary_use_use_police', [0, 1])
has_secondary_use_other = st.selectbox('has_secondary_use_other', [0, 1])

if st.button('Predict'):
    input_dict = {
        'geo_level_1_id': geo_level_1_id,
        'geo_level_2_id': geo_level_2_id,
        'geo_level_3_id': geo_level_3_id,
        'count_floors_pre_eq': count_floors_pre_eq,
        'age': age,
        'area_percentage': area_percentage,
        'height_percentage': height_percentage,
        'land_surface_condition': land_surface_condition,
        'foundation_type': foundation_type,
        'roof_type': roof_type,
        'ground_floor_type': ground_floor_type,
        'other_floor_type': other_floor_type,
        'position': position,
        'plan_configuration': plan_configuration,
        'has_superstructure_adobe_mud': has_superstructure_adobe_mud,
        'has_superstructure_mud_mortar_stone': has_superstructure_mud_mortar_stone,
        'has_superstructure_stone_flag': has_superstructure_stone_flag,
        'has_superstructure_cement_mortar_stone': has_superstructure_cement_mortar_stone,
        'has_superstructure_mud_mortar_brick': has_superstructure_mud_mortar_brick,
        'has_superstructure_cement_mortar_brick': has_superstructure_cement_mortar_brick,
        'has_superstructure_timber': has_superstructure_timber,
        'has_superstructure_bamboo': has_superstructure_bamboo,
        'has_superstructure_rc_non_engineered': has_superstructure_rc_non_engineered,
        'has_superstructure_rc_engineered': has_superstructure_rc_engineered,
        'has_superstructure_other': has_superstructure_other,
        'has_secondary_use': has_secondary_use,
        'has_secondary_use_agriculture': has_secondary_use_agriculture,
        'has_secondary_use_hotel': has_secondary_use_hotel,
        'has_secondary_use_rental': has_secondary_use_rental,
        'has_secondary_use_institution': has_secondary_use_institution,
        'has_secondary_use_school': has_secondary_use_school,
        'has_secondary_use_industry': has_secondary_use_industry,
        'has_secondary_use_health_post': has_secondary_use_health_post,
        'has_secondary_use_gov_office': has_secondary_use_gov_office,
        'has_secondary_use_use_police': has_secondary_use_use_police,
        'has_secondary_use_other': has_secondary_use_other
    }
    input_df = pd.DataFrame([input_dict])
    categorical_cols = [
        'land_surface_condition', 'foundation_type', 'roof_type',
        'ground_floor_type', 'other_floor_type', 'position', 'plan_configuration'
    ]
    input_df = pd.get_dummies(input_df, columns=categorical_cols)
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_columns]
    try:
        prediction = model.predict(input_df)
        st.write('Predicted damage grade:', int(prediction[0]) + 1)
    except Exception as e:
        st.error(f"Error in prediction: {e}")