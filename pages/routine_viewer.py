import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
import numpy as np

def show_routine_viewer():
    """Display daily routine viewer and workout logger"""
    st.markdown('<h1 style="text-align: center; color: #2E86C1;">📋 Rutina del Día</h1>', unsafe_allow_html=True)
    
    # Date selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_date = st.date_input(
            "📅 Selecciona la fecha",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🏃 Rutina Actual", "➕ Agregar Ejercicio", "📊 Resumen del Día"])
    
    with tab1:
        show_daily_routine(selected_date)
    
    with tab2:
        show_add_exercise_form(selected_date)
    
    with tab3:
        show_daily_summary(selected_date)

def show_daily_routine(selected_date):
    """Show the routine for the selected date"""
    st.subheader(f"🏋️ Rutina para {selected_date.strftime('%d/%m/%Y')}")
    
    # Load workouts for the selected date
    username = st.session_state.get('username', 'demo')
    daily_workouts = load_daily_workouts(username, selected_date)
    
    if daily_workouts.empty:
        st.info("🤷‍♂️ No hay ejercicios registrados para este día")
        
        # Suggest a routine based on user preferences
        show_suggested_routine()
        return
    
    # Display workouts in cards
    for idx, workout in daily_workouts.iterrows():
        show_workout_card(workout, idx)
    
    # Summary metrics for the day
    show_daily_metrics(daily_workouts)

def show_workout_card(workout, idx):
    """Display a single workout in a card format"""
    with st.container():
        st.markdown(f"""
        <div style="
            background-color: #F8F9FA; 
            padding: 1rem; 
            border-radius: 10px; 
            border-left: 5px solid #2E86C1; 
            margin: 1rem 0;
        ">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"### {get_exercise_emoji(workout['exercise'])} {workout['exercise']}")
            st.write(f"⏰ {workout.get('start_time', 'N/A')} - Duración: {workout['duration_minutes']} min")
        
        with col2:
            st.metric("Series", workout['sets'])
        
        with col3:
            st.metric("Repeticiones", workout['reps'])
        
        with col4:
            if workout.get('weight', 0) > 0:
                st.metric("Peso (kg)", f"{workout['weight']}")
            else:
                st.metric("Peso corporal", "✓")
        
        # Action buttons
        col_edit, col_delete = st.columns(2)
        
        with col_edit:
            if st.button(f"✏️ Editar", key=f"edit_{idx}"):
                st.session_state[f'editing_{idx}'] = True
        
        with col_delete:
            if st.button(f"🗑️ Eliminar", key=f"delete_{idx}"):
                if delete_workout(workout, idx):
                    st.rerun()
                else:
                    st.error("Error al eliminar el ejercicio")
        
        # Edit form (shown when editing)
        if st.session_state.get(f'editing_{idx}', False):
            show_edit_workout_form(workout, idx)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_edit_workout_form(workout, idx):
    """Show form to edit an existing workout"""
    st.markdown("##### ✏️ Editar Ejercicio")
    
    with st.form(f"edit_form_{idx}"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_sets = st.number_input("Series", min_value=1, value=int(workout['sets']))
            new_reps = st.number_input("Repeticiones", min_value=1, value=int(workout['reps']))
        
        with col2:
            new_weight = st.number_input("Peso (kg)", min_value=0.0, value=float(workout.get('weight', 0)), step=0.5)
            new_duration = st.number_input("Duración (min)", min_value=1, value=int(workout['duration_minutes']))
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            if st.form_submit_button("💾 Guardar"):
                if update_workout(workout, idx, new_sets, new_reps, new_weight, new_duration):
                    st.session_state[f'editing_{idx}'] = False
                    st.rerun()
                else:
                    st.error("Error al guardar los cambios")
        
        with col_cancel:
            if st.form_submit_button("❌ Cancelar"):
                st.session_state[f'editing_{idx}'] = False
                st.rerun()

def show_suggested_routine():
    """Show a suggested routine for the day"""
    st.markdown("### 💡 Rutina Sugerida para Hoy")
    
    # Load user preferences
    username = st.session_state.get('username', 'demo')
    preferences = load_user_preferences(username)
    
    # Get routine based on day of week and preferences
    suggested_exercises = get_suggested_exercises(preferences)
    
    st.info("🎯 Basada en tus preferencias y objetivos")
    
    for i, exercise in enumerate(suggested_exercises):
        with st.expander(f"{exercise['emoji']} {exercise['name']} - {exercise['duration']} min"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Series:** {exercise['sets']}")
                st.write(f"**Repeticiones:** {exercise['reps']}")
                st.write(f"**Descanso:** {exercise['rest']} seg")
            
            with col2:
                st.write(f"**Dificultad:** {exercise['difficulty']}")
                st.write(f"**Músculo objetivo:** {exercise['target']}")
                if st.button(f"➕ Agregar este ejercicio", key=f"add_suggested_{i}"):
                    add_suggested_exercise_to_routine(exercise)
                    st.success(f"✅ {exercise['name']} agregado a tu rutina!")
                    st.rerun()

def show_add_exercise_form(selected_date):
    """Show form to add new exercise"""
    st.subheader("➕ Agregar Nuevo Ejercicio")
    
    with st.form("add_exercise_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            exercise_name = st.selectbox(
                "🏋️ Tipo de Ejercicio",
                options=[
                    "Push-ups", "Squats", "Planks", "Burpees", "Lunges", 
                    "Mountain Climbers", "Jumping Jacks", "Pull-ups", 
                    "Deadlifts", "Bench Press", "Rows", "Dips"
                ]
            )
            
            sets = st.number_input("Series", min_value=1, max_value=10, value=3)
            reps = st.number_input("Repeticiones", min_value=1, max_value=100, value=15)
        
        with col2:
            weight = st.number_input(
                "Peso (kg) - 0 para peso corporal", 
                min_value=0.0, 
                max_value=500.0, 
                value=0.0, 
                step=0.5
            )
            
            duration = st.number_input(
                "Duración estimada (minutos)", 
                min_value=1, 
                max_value=120, 
                value=15
            )
            
            start_time = st.time_input(
                "⏰ Hora de inicio", 
                value=datetime.now().time()
            )
        
        notes = st.text_area(
            "📝 Notas adicionales", 
            placeholder="Observaciones, sensaciones, modificaciones..."
        )
        
        if st.form_submit_button("✅ Agregar Ejercicio", use_container_width=True):
            new_workout = {
                'date': selected_date,
                'exercise': exercise_name,
                'sets': sets,
                'reps': reps,
                'weight': weight,
                'duration_minutes': duration,
                'start_time': start_time.strftime('%H:%M'),
                'notes': notes,
                'created_at': datetime.now().isoformat()
            }
            
            if save_workout(new_workout):
                st.success(f"✅ {exercise_name} agregado exitosamente!")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Error al guardar el ejercicio")

def show_daily_summary(selected_date):
    """Show summary and analytics for the selected date"""
    st.subheader(f"📊 Resumen del {selected_date.strftime('%d/%m/%Y')}")
    
    username = st.session_state.get('username', 'demo')
    daily_workouts = load_daily_workouts(username, selected_date)
    
    if daily_workouts.empty:
        st.info("No hay datos para mostrar")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_exercises = len(daily_workouts)
    total_duration = daily_workouts['duration_minutes'].sum()
    total_sets = daily_workouts['sets'].sum()
    total_reps = daily_workouts['reps'].sum()
    
    with col1:
        st.metric("🏋️ Ejercicios", total_exercises)
    
    with col2:
        st.metric("⏱️ Tiempo Total", f"{total_duration} min")
    
    with col3:
        st.metric("📊 Series Totales", total_sets)
    
    with col4:
        st.metric("🔢 Repeticiones", total_reps)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Exercise distribution
        exercise_counts = daily_workouts['exercise'].value_counts()
        fig = px.pie(
            values=exercise_counts.values,
            names=exercise_counts.index,
            title="Distribución de Ejercicios"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Timeline of workouts
        if 'start_time' in daily_workouts.columns:
            daily_workouts['hour'] = pd.to_datetime(daily_workouts['start_time']).dt.hour
            hour_counts = daily_workouts.groupby('hour')['duration_minutes'].sum()
            
            fig = px.bar(
                x=hour_counts.index,
                y=hour_counts.values,
                title="Duración por Hora del Día",
                labels={'x': 'Hora', 'y': 'Minutos'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Workout intensity analysis
    show_intensity_analysis(daily_workouts)
    
    # Export in JSON format only
    try:
        json_data = daily_workouts.copy()
        if not json_data.empty:
            json_data['date'] = json_data['date'].astype(str)
            # Use json.dumps instead of pandas to_json to avoid recursion
            json_records = json_data.to_dict('records')
            json_str = json.dumps(json_records, indent=2, default=str)
        else:
            json_str = "[]"
        
        st.download_button(
            label="📥 Exportar Rutina (JSON)",
            data=json_str,
            file_name=f"routine_{selected_date}.json",
            mime="application/json",
            key=f"export_json_{selected_date}",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error al generar JSON: {str(e)}")
        st.download_button(
            label="📥 Exportar Rutina (Error)",
            data="[]",
            file_name=f"routine_{selected_date}.json",
            mime="application/json",
            key=f"export_json_error_{selected_date}",
            use_container_width=True
        )

def show_intensity_analysis(daily_workouts):
    """Show workout intensity analysis"""
    st.markdown("---")
    st.subheader("🔥 Análisis de Intensidad")
    
    # Calculate intensity score
    intensity_scores = []
    for _, workout in daily_workouts.iterrows():
        base_score = workout['sets'] * workout['reps']
        weight_multiplier = 1 + (workout.get('weight', 0) / 100)  # Normalize weight
        duration_factor = workout['duration_minutes'] / 30  # Normalize to 30min baseline
        
        intensity = base_score * weight_multiplier * duration_factor
        intensity_scores.append(intensity)
    
    daily_workouts['intensity'] = intensity_scores
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_intensity = np.mean(intensity_scores)
        max_intensity = max(intensity_scores) if intensity_scores else 0
        
        st.metric("🔥 Intensidad Promedio", f"{avg_intensity:.1f}")
        st.metric("⚡ Pico de Intensidad", f"{max_intensity:.1f}")
        
        # Intensity level
        if avg_intensity < 50:
            intensity_level = "🟢 Ligero"
        elif avg_intensity < 100:
            intensity_level = "🟡 Moderado"
        elif avg_intensity < 200:
            intensity_level = "🟠 Intenso"
        else:
            intensity_level = "🔴 Extremo"
        
        st.markdown(f"**Nivel del día:** {intensity_level}")
    
    with col2:
        # Intensity by exercise
        intensity_by_exercise = daily_workouts.groupby('exercise')['intensity'].mean()
        
        fig = px.bar(
            x=intensity_by_exercise.values,
            y=intensity_by_exercise.index,
            orientation='h',
            title="Intensidad por Ejercicio",
            color=intensity_by_exercise.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def show_daily_metrics(daily_workouts):
    """Show metrics for daily workouts"""
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💪 Total Ejercicios", len(daily_workouts))
    
    with col2:
        total_time = daily_workouts['duration_minutes'].sum()
        st.metric("⏱️ Tiempo Total", f"{total_time} min")
    
    with col3:
        calories_estimate = estimate_calories_burned(daily_workouts)
        st.metric("🔥 Calorías Estimadas", f"{calories_estimate:.0f}")
    
    with col4:
        muscle_groups = get_muscle_groups_worked(daily_workouts)
        st.metric("🎯 Grupos Musculares", len(muscle_groups))

def get_exercise_emoji(exercise_name):
    """Get emoji for exercise type"""
    emoji_map = {
        'Push-ups': '💪',
        'Squats': '🦵',
        'Planks': '🧘',
        'Burpees': '🏃',
        'Lunges': '🦵',
        'Mountain Climbers': '🧗',
        'Jumping Jacks': '🤸',
        'Pull-ups': '💪',
        'Deadlifts': '🏋️',
        'Bench Press': '🏋️',
        'Rows': '🚣',
        'Dips': '💪'
    }
    return emoji_map.get(exercise_name, '🏋️')

def load_daily_workouts(username, date):
    """Load workouts for a specific date from JSON"""
    try:
        data_file = Path(f"data/{username}/workouts.json")
        if data_file.exists():
            with open(data_file, 'r') as f:
                workouts_data = json.load(f)
            
            df = pd.DataFrame(workouts_data)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date']).dt.date
                
                # Filter for selected date
                daily_data = df[df['date'] == date]
                return daily_data
        
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading workouts: {str(e)}")
        return pd.DataFrame()

def save_workout(workout_data):
    """Save a new workout to the user's data in JSON format"""
    try:
        username = st.session_state.get('username', 'demo')
        data_dir = Path(f"data/{username}")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        data_file = data_dir / "workouts.json"
        
        # Convert date to string if it's a date object
        if hasattr(workout_data['date'], 'strftime'):
            workout_data['date'] = workout_data['date'].strftime('%Y-%m-%d')
        
        # Load existing data
        if data_file.exists():
            with open(data_file, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Append new workout
        existing_data.append(workout_data)
        
        # Save back to JSON
        with open(data_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        return True
    
    except Exception as e:
        st.error(f"Error saving workout: {str(e)}")
        return False

def get_suggested_exercises(preferences):
    """Get suggested exercises based on user preferences"""
    username = st.session_state.get('username', 'demo')
    
    # Different exercise suggestions based on user
    if username == 'rocio':
        # Advanced exercises for Rocío
        base_exercises = [
            {
                'name': 'Pull-ups',
                'emoji': '💪',
                'sets': 4,
                'reps': 8,
                'duration': 15,
                'rest': 90,
                'difficulty': 'Avanzado',
                'target': 'Espalda, Bíceps'
            },
            {
                'name': 'Deadlifts',
                'emoji': '🏋️',
                'sets': 4,
                'reps': 6,
                'duration': 20,
                'rest': 120,
                'difficulty': 'Avanzado',
                'target': 'Espalda, Piernas'
            },
            {
                'name': 'Bench Press',
                'emoji': '🏋️',
                'sets': 4,
                'reps': 8,
                'duration': 18,
                'rest': 90,
                'difficulty': 'Avanzado',
                'target': 'Pecho, Tríceps'
            },
            {
                'name': 'Squats',
                'emoji': '🦵',
                'sets': 4,
                'reps': 10,
                'duration': 15,
                'rest': 75,
                'difficulty': 'Intermedio',
                'target': 'Piernas, Glúteos'
            }
        ]
    else:
        # Bodyweight exercises for demo user
        base_exercises = [
            {
                'name': 'Push-ups',
                'emoji': '💪',
                'sets': 3,
                'reps': 12,
                'duration': 10,
                'rest': 60,
                'difficulty': 'Moderado',
                'target': 'Pecho, Tríceps'
            },
            {
                'name': 'Squats',
                'emoji': '🦵',
                'sets': 3,
                'reps': 15,
                'duration': 10,
                'rest': 45,
                'difficulty': 'Fácil',
                'target': 'Piernas, Glúteos'
            },
            {
                'name': 'Planks',
                'emoji': '🧘',
                'sets': 3,
                'reps': 45,
                'duration': 8,
                'rest': 30,
                'difficulty': 'Moderado',
                'target': 'Core'
            },
            {
                'name': 'Burpees',
                'emoji': '🏃',
                'sets': 3,
                'reps': 8,
                'duration': 12,
                'rest': 90,
                'difficulty': 'Desafiante',
                'target': 'Cuerpo Completo'
            }
        ]
    
    # Filter based on user preferences
    preferred_difficulty = preferences.get('difficulty_level', 'Moderado')
    
    # Return 3-4 exercises matching preferences
    return base_exercises[:3]

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

def estimate_calories_burned(workouts):
    """Estimate calories burned based on workouts"""
    # Simple estimation based on exercise type and duration
    calorie_rates = {
        'Push-ups': 8,    # calories per minute
        'Squats': 9,      
        'Planks': 5,      
        'Burpees': 12,    
        'Lunges': 8,      
        'Mountain Climbers': 10,
        'Jumping Jacks': 11,
        'Pull-ups': 9,
        'Deadlifts': 7,
        'Bench Press': 6,
        'Rows': 7,
        'Dips': 8
    }
    
    total_calories = 0
    for _, workout in workouts.iterrows():
        rate = calorie_rates.get(workout['exercise'], 7)  # Default rate
        calories = rate * workout['duration_minutes']
        total_calories += calories
    
    return total_calories

def get_muscle_groups_worked(workouts):
    """Get list of muscle groups worked"""
    muscle_groups = set()
    
    muscle_map = {
        'Push-ups': ['Pecho', 'Tríceps', 'Hombros'],
        'Squats': ['Piernas', 'Glúteos'],
        'Planks': ['Core', 'Hombros'],
        'Burpees': ['Cuerpo Completo'],
        'Lunges': ['Piernas', 'Glúteos'],
        'Mountain Climbers': ['Core', 'Piernas'],
        'Jumping Jacks': ['Cardio', 'Piernas'],
        'Pull-ups': ['Espalda', 'Bíceps'],
        'Deadlifts': ['Espalda', 'Piernas', 'Glúteos'],
        'Bench Press': ['Pecho', 'Tríceps', 'Hombros'],
        'Rows': ['Espalda', 'Bíceps'],
        'Dips': ['Tríceps', 'Pecho']
    }
    
    for _, workout in workouts.iterrows():
        groups = muscle_map.get(workout['exercise'], ['General'])
        muscle_groups.update(groups)
    
    return list(muscle_groups)

def add_suggested_exercise_to_routine(exercise):
    """Add a suggested exercise to the current routine"""
    selected_date = datetime.now().date()
    
    new_workout = {
        'date': selected_date,
        'exercise': exercise['name'],
        'sets': exercise['sets'],
        'reps': exercise['reps'],
        'weight': 0,
        'duration_minutes': exercise['duration'],
        'start_time': datetime.now().strftime('%H:%M'),
        'notes': 'Ejercicio sugerido',
        'created_at': datetime.now().isoformat()
    }
    
    save_workout(new_workout)

def delete_workout(workout, idx):
    """Delete a workout from the user's data"""
    try:
        username = st.session_state.get('username', 'demo')
        data_file = Path(f"data/{username}/workouts.json")
        
        if not data_file.exists():
            st.error("No se encontró el archivo de datos")
            return False
        
        # Load existing data
        with open(data_file, 'r') as f:
            existing_data = json.load(f)
        
        # Convert workout date to string for comparison
        workout_date = workout['date'].strftime('%Y-%m-%d') if hasattr(workout['date'], 'strftime') else str(workout['date'])
        
        # Find and remove the workout
        original_length = len(existing_data)
        existing_data = [w for w in existing_data if not (
            w['date'] == workout_date and 
            w['exercise'] == workout['exercise'] and
            w['sets'] == workout['sets'] and
            w['reps'] == workout['reps']
        )]
        
        if len(existing_data) < original_length:
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            st.success(f"✅ Ejercicio {workout['exercise']} eliminado")
            return True
        else:
            st.error("❌ No se pudo encontrar el ejercicio para eliminar")
            return False
            
    except Exception as e:
        st.error(f"❌ Error al eliminar ejercicio: {str(e)}")
        return False

def update_workout(workout, idx, sets, reps, weight, duration):
    """Update an existing workout"""
    try:
        username = st.session_state.get('username', 'demo')
        data_file = Path(f"data/{username}/workouts.json")
        
        if not data_file.exists():
            st.error("No se encontró el archivo de datos")
            return False
        
        # Load existing data
        with open(data_file, 'r') as f:
            existing_data = json.load(f)
        
        # Convert workout date to string for comparison
        workout_date = workout['date'].strftime('%Y-%m-%d') if hasattr(workout['date'], 'strftime') else str(workout['date'])
        
        # Find and update the workout
        updated = False
        for w in existing_data:
            if (w['date'] == workout_date and 
                w['exercise'] == workout['exercise'] and
                w.get('created_at') == workout.get('created_at')):
                
                # Update the workout data
                w['sets'] = int(sets)
                w['reps'] = int(reps)
                w['weight'] = float(weight)
                w['duration_minutes'] = int(duration)
                w['updated_at'] = datetime.now().isoformat()
                updated = True
                break
        
        if updated:
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            st.success("✅ Ejercicio actualizado exitosamente!")
            return True
        else:
            st.error("❌ No se pudo encontrar el ejercicio para actualizar")
            return False
            
    except Exception as e:
        st.error(f"❌ Error al actualizar ejercicio: {str(e)}")
        return False 