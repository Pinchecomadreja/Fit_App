import json
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st
import pandas as pd
import random

class PureJSONDataHandler:
    """Handle pure JSON data storage and processing - No Database, No CSV"""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self._init_mock_data()
    
    def _init_mock_data(self):
        """Initialize rich mock data in JSON format"""
        if not self.users_file.exists():
            self._create_rich_mock_data()
    
    def _create_rich_mock_data(self):
        """Create comprehensive mock data with exercises and metrics"""
        # Create users
        users_data = {
            "demo": {
                "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # demo123
                "created_at": "2024-01-01T00:00:00",
                "profile": {
                    "name": "Usuario Demo",
                    "email": "demo@rochi.com",
                    "age": 28,
                    "height": 175,
                    "weight": 75,
                    "fitness_level": "Intermedio",
                    "goals": ["Perder peso", "Ganar músculo"],
                    "favorite_exercises": ["Push-ups", "Squats", "Running"]
                }
            },
            "rocio": {
                "password": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # password123
                "created_at": "2024-01-01T00:00:00",
                "profile": {
                    "name": "Rocío Fitness",
                    "email": "rocio@rochi.com",
                    "age": 25,
                    "height": 165,
                    "weight": 60,
                    "fitness_level": "Avanzado",
                    "goals": ["Fuerza", "Resistencia", "Competir"],
                    "favorite_exercises": ["Deadlifts", "Pull-ups", "Bench Press"]
                }
            }
        }
        
        # Save users
        with open(self.users_file, 'w') as f:
            json.dump(users_data, f, indent=2)
        
        # Create rich workout data for each user
        self._create_demo_workouts("demo")
        self._create_rocio_workouts("rocio")
        
        # Create metrics and analytics
        self._create_user_metrics("demo")
        self._create_user_metrics("rocio")
    
    def _create_demo_workouts(self, username):
        """Create diverse workout data for demo user"""
        user_dir = Path(f"data/{username}")
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Bodyweight exercises for demo user
        exercises = [
            {"name": "Push-ups", "type": "strength", "muscle_groups": ["chest", "triceps"], "equipment": "bodyweight"},
            {"name": "Squats", "type": "strength", "muscle_groups": ["legs", "glutes"], "equipment": "bodyweight"},
            {"name": "Planks", "type": "core", "muscle_groups": ["core"], "equipment": "bodyweight"},
            {"name": "Burpees", "type": "cardio", "muscle_groups": ["full_body"], "equipment": "bodyweight"},
            {"name": "Lunges", "type": "strength", "muscle_groups": ["legs", "glutes"], "equipment": "bodyweight"},
            {"name": "Mountain Climbers", "type": "cardio", "muscle_groups": ["core", "legs"], "equipment": "bodyweight"},
            {"name": "Jumping Jacks", "type": "cardio", "muscle_groups": ["full_body"], "equipment": "bodyweight"},
        ]
        
        workouts = []
        start_date = datetime.now() - timedelta(days=60)
        
        for i in range(60):
            current_date = start_date + timedelta(days=i)
            
            # Create 1-3 exercises per day, but not every day
            if random.random() > 0.3:  # 70% chance of workout
                num_exercises = random.randint(1, 3)
                selected_exercises = random.sample(exercises, num_exercises)
                
                for exercise in selected_exercises:
                    workout = {
                        "date": current_date.strftime('%Y-%m-%d'),
                        "exercise": exercise["name"],
                        "sets": random.randint(2, 4),
                        "reps": random.randint(8, 20),
                        "weight": 0,  # Bodyweight
                        "duration_minutes": random.randint(8, 25),
                        "start_time": f"{random.randint(6, 20):02d}:{random.randint(0, 59):02d}",
                        "notes": random.choice([
                            "Sesión matutina", "Entrenamiento completo", "Rutina rápida",
                            "Buen ritmo", "Desafío personal", "Día de cardio", ""
                        ]),
                        "intensity": random.choice(["Baja", "Moderada", "Alta"]),
                        "calories_burned": random.randint(50, 200),
                        "heart_rate_avg": random.randint(110, 160),
                        "created_at": current_date.isoformat()
                    }
                    workouts.append(workout)
        
        # Save workouts
        with open(user_dir / "workouts.json", 'w') as f:
            json.dump(workouts, f, indent=2)
    
    def _create_rocio_workouts(self, username):
        """Create advanced workout data for Rocío"""
        user_dir = Path(f"data/{username}")
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Advanced exercises for Rocío
        exercises = [
            {"name": "Deadlifts", "type": "strength", "muscle_groups": ["back", "legs"], "equipment": "barbell"},
            {"name": "Pull-ups", "type": "strength", "muscle_groups": ["back", "biceps"], "equipment": "bar"},
            {"name": "Bench Press", "type": "strength", "muscle_groups": ["chest", "triceps"], "equipment": "barbell"},
            {"name": "Squats", "type": "strength", "muscle_groups": ["legs", "glutes"], "equipment": "barbell"},
            {"name": "Rows", "type": "strength", "muscle_groups": ["back", "biceps"], "equipment": "barbell"},
            {"name": "Overhead Press", "type": "strength", "muscle_groups": ["shoulders", "triceps"], "equipment": "barbell"},
            {"name": "Dips", "type": "strength", "muscle_groups": ["triceps", "chest"], "equipment": "bars"},
        ]
        
        workouts = []
        start_date = datetime.now() - timedelta(days=60)
        
        for i in range(60):
            current_date = start_date + timedelta(days=i)
            
            # Rocío trains more consistently - 80% chance
            if random.random() > 0.2:
                num_exercises = random.randint(2, 4)
                selected_exercises = random.sample(exercises, num_exercises)
                
                for exercise in selected_exercises:
                    workout = {
                        "date": current_date.strftime('%Y-%m-%d'),
                        "exercise": exercise["name"],
                        "sets": random.randint(3, 6),
                        "reps": random.randint(4, 12),
                        "weight": random.randint(20, 120),  # Uses weights
                        "duration_minutes": random.randint(15, 45),
                        "start_time": f"{random.randint(6, 20):02d}:{random.randint(0, 59):02d}",
                        "notes": random.choice([
                            "PR personal!", "Técnica perfecta", "Entrenamiento intenso",
                            "Nueva marca", "Fuerza en aumento", "Día de poder", "Supersets"
                        ]),
                        "intensity": random.choice(["Moderada", "Alta", "Máxima"]),
                        "calories_burned": random.randint(150, 400),
                        "heart_rate_avg": random.randint(120, 180),
                        "created_at": current_date.isoformat()
                    }
                    workouts.append(workout)
        
        # Save workouts
        with open(user_dir / "workouts.json", 'w') as f:
            json.dump(workouts, f, indent=2)
    
    def _create_user_metrics(self, username):
        """Create analytics and metrics for user"""
        user_dir = Path(f"data/{username}")
        
        # Personal records
        if username == "demo":
            records = {
                "personal_records": {
                    "Push-ups": {"max_reps": 25, "date": "2024-05-15"},
                    "Squats": {"max_reps": 30, "date": "2024-05-20"},
                    "Planks": {"max_duration": 120, "date": "2024-05-10"},
                    "longest_workout": 45,
                    "most_calories": 250
                }
            }
        else:  # rocio
            records = {
                "personal_records": {
                    "Deadlifts": {"max_weight": 120, "date": "2024-05-25"},
                    "Pull-ups": {"max_reps": 15, "date": "2024-05-18"},
                    "Bench Press": {"max_weight": 80, "date": "2024-05-22"},
                    "Squats": {"max_weight": 100, "date": "2024-05-20"},
                    "longest_workout": 75,
                    "most_calories": 450
                }
            }
        
        # Goals and achievements
        goals = {
            "current_goals": [
                {"goal": "Entrenar 4 veces por semana", "progress": 75, "target_date": "2024-07-01"},
                {"goal": "Quemar 1000 calorías semanales", "progress": 60, "target_date": "2024-06-30"},
                {"goal": "Mejorar resistencia", "progress": 40, "target_date": "2024-08-01"}
            ],
            "achievements": [
                "🏆 Primera semana completa",
                "💪 10 días consecutivos",
                "🔥 1000 calorías quemadas",
                "📈 Récord personal",
                "⭐ Mes de constancia"
            ]
        }
        
        # Weekly stats
        weekly_stats = {
            "last_4_weeks": [
                {"week": "Semana 1", "workouts": 4, "duration": 180, "calories": 800},
                {"week": "Semana 2", "workouts": 5, "duration": 210, "calories": 950},
                {"week": "Semana 3", "workouts": 3, "duration": 145, "calories": 650},
                {"week": "Semana 4", "workouts": 6, "duration": 245, "calories": 1100}
            ]
        }
        
        # Save all metrics
        with open(user_dir / "records.json", 'w') as f:
            json.dump(records, f, indent=2)
        
        with open(user_dir / "goals.json", 'w') as f:
            json.dump(goals, f, indent=2)
        
        with open(user_dir / "stats.json", 'w') as f:
            json.dump(weekly_stats, f, indent=2)
    
    def get_user_workouts(self, username: str, start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> pd.DataFrame:
        """Get user workouts from JSON file only"""
        try:
            json_file = Path(f"data/{username}/workouts.json")
            
            if json_file.exists():
                with open(json_file, 'r') as f:
                    workouts_data = json.load(f)
                
                if not workouts_data:
                    return pd.DataFrame()
                
                df = pd.DataFrame(workouts_data)
                df['date'] = pd.to_datetime(df['date'])
                
                # Apply date filters
                if start_date:
                    df = df[df['date'] >= pd.to_datetime(start_date)]
                if end_date:
                    df = df[df['date'] <= pd.to_datetime(end_date)]
                
                return df.sort_values('date', ascending=False)
            
            # If no file exists, create mock data
            if username in ["demo", "rocio"]:
                self._init_mock_data()
                return self.get_user_workouts(username, start_date, end_date)
            
            return pd.DataFrame()
            
        except Exception as e:
            st.error(f"Error loading workouts: {str(e)}")
            return pd.DataFrame()
    
    def save_workout(self, username: str, workout_data: Dict) -> bool:
        """Save workout to JSON file"""
        try:
            user_dir = Path(f"data/{username}")
            user_dir.mkdir(parents=True, exist_ok=True)
            
            json_file = user_dir / "workouts.json"
            
            # Load existing data
            if json_file.exists():
                with open(json_file, 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []
            
            # Add timestamp if not present
            if 'created_at' not in workout_data:
                workout_data['created_at'] = datetime.now().isoformat()
            
            # Convert date to string
            if hasattr(workout_data.get('date'), 'strftime'):
                workout_data['date'] = workout_data['date'].strftime('%Y-%m-%d')
            
            # Append new workout
            existing_data.append(workout_data)
            
            # Save back to JSON
            with open(json_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
            
            return True
            
        except Exception as e:
            st.error(f"Error saving workout: {str(e)}")
            return False
    
    def calculate_workout_stats(self, username: str, period_days: int = 30) -> Dict:
        """Calculate workout statistics from JSON data"""
        workouts = self.get_user_workouts(username)
        
        if workouts.empty:
            return {
                'total_workouts': 0,
                'total_duration': 0,
                'avg_duration': 0,
                'total_calories': 0,
                'total_sets': 0,
                'total_reps': 0,
                'most_common_exercise': 'N/A',
                'workout_frequency': 0,
                'current_streak': 0
            }
        
        # Filter by period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        recent_workouts = workouts[workouts['date'] >= start_date]
        
        stats = {
            'total_workouts': len(recent_workouts),
            'total_duration': recent_workouts['duration_minutes'].sum(),
            'avg_duration': recent_workouts['duration_minutes'].mean(),
            'total_calories': recent_workouts.get('calories_burned', pd.Series([0])).sum(),
            'total_sets': recent_workouts['sets'].sum(),
            'total_reps': recent_workouts['reps'].sum(),
            'most_common_exercise': recent_workouts['exercise'].mode().iloc[0] if len(recent_workouts) > 0 else 'N/A',
            'workout_frequency': len(recent_workouts) / period_days * 7,  # per week
            'current_streak': self._calculate_streak(workouts)
        }
        
        return stats
    
    def _calculate_streak(self, workouts: pd.DataFrame) -> int:
        """Calculate current workout streak"""
        if workouts.empty:
            return 0
        
        # Get unique workout dates
        workout_dates = workouts['date'].dt.date.unique()
        workout_dates = sorted(workout_dates, reverse=True)
        
        current_date = datetime.now().date()
        streak = 0
        
        for date in workout_dates:
            days_diff = (current_date - date).days
            if days_diff <= streak + 1:  # Allow 1 day gap
                streak += 1
            else:
                break
        
        return streak


# Global instance - Pure JSON Handler
json_data_handler = PureJSONDataHandler()

# Convenience functions
def save_workout(username: str, workout_data: Dict) -> bool:
    """Save workout data to JSON"""
    return json_data_handler.save_workout(username, workout_data)

def get_workouts(username: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """Get user workouts from JSON"""
    return json_data_handler.get_user_workouts(username, start_date, end_date)

def get_stats(username: str, period_days: int = 30) -> Dict:
    """Get workout statistics from JSON"""
    return json_data_handler.calculate_workout_stats(username, period_days) 