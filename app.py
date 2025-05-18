import streamlit as st
import pandas as pd
import numpy as np
import pickle

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('model_columns.pkl', 'rb') as file:
    model_columns = pickle.load(file)

st.title('Earthquake Damage Prediction')

geo_level_1_id = st.number_input('Wilayah Level 1', value=1)
geo_level_2_id = st.number_input('Wilayah Level 2', value=1)
geo_level_3_id = st.number_input('Wilayah Level 3', value=1)
jumlah_lantai = st.number_input('Jumlah Lantai', value=1)
umur_bangunan = st.number_input('Umur Bangunan', value=1)
luas_area = st.number_input('Luas Area (%)', value=1)
persentase_tinggi = st.number_input('Persentase Tinggi (%)', value=1)

land_surface_condition_map = {
    "Flat": "n",
    "Obstructed": "o",
    "Sloped": "t"
}
foundation_type_map = {
    "Rock": "r",
    "Unreinforced Masonry": "u",
    "Wood": "w",
    "Mud": "i",
    "Other": "h"
}
roof_type_map = {
    "Nepa": "n",
    "Quake Resistant": "q",
    "Other": "x"
}
ground_floor_type_map = {
    "Flagstone": "f",
    "Mud": "m",
    "Veneer": "v",
    "Other": "x"
}
other_floor_type_map = {
    "Quake Resistant": "q",
    "Stone": "s",
    "Other": "x"
}
position_map = {
    "Attached": "j",
    "Other": "o",
    "Separated": "s",
    "T-shaped": "t"
}
plan_configuration_map = {
    "Rectangular": "a",
    "Square": "c",
    "L-shape": "d",
    "T-shape": "f",
    "U-shape": "m",
    "H-shape": "n",
    "Multi-projected": "o",
    "Irregular": "q",
    "E-shape": "s",
    "Other": "u"
}

kondisi_permukaan_tanah = st.selectbox('Kondisi Permukaan Tanah', list(land_surface_condition_map.keys()))
tipe_fondasi = st.selectbox('Tipe Fondasi', list(foundation_type_map.keys()))
tipe_atap = st.selectbox('Tipe Atap', list(roof_type_map.keys()))
lantai_dasar = st.selectbox('Tipe Lantai Dasar', list(ground_floor_type_map.keys()))
lantai_lain = st.selectbox('Tipe Lantai Lain', list(other_floor_type_map.keys()))
posisi = st.selectbox('Posisi', list(position_map.keys()))
konfigurasi_rencana = st.selectbox('Konfigurasi Rencana', list(plan_configuration_map.keys()))

superstruktur_adobe_mud = st.selectbox('Superstruktur Adobe/Mud', [0, 1])
superstruktur_mud_mortar_stone = st.selectbox('Superstruktur Batu/Mortar Lumpur', [0, 1])
superstruktur_stone_flag = st.selectbox('Superstruktur Batu Flag', [0, 1])
superstruktur_cement_mortar_stone = st.selectbox('Superstruktur Batu/Mortar Semen', [0, 1])
superstruktur_mud_mortar_brick = st.selectbox('Superstruktur Bata/Mortar Lumpur', [0, 1])
superstruktur_cement_mortar_brick = st.selectbox('Superstruktur Bata/Mortar Semen', [0, 1])
superstruktur_kayu = st.selectbox('Superstruktur Kayu', [0, 1])
superstruktur_bambu = st.selectbox('Superstruktur Bambu', [0, 1])
superstruktur_rc_non_engineered = st.selectbox('Superstruktur RC Non-Engineered', [0, 1])
superstruktur_rc_engineered = st.selectbox('Superstruktur RC Engineered', [0, 1])
superstruktur_lain = st.selectbox('Superstruktur Lain', [0, 1])
ada_secondary_use = st.selectbox('Ada Secondary Use', [0, 1])
secondary_use_pertanian = st.selectbox('Secondary Use Pertanian', [0, 1])
secondary_use_hotel = st.selectbox('Secondary Use Hotel', [0, 1])
secondary_use_rental = st.selectbox('Secondary Use Rental', [0, 1])
secondary_use_institusi = st.selectbox('Secondary Use Institusi', [0, 1])
secondary_use_sekolah = st.selectbox('Secondary Use Sekolah', [0, 1])
secondary_use_industri = st.selectbox('Secondary Use Industri', [0, 1])
secondary_use_puskesmas = st.selectbox('Secondary Use Puskesmas', [0, 1])
secondary_use_kantor_pemerintah = st.selectbox('Secondary Use Kantor Pemerintah', [0, 1])
secondary_use_polisi = st.selectbox('Secondary Use Polisi', [0, 1])
secondary_use_lain = st.selectbox('Secondary Use Lain', [0, 1])

age_x_area = umur_bangunan * luas_area
age_x_height = umur_bangunan * persentase_tinggi
floors_x_area = jumlah_lantai * luas_area
floors_x_height = jumlah_lantai * persentase_tinggi
area_per_floor = luas_area / (jumlah_lantai + 1)
height_per_floor = persentase_tinggi / (jumlah_lantai + 1)
area_to_height = luas_area / (persentase_tinggi + 1)
foundation_roof_combo = foundation_type_map[tipe_fondasi] + '_' + roof_type_map[tipe_atap]

if st.button('Predict'):
    input_dict = {
        'geo_level_1_id': geo_level_1_id,
        'geo_level_2_id': geo_level_2_id,
        'geo_level_3_id': geo_level_3_id,
        'count_floors_pre_eq': jumlah_lantai,
        'age': umur_bangunan,
        'area_percentage': luas_area,
        'height_percentage': persentase_tinggi,
        'land_surface_condition': land_surface_condition_map[kondisi_permukaan_tanah],
        'foundation_type': foundation_type_map[tipe_fondasi],
        'roof_type': roof_type_map[tipe_atap],
        'ground_floor_type': ground_floor_type_map[lantai_dasar],
        'other_floor_type': other_floor_type_map[lantai_lain],
        'position': position_map[posisi],
        'plan_configuration': plan_configuration_map[konfigurasi_rencana],
        'has_superstructure_adobe_mud': superstruktur_adobe_mud,
        'has_superstructure_mud_mortar_stone': superstruktur_mud_mortar_stone,
        'has_superstructure_stone_flag': superstruktur_stone_flag,
        'has_superstructure_cement_mortar_stone': superstruktur_cement_mortar_stone,
        'has_superstructure_mud_mortar_brick': superstruktur_mud_mortar_brick,
        'has_superstructure_cement_mortar_brick': superstruktur_cement_mortar_brick,
        'has_superstructure_timber': superstruktur_kayu,
        'has_superstructure_bamboo': superstruktur_bambu,
        'has_superstructure_rc_non_engineered': superstruktur_rc_non_engineered,
        'has_superstructure_rc_engineered': superstruktur_rc_engineered,
        'has_superstructure_other': superstruktur_lain,
        'has_secondary_use': ada_secondary_use,
        'has_secondary_use_agriculture': secondary_use_pertanian,
        'has_secondary_use_hotel': secondary_use_hotel,
        'has_secondary_use_rental': secondary_use_rental,
        'has_secondary_use_institution': secondary_use_institusi,
        'has_secondary_use_school': secondary_use_sekolah,
        'has_secondary_use_industry': secondary_use_industri,
        'has_secondary_use_health_post': secondary_use_puskesmas,
        'has_secondary_use_gov_office': secondary_use_kantor_pemerintah,
        'has_secondary_use_use_police': secondary_use_polisi,
        'has_secondary_use_other': secondary_use_lain,
        'foundation_roof_combo': foundation_roof_combo,
        'age_x_area': age_x_area,
        'age_x_height': age_x_height,
        'floors_x_area': floors_x_area,
        'floors_x_height': floors_x_height,
        'area_per_floor': area_per_floor,
        'height_per_floor': height_per_floor,
        'area_to_height': area_to_height
    }
    input_df = pd.DataFrame([input_dict])
    categorical_cols = [
        'land_surface_condition', 'foundation_type', 'roof_type',
        'ground_floor_type', 'other_floor_type', 'position', 'plan_configuration',
        'foundation_roof_combo'
    ]
    input_df = pd.get_dummies(input_df, columns=categorical_cols)
    for col in model_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[model_columns]
    try:
        prediction = model.predict(input_df)
        probs = model.predict_proba(input_df)
        st.write(f'Probabilities: {probs}')
        grade = int(prediction[0]) + 1
        if grade == 1:
            grade_label = "Low"
        elif grade == 2:
            grade_label = "Medium"
        elif grade == 3:
            grade_label = "High"
        else:
            grade_label = "Unknown"
        st.write(f'Predicted damage grade: {grade} ({grade_label})')
    except Exception as e:
        st.error(f"Error in prediction: {e}")