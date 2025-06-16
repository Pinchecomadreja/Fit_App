import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

def show_profile():
    """Display user profile page with editable information"""
    st.markdown('<h1 style="text-align: center; color: #2E86C1;">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    
    # Load current user data
    user_data = st.session_state.get('user_data', {})
    username = st.session_state.get('username', 'demo')
    
    # Create tabs for different profile sections  
    tab1, tab2 = st.tabs(["📝 Información Personal", "🎯 Preferencias"])
    
    with tab1:
        show_personal_info(user_data, username)
    
    with tab2:
        show_preferences(username)

def show_personal_info(user_data, username):
    """Show and allow editing of personal information"""
    st.subheader("📝 Información Personal")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Profile picture placeholder
        st.image("https://via.placeholder.com/200x200/2E86C1/FFFFFF?text=👤", width=200)
        
        if st.button("📸 Cambiar Foto", use_container_width=True):
            st.info("Funcionalidad de carga de imagen próximamente disponible")
    
    with col2:
        # Editable form
        with st.form("profile_form"):
            st.markdown("##### Datos Personales")
            
            name = st.text_input(
                "Nombre Completo", 
                value=user_data.get('name', username),
                placeholder="Tu nombre completo"
            )
            
            email = st.text_input(
                "Email", 
                value=user_data.get('email', ''),
                placeholder="tu.email@ejemplo.com"
            )
            
            col_age, col_height, col_weight = st.columns(3)
            
            with col_age:
                age = st.number_input(
                    "Edad", 
                    min_value=13, 
                    max_value=100, 
                    value=user_data.get('age', 25)
                )
            
            with col_height:
                height = st.number_input(
                    "Altura (cm)", 
                    min_value=100, 
                    max_value=250, 
                    value=user_data.get('height', 170)
                )
            
            with col_weight:
                weight = st.number_input(
                    "Peso (kg)", 
                    min_value=30.0, 
                    max_value=300.0, 
                    value=float(user_data.get('weight', 70)),
                    step=0.1
                )
            
            fitness_level = st.selectbox(
                "Nivel de Fitness",
                options=["Principiante", "Intermedio", "Avanzado", "Profesional"],
                index=["Principiante", "Intermedio", "Avanzado", "Profesional"].index(
                    user_data.get('fitness_level', 'Intermedio')
                )
            )
            
            goals = st.multiselect(
                "Objetivos de Fitness",
                options=[
                    "Perder peso", "Ganar músculo", "Mejorar resistencia", 
                    "Aumentar fuerza", "Flexibilidad", "Bienestar general"
                ],
                default=user_data.get('goals', ["Bienestar general"])
            )
            
            bio = st.text_area(
                "Biografía", 
                value=user_data.get('bio', ''),
                placeholder="Cuéntanos un poco sobre ti y tus objetivos fitness...",
                height=100
            )
            
            # Save button
            if st.form_submit_button("💾 Guardar Cambios", use_container_width=True):
                updated_data = {
                    'name': name,
                    'email': email,
                    'age': age,
                    'height': height,
                    'weight': weight,
                    'fitness_level': fitness_level,
                    'goals': goals,
                    'bio': bio
                }
                
                if save_user_profile(username, updated_data):
                    st.session_state.user_data = updated_data
                    st.success("✅ Perfil actualizado exitosamente!")
                    st.rerun()
                else:
                    st.error("❌ Error al guardar el perfil")
    
    # Calculate and show BMI
    if user_data.get('height') and user_data.get('weight'):
        show_health_metrics(user_data)

def show_health_metrics(user_data):
    """Display health metrics like BMI"""
    st.markdown("---")
    st.subheader("🏥 Métricas de Salud")
    
    height_m = user_data['height'] / 100
    weight = user_data['weight']
    bmi = weight / (height_m ** 2)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📏 IMC", f"{bmi:.1f}")
    
    with col2:
        bmi_category = get_bmi_category(bmi)
        st.metric("📊 Categoría", bmi_category)
    
    with col3:
        ideal_weight = 22.5 * (height_m ** 2)  # Middle of healthy BMI range
        st.metric("🎯 Peso Ideal", f"{ideal_weight:.1f} kg")
    
    with col4:
        weight_diff = weight - ideal_weight
        st.metric("⚖️ Diferencia", f"{weight_diff:+.1f} kg")
    
    # BMI visualization
    show_bmi_chart(bmi)

def get_bmi_category(bmi):
    """Get BMI category based on value"""
    if bmi < 18.5:
        return "Bajo peso"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

def show_bmi_chart(bmi):
    """Show BMI visualization chart"""
    # BMI ranges
    ranges = ['Bajo peso', 'Normal', 'Sobrepeso', 'Obesidad']
    values = [18.5, 25, 30, 40]
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    
    fig = go.Figure()
    
    # Add ranges
    for i, (range_name, value, color) in enumerate(zip(ranges, values, colors)):
        start = 0 if i == 0 else values[i-1]
        fig.add_trace(go.Bar(
            x=[value - start],
            y=[range_name],
            orientation='h',
            name=range_name,
            marker_color=color,
            opacity=0.7
        ))
    
    # Add user BMI marker
    fig.add_vline(x=bmi, line_dash="dash", line_color="red", line_width=3)
    fig.add_annotation(
        x=bmi, y=1.5,
        text=f"Tu IMC: {bmi:.1f}",
        showarrow=True,
        arrowhead=2,
        bgcolor="white",
        bordercolor="red"
    )
    
    fig.update_layout(
        title="Tu IMC en Contexto",
        xaxis_title="IMC",
        yaxis_title="Categorías",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_preferences(username):
    """Show user preferences and settings"""
    st.subheader("🎯 Preferencias de Entrenamiento")
    
    # Load current preferences
    prefs = load_user_preferences(username)
    
    with st.form("preferences_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### ⏰ Horarios Preferidos")
            preferred_time = st.selectbox(
                "Hora preferida para entrenar",
                options=["Mañana (6-10)", "Medio día (11-14)", "Tarde (15-18)", "Noche (19-22)"],
                index=prefs.get('preferred_time_index', 0)
            )
            
            workout_duration = st.slider(
                "Duración ideal por sesión (minutos)",
                min_value=15,
                max_value=120,
                value=prefs.get('workout_duration', 45),
                step=15
            )
            
            weekly_frequency = st.slider(
                "Frecuencia semanal deseada",
                min_value=1,
                max_value=7,
                value=prefs.get('weekly_frequency', 3)
            )
        
        with col2:
            st.markdown("##### 🏋️ Tipos de Ejercicio")
            exercise_preferences = st.multiselect(
                "Ejercicios favoritos",
                options=[
                    "Cardio", "Fuerza", "Flexibilidad", "HIIT", 
                    "Yoga", "Pilates", "Calistenia", "Pesas"
                ],
                default=prefs.get('exercise_preferences', ["Cardio", "Fuerza"])
            )
            
            difficulty_level = st.select_slider(
                "Nivel de dificultad preferido",
                options=["Fácil", "Moderado", "Desafiante", "Extremo"],
                value=prefs.get('difficulty_level', "Moderado")
            )
            
            notifications = st.checkbox(
                "Recibir recordatorios de entrenamiento",
                value=prefs.get('notifications', True)
            )
        
        if st.form_submit_button("💾 Guardar Preferencias", use_container_width=True):
            new_prefs = {
                'preferred_time': preferred_time,
                'preferred_time_index': ["Mañana (6-10)", "Medio día (11-14)", "Tarde (15-18)", "Noche (19-22)"].index(preferred_time),
                'workout_duration': workout_duration,
                'weekly_frequency': weekly_frequency,
                'exercise_preferences': exercise_preferences,
                'difficulty_level': difficulty_level,
                'notifications': notifications
            }
            
            if save_user_preferences(username, new_prefs):
                st.success("✅ Preferencias guardadas exitosamente!")
            else:
                st.error("❌ Error al guardar las preferencias")

def save_user_profile(username, profile_data):
    """Save user profile data"""
    try:
        users_file = Path("data/users.json")
        users_file.parent.mkdir(exist_ok=True)
        
        if users_file.exists():
            with open(users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}
        
        if username not in users:
            users[username] = {}
        
        users[username]['profile'] = profile_data
        users[username]['updated_at'] = str(datetime.now())
        
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving profile: {str(e)}")
        return False

def load_user_preferences(username):
    """Load user preferences"""
    try:
        prefs_file = Path(f"data/{username}/preferences.json")
        if prefs_file.exists():
            with open(prefs_file, 'r') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_user_preferences(username, preferences):
    """Save user preferences"""
    try:
        user_dir = Path(f"data/{username}")
        user_dir.mkdir(parents=True, exist_ok=True)
        
        prefs_file = user_dir / "preferences.json"
        with open(prefs_file, 'w') as f:
            json.dump(preferences, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving preferences: {str(e)}")
        return False 