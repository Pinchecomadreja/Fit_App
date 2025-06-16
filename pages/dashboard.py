import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

def show_enhanced_dashboard_main(workout_data):
    """Show enhanced dashboard with 2x2 metrics layout"""
    # Custom CSS for dashboard cards
    st.markdown("""
    <style>
    .dashboard-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
    }
    
    .dashboard-card-blue {
        background: linear-gradient(135deg, #2E86C1 0%, #3498DB 100%);
    }
    
    .dashboard-card-green {
        background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
    }
    
    .dashboard-card-orange {
        background: linear-gradient(135deg, #E67E22 0%, #F39C12 100%);
    }
    
    .dashboard-card-red {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
    }
    
    .metric-title {
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-subtitle {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if workout_data.empty:
        st.info("🏃‍♂️ ¡Comienza tu viaje fitness! Agrega tu primer entrenamiento.")
        return
    
    # Calculate metrics
    total_workouts = len(workout_data)
    total_duration = workout_data['duration_minutes'].sum()
    current_streak = calculate_streak(workout_data)
    estimated_calories = total_duration * 8  # ~8 calories per minute average
    
    # Row 1: Two columns
    st.markdown("### 🏃‍♀️ Tu Progreso Fitness")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-card dashboard-card-blue">
            <div class="metric-icon">🏋️</div>
            <div class="metric-title">ENTRENAMIENTOS TOTALES</div>
            <div class="metric-value">{total_workouts}</div>
            <div class="metric-subtitle">Sesiones completadas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-card dashboard-card-green">
            <div class="metric-icon">⏱️</div>
            <div class="metric-title">TIEMPO TOTAL</div>
            <div class="metric-value">{total_duration}</div>
            <div class="metric-subtitle">Minutos de entrenamiento</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Row 2: Two columns  
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown(f"""
        <div class="dashboard-card dashboard-card-orange">
            <div class="metric-icon">🔥</div>
            <div class="metric-title">CALORÍAS ESTIMADAS</div>
            <div class="metric-value">{estimated_calories:.0f}</div>
            <div class="metric-subtitle">Energía quemada</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="dashboard-card dashboard-card-red">
            <div class="metric-icon">📈</div>
            <div class="metric-title">RACHA ACTUAL</div>
            <div class="metric-value">{current_streak}</div>
            <div class="metric-subtitle">Días consecutivos</div>
        </div>
        """, unsafe_allow_html=True)

def show_dashboard():
    """Display the main dashboard with metrics and visualizations"""
    st.markdown('<h1 style="text-align: center; color: #2E86C1;">📊 Dashboard Fitness</h1>', unsafe_allow_html=True)
    
    # Load user data
    username = st.session_state.get('username', 'demo')
    workout_data = load_workout_data()
    
    # Enhanced Dashboard with 2x2 Metrics Layout
    show_enhanced_dashboard_main(workout_data)
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        show_progress_chart(workout_data)
        show_exercise_distribution(workout_data)
    
    with col2:
        show_weekly_activity(workout_data)
        show_performance_trends(workout_data)
    
    st.markdown("---")
    
    # Additional Analytics
    show_detailed_analytics(workout_data)

def show_key_metrics(data):
    """Display key performance metrics"""
    if data.empty:
        st.warning("No hay datos de entrenamientos disponibles")
        return
    
    # Calculate metrics
    total_workouts = len(data)
    total_duration = data['duration_minutes'].sum()
    avg_duration = data['duration_minutes'].mean()
    current_streak = calculate_streak(data)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏋️ Total Entrenamientos",
            value=total_workouts,
            delta=f"+{len(data[data['date'] >= datetime.now() - timedelta(days=7)])}" if total_workouts > 0 else None
        )
    
    with col2:
        st.metric(
            label="⏱️ Tiempo Total (min)",
            value=f"{total_duration:.0f}",
            delta=f"+{data[data['date'] >= datetime.now() - timedelta(days=7)]['duration_minutes'].sum():.0f}"
        )
    
    with col3:
        st.metric(
            label="📊 Promedio por Sesión",
            value=f"{avg_duration:.1f} min",
            delta=f"{(avg_duration - data['duration_minutes'].mean()):.1f}"
        )
    
    with col4:
        st.metric(
            label="🔥 Racha Actual",
            value=f"{current_streak} días",
            delta="🎯" if current_streak > 7 else None
        )

def show_progress_chart(data):
    """Show progress over time using matplotlib"""
    st.subheader("📈 Progreso Semanal")
    
    if data.empty:
        st.info("No hay datos para mostrar")
        return
    
    # Aggregate weekly data
    data['week'] = data['date'].dt.to_period('W')
    weekly_data = data.groupby('week').agg({
        'duration_minutes': 'sum',
        'exercise': 'count'
    }).reset_index()
    
    # Create matplotlib chart
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Duration chart
    ax1.plot(weekly_data.index, weekly_data['duration_minutes'], 
             marker='o', linewidth=2, color='#2E86C1')
    ax1.set_ylabel('Minutos Totales', fontsize=12)
    ax1.set_title('Duración Semanal de Entrenamientos', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Frequency chart
    ax2.bar(weekly_data.index, weekly_data['exercise'], 
            color='#85C1E9', alpha=0.7)
    ax2.set_ylabel('Número de Ejercicios', fontsize=12)
    ax2.set_xlabel('Semanas', fontsize=12)
    ax2.set_title('Frecuencia Semanal de Ejercicios', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def show_weekly_activity(data):
    """Show weekly activity heatmap using plotly"""
    st.subheader("🗓️ Actividad Semanal")
    
    if data.empty:
        st.info("No hay datos para mostrar")
        return
    
    # Create activity heatmap data
    data['day_of_week'] = data['date'].dt.day_name()
    data['hour'] = data['date'].dt.hour
    
    # Fill missing hours with realistic training times
    if 'hour' not in data.columns or data['hour'].isna().all():
        np.random.seed(42)
        data['hour'] = np.random.choice([6, 7, 8, 18, 19, 20], size=len(data))
    
    activity_matrix = data.groupby(['day_of_week', 'hour']).size().reset_index(name='count')
    
    # Create pivot table for heatmap
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = activity_matrix.pivot_table(
        values='count', 
        index='day_of_week', 
        columns='hour', 
        fill_value=0
    )
    
    # Reorder days
    pivot_data = pivot_data.reindex(days_order, fill_value=0)
    
    # Create plotly heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Blues',
        showscale=True,
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Mapa de Calor - Actividad por Día y Hora',
        xaxis_title='Hora del Día',
        yaxis_title='Día de la Semana',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_exercise_distribution(data):
    """Show exercise type distribution"""
    st.subheader("💪 Distribución de Ejercicios")
    
    if data.empty:
        st.info("No hay datos para mostrar")
        return
    
    exercise_counts = data['exercise'].value_counts()
    
    # Create plotly pie chart
    fig = px.pie(
        values=exercise_counts.values,
        names=exercise_counts.index,
        title="Distribución de Tipos de Ejercicio",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

def show_performance_trends(data):
    """Show performance trends over time"""
    st.subheader("📊 Tendencias de Rendimiento")
    
    if data.empty:
        st.info("No hay datos para mostrar")
        return
    
    # Calculate performance metrics
    data_sorted = data.sort_values('date')
    data_sorted['cumulative_duration'] = data_sorted['duration_minutes'].cumsum()
    data_sorted['moving_avg'] = data_sorted['duration_minutes'].rolling(window=7).mean()
    
    # Create plotly line chart
    fig = go.Figure()
    
    # Add cumulative duration
    fig.add_trace(go.Scatter(
        x=data_sorted['date'],
        y=data_sorted['cumulative_duration'],
        mode='lines',
        name='Duración Acumulada',
        line=dict(color='#2E86C1', width=2)
    ))
    
    # Add moving average
    fig.add_trace(go.Scatter(
        x=data_sorted['date'],
        y=data_sorted['moving_avg'],
        mode='lines',
        name='Promedio Móvil (7 días)',
        line=dict(color='#E74C3C', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Tendencias de Rendimiento',
        xaxis_title='Fecha',
        yaxis_title='Minutos',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_analytics(data):
    """Show detailed analytics and insights"""
    st.subheader("🔍 Análisis Detallado")
    
    if data.empty:
        return
    
    tab1, tab2, tab3 = st.tabs(["📋 Resumen", "📊 Estadísticas", "🎯 Objetivos"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Estadísticas Generales")
            st.write(f"**Ejercicio más frecuente:** {data['exercise'].mode().iloc[0] if not data.empty else 'N/A'}")
            st.write(f"**Duración promedio:** {data['duration_minutes'].mean():.1f} minutos")
            st.write(f"**Total de series:** {data['sets'].sum()}")
            st.write(f"**Total de repeticiones:** {data['reps'].sum()}")
        
        with col2:
            st.markdown("#### 🏆 Récords Personales")
            max_duration = data['duration_minutes'].max()
            max_reps = data['reps'].max()
            max_sets = data['sets'].max()
            
            st.write(f"**Mayor duración:** {max_duration} minutos")
            st.write(f"**Máximas repeticiones:** {max_reps}")
            st.write(f"**Máximas series:** {max_sets}")
    
    with tab2:
        # Show data table
        st.markdown("#### 📊 Datos Recientes")
        recent_data = data.sort_values('date', ascending=False).head(10)
        st.dataframe(recent_data, use_container_width=True)
        
        # Download in JSON format only
        try:
            json_data = data.copy()
            if not json_data.empty:
                json_data['date'] = json_data['date'].dt.strftime('%Y-%m-%d')
                # Convert to dict first to avoid recursion issues
                json_records = json_data.to_dict('records')
                json_str = json.dumps(json_records, indent=2, default=str)
            else:
                json_str = "[]"
            
            st.download_button(
                label="📥 Descargar Datos (JSON)",
                data=json_str,
                file_name="workout_data.json",
                mime="application/json",
                key="download_json_dashboard",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error al generar JSON: {str(e)}")
            st.download_button(
                label="📥 Descargar Datos (Error)",
                data="[]",
                file_name="workout_data.json",
                mime="application/json",
                key="download_json_dashboard_error",
                use_container_width=True
            )
    
    with tab3:
        show_goals_section(data)

def show_goals_section(data):
    """Show goals and achievements section"""
    st.markdown("#### 🎯 Objetivos y Logros")
    
    # Weekly goals
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Objetivos Semanales")
        weekly_goal = st.number_input("Entrenamientos por semana", min_value=1, max_value=7, value=3)
        duration_goal = st.number_input("Minutos por semana", min_value=30, max_value=600, value=150)
        
        # Calculate current week progress
        current_week_data = data[data['date'] >= datetime.now() - timedelta(days=7)]
        current_workouts = len(current_week_data)
        current_duration = current_week_data['duration_minutes'].sum()
        
        # Progress bars
        workout_progress = min(current_workouts / weekly_goal, 1.0)
        duration_progress = min(current_duration / duration_goal, 1.0)
        
        st.progress(workout_progress, text=f"Entrenamientos: {current_workouts}/{weekly_goal}")
        st.progress(duration_progress, text=f"Duración: {current_duration:.0f}/{duration_goal} min")
    
    with col2:
        st.markdown("##### 🏅 Logros Desbloqueados")
        achievements = check_achievements(data)
        
        for achievement in achievements:
            st.success(f"🏆 {achievement}")

def check_achievements(data):
    """Check and return user achievements"""
    achievements = []
    
    if len(data) >= 10:
        achievements.append("Primer Milestone - 10+ entrenamientos")
    
    if data['duration_minutes'].sum() >= 300:
        achievements.append("Guerrero del Tiempo - 300+ minutos")
    
    streak = calculate_streak(data)
    if streak >= 7:
        achievements.append("Semana Perfecta - 7 días consecutivos")
    
    if data['exercise'].nunique() >= 5:
        achievements.append("Explorador - 5+ tipos de ejercicio")
    
    return achievements if achievements else ["¡Sigue entrenando para desbloquear logros!"]

def calculate_streak(data):
    """Calculate current workout streak"""
    if data.empty:
        return 0
    
    # Sort data by date
    data_sorted = data.sort_values('date', ascending=False)
    unique_dates = data_sorted['date'].dt.date.unique()
    
    streak = 0
    current_date = datetime.now().date()
    
    for date in unique_dates:
        if (current_date - date).days == streak:
            streak += 1
        else:
            break
    
    return streak

def load_workout_data():
    """Load workout data for the current user from JSON"""
    username = st.session_state.get('username', 'demo')
    data_file = Path(f"data/{username}/workouts.json")
    
    try:
        if data_file.exists():
            with open(data_file, 'r') as f:
                workouts_data = json.load(f)
            
            # Convert to DataFrame
            data = pd.DataFrame(workouts_data)
            if not data.empty:
                data['date'] = pd.to_datetime(data['date'])
            return data
        else:
            # Return sample data if file doesn't exist
            return generate_sample_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return generate_sample_data()

def generate_sample_data():
    """Generate sample workout data for demonstration"""
    username = st.session_state.get('username', 'demo')
    
    # Different seed for different users to show varied data
    if username == 'rocio':
        np.random.seed(123)  # Different seed for Rocío
        exercises = ['Pull-ups', 'Deadlifts', 'Squats', 'Bench Press', 'Rows', 'Dips']
        weight_range = (5, 25)  # Rocío uses weights
    else:
        np.random.seed(42)   # Original seed for demo user
        exercises = ['Push-ups', 'Squats', 'Planks', 'Burpees', 'Lunges', 'Mountain Climbers']
        weight_range = (0, 0)  # Demo user does bodyweight
    
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    
    # Random selection of dates (not every day)
    selected_dates = np.random.choice(dates, size=min(50, len(dates)), replace=False)
    
    data = []
    for date in selected_dates:
        exercise = np.random.choice(exercises)
        weight = np.random.randint(weight_range[0], weight_range[1] + 1) if weight_range[1] > 0 else 0
        
        data.append({
            'date': date,
            'exercise': exercise,
            'sets': np.random.randint(3, 6) if username == 'rocio' else np.random.randint(2, 5),
            'reps': np.random.randint(8, 15) if exercise != 'Planks' else np.random.randint(30, 120),
            'weight': weight,
            'duration_minutes': np.random.randint(20, 60) if username == 'rocio' else np.random.randint(15, 45)
        })
    
    return pd.DataFrame(data) 