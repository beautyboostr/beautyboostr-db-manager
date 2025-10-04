import streamlit as st
import json
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="BeautyBoostr DB Viewer",
    layout="wide"
)

# --- Constants ---
# The path is relative to the root of the repository
DB_FILE_PATH = 'data/ingredients.json'

# --- Data Loading ---
# We don't need caching here for the cloud version
def load_ingredients_data(filepath):
    """
    Loads the ingredients database from the specified file path.
    """
    try:
        # Streamlit cloud can't access local files the same way,
        # but it can read from the repo structure.
        # For robustness, we will assume the file exists.
        # Error handling will be simpler.
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading the database file: {e}")
        return None

# --- Main App ---
st.title("🌿 BeautyBoostr Ingredient Database Viewer")
st.markdown("---")

# Load the data
ingredients_data = load_ingredients_data(DB_FILE_PATH)

if ingredients_data is not None:
    st.success(f"Successfully loaded the database. Found {len(ingredients_data)} ingredients.")
    
    st.markdown("## 📜 View & Search Ingredients")

    # --- Search Functionality ---
    search_term = st.text_input("Search by INCI Name:", placeholder="e.g., Glycerin")

    # --- Display Data ---
    filtered_ingredients = [
        ing for ing in ingredients_data
        if search_term.lower() in ing.get("INCI Name", "").lower()
    ]

    if not filtered_ingredients:
        st.warning("No ingredients found matching your search.")
    else:
        st.info(f"Showing {len(filtered_ingredients)} of {len(ingredients_data)} ingredients.")
        # Displaying each ingredient in an expander
        for index, ingredient in enumerate(filtered_ingredients):
            with st.expander(f"**{ingredient.get('INCI Name', 'N/A')}**"):
                st.write(f"**Function:** {ingredient.get('Function', 'Not specified')}")
                st.write(f"**Description:** {ingredient.get('Description', 'Not specified')}")

else:
    st.error("Could not load the database. The application cannot proceed.")
