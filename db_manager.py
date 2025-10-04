import streamlit as st
import json
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="BeautyBoostr DB Manager",
    layout="wide"
)

# --- Constants ---
DB_FILE_PATH = 'data/ingredients.json'

# --- Data Loading ---
def load_ingredients_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Помилка завантаження файлу бази даних: {e}")
        return None

# --- Main App ---
st.title("🌿 BeautyBoostr: Менеджер бази даних інгредієнтів")
st.markdown("---")

# Initialize session state for dynamic functions list
if 'functions' not in st.session_state:
    st.session_state.functions = [{
        "IF_Percent": "", "IF_pH": "", "Target": "", "Function": ""
    }]

# Create tabs for different actions
tab1, tab2 = st.tabs(["📜 Перегляд та Пошук", "➕ Додати Новий Інгредієнт"])


# --- TAB 1: View & Search Ingredients ---
with tab1:
    ingredients_data = load_ingredients_data(DB_FILE_PATH)
    if ingredients_data:
        st.header("Перегляд існуючих інгредієнтів")
        search_term = st.text_input("Пошук за назвою INCI:", placeholder="Наприклад, Aqua")

        filtered_ingredients = [
            ing for ing in ingredients_data
            if search_term.lower() in ing.get("INCI", "").lower()
        ]

        if not filtered_ingredients:
            st.warning("Інгредієнти, що відповідають вашому пошуку, не знайдені.")
        else:
            st.info(f"Показано {len(filtered_ingredients)} з {len(ingredients_data)} інгредієнтів.")
            for ingredient in filtered_ingredients:
                with st.expander(f"**{ingredient.get('INCI', 'N/A')}** ({ingredient.get('Name_UA', 'N/A')})"):
                    st.write(f"**Походження:** {ingredient.get('Origin', 'Не вказано')}")
                    st.write(f"**Природа:** {ingredient.get('Nature', 'Не вказано')}")
                    st.write(f"**Обмеження:** {ingredient.get('Restrictions', 'Не вказано')}")
                    
                    st.subheader("Функції:")
                    for func in ingredient.get("Functions", []):
                        condition = f"Якщо % = [{func.get('IF_Percent', 'N/A')}] та pH = [{func.get('IF_pH', 'N/A')}]"
                        st.markdown(f"- **{func.get('Function', 'N/A')}** для **{func.get('Target', 'N/A')}** `({condition})`")


# --- TAB 2: Add New Ingredient Form ---
with tab2:
    st.header("Форма для додавання нового інгредієнта")
    st.markdown("Заповніть поля нижче. Коли закінчите, натисніть 'Згенерувати JSON', скопіюйте код і вставте його у ваш файл `data/ingredients.json` на GitHub.")

    with st.form("new_ingredient_form"):
        # Main ingredient details
        col1, col2 = st.columns(2)
        with col1:
            inci_name = st.text_input("**INCI Назва**", key="inci")
            origin = st.selectbox("**Походження**", ["Натуральне", "Синтетичне"], key="origin")
            physical_form = st.text_input("**Фізична форма**", key="physical_form")
            restrictions = st.text_area("**Обмеження**", key="restrictions")
        with col2:
            name_ua = st.text_input("**Назва (UA)**", key="name_ua")
            nature = st.selectbox("**Природа**", ["Органічна", "Неорганічна"], key="nature")
            ecology = st.selectbox("**Екологічність**", ["Екологічний", "Не екологічний"], key="ecology")
        
        st.subheader("Відсотки використання (%)")
        p_col1, p_col2, p_col3 = st.columns(3)
        with p_col1:
            usage_gel = st.text_input("Гель для вмивання", key="usage_gel")
        with p_col2:
            usage_cream = st.text_input("Крем", key="usage_cream")
        with p_col3:
            usage_tonic = st.text_input("Тонік", key="usage_tonic")

        st.subheader("Функції інгредієнта")
        
        # Dynamic function forms
        for i, func in enumerate(st.session_state.functions):
            st.markdown(f"--- \n #### Функція #{i+1}")
            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
            with f_col1:
                func['IF_Percent'] = st.text_input("Якщо %", key=f"if_percent_{i}")
            with f_col2:
                func['IF_pH'] = st.text_input("Якщо pH", key=f"if_ph_{i}")
            with f_col3:
                func['Target'] = st.text_input("Призначення (THEN)", key=f"target_{i}")
            with f_col4:
                func['Function'] = st.text_input("Функція", key=f"function_{i}")
        
        # Buttons to add/remove function blocks
        b_col1, b_col2, _ = st.columns([1, 1, 5])
        if b_col1.button("Додати ще одну функцію"):
            st.session_state.functions.append({"IF_Percent": "", "IF_pH": "", "Target": "", "Function": ""})
            st.experimental_rerun()
        if b_col2.button("Видалити останню функцію") and len(st.session_state.functions) > 1:
            st.session_state.functions.pop()
            st.experimental_rerun()

        submitted = st.form_submit_button("✅ Згенерувати JSON")

        if submitted:
            # Gather all data into a dictionary
            new_ingredient = {
                "INCI": inci_name,
                "Name_UA": name_ua,
                "Origin": origin,
                "Nature": nature,
                "Physical_Form": physical_form,
                "Ecology": ecology,
                "Restrictions": restrictions,
                "Usage_Percentages": {
                    "Cleansing_Gel": usage_gel or None,
                    "Cream": usage_cream or None,
                    "Tonic": usage_tonic or None
                },
                "Functions": st.session_state.functions
            }
            
            # Convert to JSON string
            # ensure_ascii=False is important for Cyrillic characters
            json_output = json.dumps(new_ingredient, indent=2, ensure_ascii=False)
            
            st.subheader("🎉 Готово! Ваш JSON-код:")
            st.code(json_output, language='json')
            st.warning("Тепер скопіюйте цей код і додайте його до списку у файлі `data/ingredients.json` на GitHub.")

