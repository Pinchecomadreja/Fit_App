import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
from pathlib import Path

# Import custom modules (suppress any debug output)
import sys
from io import StringIO

# Capture any unwanted print outputs during imports
old_stdout = sys.stdout
sys.stdout = StringIO()

try:
    from pages import login, dashboard, profile, routine_viewer
    from utils import api_client, data_handler
finally:
    sys.stdout = old_stdout

# Configure page
st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
.stDecoration {display:none;}

/* Clean interface styling */
.main .block-container {
    padding-top: 1rem;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86C1;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E86C1;
        margin: 1rem 0;
    }
    .sidebar-section {
        background-color: #EBF5FB;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def handle_url_navigation():
    """Handle URL-based navigation for direct links"""
    try:
        # Get query parameters from URL (compatible with older Streamlit versions)
        try:
            query_params = st.experimental_get_query_params()
        except AttributeError:
            # If experimental_get_query_params doesn't exist, return empty dict
            query_params = {}
        
        # URL to page mapping
        url_routes = {
            'login': 'login',
            'dashboard': 'dashboard',
            'profile': 'profile', 
            'routine_viewer': 'routine_viewer',
            'settings': 'settings'
        }
        
        # Check if there's a page parameter in URL (?page=dashboard)
        if 'page' in query_params:
            page = query_params['page'][0]  # experimental_get_query_params returns lists
            if page in url_routes:
                st.session_state.current_page = url_routes[page]
                return True
        
        # Handle direct URLs like /dashboard by using a custom component
        # This will inject JavaScript to detect the URL path
        if 'url_detected' not in st.session_state:
            detect_url_path()
        
        # If no specific page is detected, default to dashboard for authenticated users
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "dashboard"
        
        return False
        
    except Exception as e:
        # If URL handling fails, ensure we have a valid page
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "dashboard"
        return False

def detect_url_path():
    """Detect URL path using JavaScript - Simplified version"""
    try:
        # Simple JavaScript that works with any Streamlit version
        st.markdown("""
        <script>
        (function() {
            if (window.urlChecked) return; // Only run once
            
            const path = window.location.pathname;
            const search = window.location.search;
            const validPaths = ['login', 'dashboard', 'profile', 'routine_viewer', 'settings'];
            
            // Extract the last segment of the path
            const segments = path.split('/').filter(s => s);
            const lastSegment = segments[segments.length - 1];
            
            // Check if we need to redirect based on URL
            if (validPaths.includes(lastSegment) && !search.includes('page=')) {
                // Redirect to add query parameter
                const newUrl = window.location.origin + window.location.pathname + '?page=' + lastSegment;
                window.location.href = newUrl;
            } else if ((path === '/' || path === '') && !search.includes('page=')) {
                // Default to dashboard
                const newUrl = window.location.origin + '/?page=dashboard';
                window.location.href = newUrl;
            }
            
            window.urlChecked = true;
        })();
        </script>
        """, unsafe_allow_html=True)
        
        st.session_state.url_detected = True
        
    except Exception:
        pass

def update_url_for_page(page):
    """Update URL when page changes"""
    try:
        # Update query parameters (compatible with older Streamlit)
        try:
            st.experimental_set_query_params(page=page)
        except AttributeError:
            # If experimental functions don't exist, just update browser URL
            pass
        
        # Also update the browser URL path for clean URLs
        st.markdown(f"""
        <script>
        (function() {{
            const newUrl = new URL(window.location);
            newUrl.pathname = '/{page}';
            newUrl.searchParams.set('page', '{page}');
            window.history.pushState({{}}, '', newUrl);
        }})();
        </script>
        """, unsafe_allow_html=True)
        
    except Exception:
        pass

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"  # Default to dashboard
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    # Handle URL-based navigation
    handle_url_navigation()

def main():
    """Main application function"""
    initialize_session_state()
    
    # Check if user is accessing login page specifically
    try:
        query_params = st.experimental_get_query_params()
        page_param = query_params.get('page', [None])[0]
    except AttributeError:
        page_param = None
    
    if page_param == 'login':
        st.session_state.authenticated = False
        st.session_state.current_page = "login"
    
    # Auto-login for demo purposes (unless specifically going to login)
    elif not st.session_state.authenticated:
        # Auto-authenticate demo user for easier navigation
        st.session_state.authenticated = True
        st.session_state.username = "demo"
        st.session_state.user_data = {
            "name": "Usuario Demo",
            "email": "demo@rochi.com", 
            "age": 28,
            "height": 175,
            "weight": 75,
            "fitness_level": "Intermedio"
        }
        # Ensure URL is updated to reflect authentication
        if st.session_state.current_page != "login":
            update_url_for_page(st.session_state.current_page)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/2E86C1/FFFFFF?text=ROCHI", width=200)
        st.markdown("---")
        
        if st.session_state.authenticated:
            st.success(f"¡Hola, {st.session_state.username}!")
            
            # Navigation menu with better selection logic
            pages = {
                "🏠 Dashboard": "dashboard",
                "👤 Perfil": "profile", 
                "📋 Rutina del Día": "routine_viewer",
                "🔧 Configuración": "settings"
            }
            
            # Find current page index
            current_index = 0
            page_list = list(pages.keys())
            current_page_value = st.session_state.current_page
            
            for i, (key, value) in enumerate(pages.items()):
                if value == current_page_value:
                    current_index = i
                    break
            
            selected_page = st.selectbox(
                "Navegación",
                page_list,
                index=current_index,
                key="nav_selectbox"
            )
            
            # Update current page only if selection changed
            new_page = pages[selected_page]
            if new_page != st.session_state.current_page:
                st.session_state.current_page = new_page
                update_url_for_page(new_page)
                st.rerun()
            
            st.markdown("---")
            
            # Login/Logout buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Cambiar Usuario", use_container_width=True):
                    show_user_selector()
            
            with col2:
                if st.button("🚪 Cerrar Sesión", use_container_width=True):
                    logout()
        else:
            st.session_state.current_page = "login"
    
    # Main content area - always show content
    show_main_content()

def show_home_or_login():
    """Show home page or login form"""
    # If user just logged in, redirect to dashboard
    if st.session_state.authenticated:
        st.session_state.current_page = "dashboard"
        st.rerun()
    
    tab1, tab2 = st.tabs(["🏠 Inicio", "🔐 Iniciar Sesión"])
    
    with tab1:
        show_home_page()
    
    with tab2:
        login.show_login_page()

def show_home_page():
    """Show the home/landing page"""
    st.markdown('<h1 class="main-header">💪 Bienvenido a Fitness Tracker</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Seguimiento Personal</h3>
            <p>Rastrea tus rutinas diarias y progreso de ejercicios de forma intuitiva.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Visualización de Datos</h3>
            <p>Gráficos interactivos para ver tu evolución y estadísticas detalladas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🏋️ Rutinas Personalizadas</h3>
            <p>Crea y gestiona rutinas adaptadas a tus objetivos fitness.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("👈 **Inicia sesión desde la barra lateral para acceder a todas las funcionalidades**")

def show_user_selector():
    """Show user selection modal"""
    st.session_state.show_user_modal = True

def show_main_content():
    """Show main content based on current page and authentication"""
    
    # Debug info removed for production
    
    # Show user selector modal if needed
    if st.session_state.get('show_user_modal', False):
        with st.container():
            st.markdown("### 👤 Seleccionar Usuario")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                users = {
                    "demo": "Usuario Demo",
                    "rocio": "Rocío Fitness"
                }
                
                selected_user = st.selectbox(
                    "Elegir usuario:",
                    list(users.keys()),
                    format_func=lambda x: users[x]
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Confirmar", use_container_width=True):
                        switch_user(selected_user)
                        st.session_state.show_user_modal = False
                        st.rerun()
                
                with col_b:
                    if st.button("❌ Cancelar", use_container_width=True):
                        st.session_state.show_user_modal = False
                        st.rerun()
        return
    
    # Ensure we always have a valid page
    valid_pages = ["dashboard", "profile", "routine_viewer", "settings", "login"]
    if st.session_state.current_page not in valid_pages:
        st.session_state.current_page = "dashboard"
    
    # Show content based on authentication and current page
    if not st.session_state.authenticated:
        show_home_or_login()
    else:
        show_authenticated_content()

def switch_user(username):
    """Switch to different user"""
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
            "name": "Rocío Escalda",
            "email": "rocio@rochi.com",
            "age": 25,
            "height": 165,
            "weight": 60,
            "fitness_level": "Avanzado"
        }
    }
    
    st.session_state.username = username
    st.session_state.user_data = mock_profiles.get(username, mock_profiles["demo"])
    st.success(f"¡Cambiado a {st.session_state.user_data['name']}!")

def show_authenticated_content():
    """Show content for authenticated users"""
    try:
        if st.session_state.current_page == "dashboard":
            dashboard.show_dashboard()
        elif st.session_state.current_page == "profile":
            profile.show_profile()
        elif st.session_state.current_page == "routine_viewer":
            routine_viewer.show_routine_viewer()
        elif st.session_state.current_page == "settings":
            show_settings()
        elif st.session_state.current_page == "login":
            show_home_or_login()
        else:
            # Default fallback to dashboard
            st.session_state.current_page = "dashboard"
            dashboard.show_dashboard()
    except Exception as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Redirecting to dashboard...")
        st.session_state.current_page = "dashboard"
        dashboard.show_dashboard()

def show_settings():
    """Show settings page"""
    st.header("🔧 Configuración")
    
    with st.expander("⚙️ Preferencias de Usuario"):
        language = st.selectbox("Idioma", ["Español", "English"])
        notifications = st.checkbox("Recibir notificaciones", value=True)
    
    with st.expander("📊 Configuración de Datos"):
        sync_api = st.checkbox("Sincronizar con API", value=True)
        export_format = st.selectbox("Formato de exportación", ["CSV", "JSON", "Excel"])
    
    if st.button("💾 Guardar Configuración"):
        st.success("✅ Configuración guardada exitosamente!")

def logout():
    """Handle user logout"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.user_data = {}
    st.session_state.current_page = "login"
    update_url_for_page("login")
    st.rerun()

if __name__ == "__main__":
    main() 
