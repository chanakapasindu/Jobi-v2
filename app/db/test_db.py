from app.db.session import engine

def test_connection():
    try:
        conn = engine.connect()
        conn.close()
        print("✅ Database connected successfully")
    except Exception as e:
        print("❌ DB connection failed:", e)

if __name__ == "__main__":
    test_connection()
