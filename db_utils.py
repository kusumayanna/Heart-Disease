"""
Database utilities for Heart Disease Classification Project
Uses PostgreSQL database on Render
"""

import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_connection():
    """
    Get PostgreSQL database connection from Render.
    """
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    if not database_url.startswith("postgresql://"):
        raise ValueError("DATABASE_URL must be a PostgreSQL connection string")
    
    try:
        import psycopg2
        # Add SSL configuration for Render if not present
        if "?sslmode=" not in database_url:
            database_url = database_url + "?sslmode=require"
        conn = psycopg2.connect(database_url)
        return conn
    except ImportError:
        raise ImportError("psycopg2 not installed. Install with: pip install psycopg2-binary")
    except Exception as e:
        raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")

def load_heart_data():
    """
    Load heart disease data from the PostgreSQL database.
    """
    conn = get_database_connection()
    
    try:
        # Use the ML view for easy data access
        query = "SELECT * FROM patient_ml_data"
        df = pd.read_sql_query(query, conn)
        print(f"✓ Loaded {len(df)} patients from PostgreSQL database")
        return df
        
    finally:
        conn.close()

def get_database_info():
    """Get information about the current database configuration"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        return {
            "type": "Not Configured",
            "location": "Unknown",
            "error": "DATABASE_URL not found in environment"
        }
    
    return {
        "type": "PostgreSQL",
        "location": "Render Cloud",
        "url": database_url.split("@")[1] if "@" in database_url else "configured"
    }

def test_database_connection():
    """Test PostgreSQL database connection and return basic info"""
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM patient_ml_data")
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "success": True,
            "database_type": "postgresql",
            "version": version,
            "patient_count": count
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "database_type": None
        }

if __name__ == "__main__":
    # Test the database connection
    print("🔍 Testing PostgreSQL database connection...")
    
    info = get_database_info()
    print(f"Database type: {info['type']}")
    print(f"Location: {info['location']}")
    
    test_result = test_database_connection()
    if test_result["success"]:
        print(f"✅ Connection successful!")
        print(f"   Database: {test_result['database_type'].upper()}")
        print(f"   Version: {test_result['version']}")
        print(f"   Patients: {test_result['patient_count']}")
    else:
        print(f"❌ Connection failed: {test_result['error']}")
        exit(1)
    
    # Test data loading
    try:
        print("\n📊 Testing data loading...")
        df = load_heart_data()
        print(f"✅ Data loaded successfully: {len(df)} rows")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Target distribution: {df['target'].value_counts().to_dict()}")
    except Exception as e:
        print(f"❌ Data loading failed: {e}")