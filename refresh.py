import sqlite3
import pandas as pd

conn = sqlite3.connect("food_management.db")
cursor = conn.cursor()

print("Creating tables...")
cursor.execute("CREATE TABLE IF NOT EXISTS providers (Provider_ID INTEGER PRIMARY KEY, Name TEXT, Type TEXT, Address TEXT, City TEXT, Contact TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS receivers (Receiver_ID INTEGER PRIMARY KEY, Name TEXT, Type TEXT, City TEXT, Contact TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS food_listings (Food_ID INTEGER PRIMARY KEY, Food_Name TEXT, Quantity INTEGER, Expiry_Date TEXT, Provider_ID INTEGER, Provider_Type TEXT, Location TEXT, Food_Type TEXT, Meal_Type TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS claims (Claim_ID INTEGER PRIMARY KEY, Food_ID INTEGER, Receiver_ID INTEGER, Status TEXT, Timestamp TEXT)")
conn.commit()

try:
    pd.read_csv("providers_data.csv").to_sql("providers", conn, if_exists="replace", index=False)
    pd.read_csv("receivers_data.csv").to_sql("receivers", conn, if_exists="replace", index=False)
    pd.read_csv("food_listings_data.csv").to_sql("food_listings", conn, if_exists="replace", index=False)
    pd.read_csv("claims_data.csv").to_sql("claims", conn, if_exists="replace", index=False)
    print("✅ Data successfully loaded into SQL database!")
except Exception as e:
    print(f"Error: {e}")

conn.close()