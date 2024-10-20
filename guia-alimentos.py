import streamlit as st
import pandas as pd

# Load the CSV file
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to search for the string in the "Alimento" column
def search_food(df, search_term):
    matches = df[df['Alimento'].str.contains(search_term, case=False, na=False)]
    return matches

# Function to get rows with matching "Grupo" and "Subgrupo"
def get_similar_foods(df, grupo, subgrupo):
    similar_rows = df[(df['Grupo'] == grupo) & (df['Subgrupo'] == subgrupo)]
    return similar_rows

# Function to highlight matching rows
def highlight_matches(row, search_term):
    # If the search term is found in the 'Alimento' column, highlight the row
    highlight_color = 'background-color: lavender'
    default_color = ''
    
    # Check if the search term is in the current row's 'Alimento' column
    if search_term.lower() in row['Alimento'].lower():
        return [highlight_color] * len(row)
    else:
        return [default_color] * len(row)

# Streamlit app
def main():

    st.set_page_config(
        page_title="Guía de alimentos",
        page_icon="🍏",
        layout="wide",
    )

    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                h2{
                    padding-bottom: 0;
                }
                .stDeployButton, header, .viewerBadge_link__qRIco, .viewerBadge_container__r5tak styles_viewerBadge__CvC9N {
                    visibility: hidden !important;
                    display: none !important;
                }
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }

        </style>
        """, unsafe_allow_html=True)

    # Set the title of the app
    st.title("Guía de alimentos")

    # Input text for search term
    search_term = st.text_input("Ingrese el alimento a buscar")

    # Search button
    if st.button("Buscar"):
        # Load the CSV file
        data = load_data("data.csv")

        # Perform search
        results = search_food(data, search_term)

        # Display results if found
        if not results.empty:
            # Get unique "Grupo" and "Subgrupo" combinations from the results
            unique_groups = results[['Grupo', 'Subgrupo']].drop_duplicates()

            # Loop through each unique "Grupo" and "Subgrupo" combination
            for _, group in unique_groups.iterrows():

                st.divider()

                grupo = group['Grupo']
                subgrupo = group['Subgrupo']

                # Get all rows with the same "Grupo" and "Subgrupo"
                similar_foods = get_similar_foods(data, grupo, subgrupo)

                # Display nutritional information for the first match in this group
                st.header(f"{grupo}")
                st.subheader(f"{subgrupo}")
                first_match = similar_foods.iloc[0]
                st.table(first_match[['Energia', 'Hidratos', 'Grasa', 'Proteinas']])

                # Apply highlighting to the matching rows
                styled_similar_foods = similar_foods[['Alimento', 'Racion']].style.apply(highlight_matches, search_term=search_term, axis=1)

                # Display all similar foods and their portions for this group, with highlighted matches
                st.subheader(f"Alimentos similares:")
                st.dataframe(styled_similar_foods, hide_index=True, use_container_width=True)
                
        else:
            st.write("No se encontró el alimento")

# Run the app
if __name__ == "__main__":
    main()
