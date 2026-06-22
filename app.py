import streamlit as st
import sqlite3
import pandas as pd

# Page title aur layout set karna
st.set_page_config(page_title="Food Wastage Management", layout="wide")

st.title("🥗 Local Food Wastage Management System")
st.markdown("Connecting surplus food providers to those in need. ❤️")

# Database connection helper function
def get_connection():
    return sqlite3.connect("food_management.db")

# -------------------------------------------------------------
# SIDEBAR - CRUD OPERATION (Naya Food Item Add Karna)
# -------------------------------------------------------------
st.sidebar.header("➕ Add New Food Listing (CRUD)")
with st.sidebar.form("food_form", clear_on_submit=True):
    food_name = st.text_input("Food Name (e.g., Roti, Rice)")
    quantity = st.number_input("Quantity (Portions)", min_value=1, value=10)
    expiry = st.date_input("Expiry Date")
    p_id = st.selectbox("Provider ID", [1, 2, 3])
    p_type = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket"])
    location = st.selectbox("City/Location", ["Mumbai", "Delhi", "Bangalore"])
    f_type = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
    
    submitted = st.form_submit_with_button("List Food Item")
    
    if submitted and food_name:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(Food_ID) FROM food_listings")
        max_id = cursor.fetchone()[0]
        new_id = (max_id if max_id else 500) + 1
        
        cursor.execute("""
            INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_id, food_name, int(quantity), str(expiry), p_id, p_type, location, f_type, meal_type))
        conn.commit()
        conn.close()
        st.sidebar.success(f"✅ {food_name} successfully list ho gaya!")

# -------------------------------------------------------------
# MAIN DASHBOARD - DATA DISPLAY & VISUALIZATION
# -------------------------------------------------------------
conn = get_connection()

tab1, tab2, tab3 = st.tabs(["📊 Food Dashboard", "🏢 Providers & Receivers", "📈 SQL Insights"])

with tab1:
    st.subheader("📍 Available Food Items in Real-time")
    col1, col2 = st.columns(2)
    with col1:
        city_filter = st.selectbox("Filter by City", ["All", "Mumbai", "Delhi", "Bangalore"])
    with col2:
        type_filter = st.selectbox("Filter by Food Type", ["All", "Vegetarian", "Non-Vegetarian", "Vegan"])
    
    query = "SELECT * FROM food_listings WHERE 1=1"
    params = []
    if city_filter != "All":
        query += " AND Location = ?"
        params.append(city_filter)
    if type_filter != "All":
        query += " AND Food_Type = ?"
        params.append(type_filter)
        
    df_food = pd.read_sql_query(query, conn, params=params)
    st.dataframe(df_food, use_container_width=True)

with tab2:
    st.subheader("📞 Registered Contacts & Network")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Food Providers:**")
        st.dataframe(pd.read_sql_query("SELECT * FROM providers", conn), use_container_width=True)
    with c2:
        st.write("**Food Receivers (NGOs/Individuals):**")
        st.dataframe(pd.read_sql_query("SELECT * FROM receivers", conn), use_container_width=True)

with tab3:
    st.subheader("💡 Business Analytics (SQL Output)")
    st.write("**City wise Food Listings Count:**")
    q_city = "SELECT Location as City, COUNT(Food_ID) as Total_Listings FROM food_listings GROUP BY Location ORDER BY Total_Listings DESC;"
    st.dataframe(pd.read_sql_query(q_city, conn))
    
    st.write("**Total Available Food Quantity (Sum):**")
    q_sum = "SELECT SUM(Quantity) as Total_Available_Food FROM food_listings;"
    st.dataframe(pd.read_sql_query(q_sum, conn))

conn.close()