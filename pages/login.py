import streamlit as st
import hashlib
import json
import pandas as pd
from pathlib import Path

def show_login_page():
    """Display the login page with authentication"""
    st.markdown('<h2 style="text-align: center; color: #2E86C1;">🔐 Iniciar Sesión</h2>', unsafe_allow_html=True)
    
    # Create login form
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("---")
            username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("🔒 Contraseña", type="password", placeholder="Ingresa tu contraseña")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_button = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
            
            with col_register:
                register_button = st.form_submit_button("📝 Registrarse", use_container_width=True)
    
    # Handle login
    if login_button:
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_data = load_user_data(username)
            st.success(f"¡Bienvenido, {username}!")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")
    
    # Handle registration
    if register_button:
        if username and password:
            if register_user(username, password):
                st.success("✅ Usuario registrado exitosamente. ¡Ahora puedes iniciar sesión!")
            else:
                st.error("❌ El usuario ya existe")
        else:
            st.error("❌ Por favor, completa todos los campos")
    


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users_file = Path("data/users.json")
    
    # Mock credentials for testing
    mock_users = {
        "demo": "demo123",
        "rocio": "password123"
    }
    
    # Check mock credentials first
    if username in mock_users and password == mock_users[username]:
        return True
    
    # Create demo user if file doesn't exist
    if not users_file.exists():
        create_demo_data()
    
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        if username in users:
            return users[username]['password'] == hash_password(password)
        return False
    except:
        return False

def register_user(username, password):
    """Register a new user"""
    users_file = Path("data/users.json")
    users_file.parent.mkdir(exist_ok=True)
    
    try:
        if users_file.exists():
            with open(users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}
        
        if username not in users:
            users[username] = {
                'password': hash_password(password),
                'created_at': str(pd.Timestamp.now()),
                'profile': {
                    'name': username,
                    'email': '',
                    'age': 25,
                    'height': 170,
                    'weight': 70,
                    'fitness_level': 'Intermedio'
                }
            }
            
            with open(users_file, 'w') as f:
                json.dump(users, f, indent=2)
            
            # Create user data directory
            create_user_data(username)
            return True
        return False
    except Exception as e:
        st.error(f"Error al registrar usuario: {str(e)}")
        return False

def load_user_data(username):
    """Load user profile data"""
    users_file = Path("data/users.json")
    
    # Mock user profiles
    mock_profiles = {
        "demo": {
            "name": "Usuario Demo",
            "email": "demo@rochi.com", 
            "age": 28,
            "height": 175,
            "weight": 75,
            "fitness_level": "Intermedio"
        },
        "rocio": {
            "name": "Rocío Fitness",
            "email": "rocio@rochi.com",
            "age": 25,
            "height": 165,
            "weight": 60,
            "fitness_level": "Avanzado"
        }
    }
    
    # Check mock profiles first
    if username in mock_profiles:
        return mock_profiles[username]
    
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
        
        if username in users:
            return users[username].get('profile', {})
        
        # Return demo data if user not found
        return get_demo_profile()
    except:
        return get_demo_profile()

def create_demo_data():
    """Create demo data for testing"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    users = {
        "demo": {
            "password": hash_password("demo123"),
            "created_at": "2024-01-01T00:00:00",
            "profile": {
                "name": "Usuario Demo",
                "email": "demo@rochi.com",
                "age": 28,
                "height": 175,
                "weight": 75,
                "fitness_level": "Intermedio"
            }
        }
    }
    
    with open(data_dir / "users.json", 'w') as f:
        json.dump(users, f, indent=2)

def get_demo_profile():
    """Get demo profile data"""
    return {
        "name": "Usuario Demo",
        "email": "demo@rochi.com", 
        "age": 28,
        "height": 175,
        "weight": 75,
        "fitness_level": "Intermedio"
    }

def create_user_data(username):
    """Create initial user data files using JSON"""
    import pandas as pd
    
    data_dir = Path(f"data/{username}")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample workout data
    sample_workouts = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'exercise': ['Push-ups', 'Squats', 'Planks'] * 10,
        'sets': [3, 4, 1] * 10,
        'reps': [15, 20, 60] * 10,
        'weight': [0, 0, 0] * 10,
        'duration_minutes': [10, 15, 5] * 10
    })
    
    # Convert to JSON format
    workouts_json = sample_workouts.to_dict('records')
    
    # Convert dates to ISO format for JSON compatibility
    for workout in workouts_json:
        workout['date'] = workout['date'].strftime('%Y-%m-%d')
    
    # Save as JSON
    with open(data_dir / "workouts.json", 'w') as f:
        json.dump(workouts_json, f, indent=2) 