import requests
import streamlit as st
import json
from typing import Dict, List, Optional
import os

class APIClient:
    """Client for backend API integration"""
    
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', 'https://api.rochi-fitness.com/v1')
        self.api_key = os.getenv('API_KEY', 'demo-key')
        self.timeout = 10
        
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'Fitness-Tracker-App/1.0'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """Make HTTP request to API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self._get_headers(), 
                                       json=data, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self._get_headers(), 
                                      json=data, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self._get_headers(), timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            st.error(f"JSON Decode Error: {str(e)}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user with backend"""
        data = {
            'username': username,
            'password': password
        }
        
        response = self._make_request('POST', '/auth/login', data)
        
        if response and response.get('success'):
            # Store auth token in session state
            st.session_state['auth_token'] = response.get('token')
            return response.get('user_data')
        
        return None
    
    def register_user(self, user_data: Dict) -> bool:
        """Register new user"""
        response = self._make_request('POST', '/auth/register', user_data)
        return response and response.get('success', False)
    
    def sync_workout_data(self, username: str, workouts: List[Dict]) -> bool:
        """Sync workout data to backend"""
        data = {
            'username': username,
            'workouts': workouts
        }
        
        response = self._make_request('POST', '/workouts/sync', data)
        return response and response.get('success', False)
    
    def get_workout_recommendations(self, user_profile: Dict) -> List[Dict]:
        """Get workout recommendations from AI backend"""
        response = self._make_request('POST', '/recommendations/workouts', user_profile)
        
        if response and response.get('success'):
            return response.get('recommendations', [])
        
        return []
    
    def get_nutrition_data(self, username: str) -> Optional[Dict]:
        """Get nutrition recommendations"""
        response = self._make_request('GET', f'/nutrition/{username}')
        
        if response and response.get('success'):
            return response.get('nutrition_data')
        
        return None
    
    def upload_progress_photo(self, username: str, photo_data: bytes) -> bool:
        """Upload progress photo"""
        # In a real implementation, this would handle file upload
        # For demo purposes, we'll simulate the API call
        
        try:
            # Simulate API call
            st.info("📸 Progress photo upload simulated (API integration)")
            return True
        except Exception as e:
            st.error(f"Photo upload failed: {str(e)}")
            return False
    
    def get_community_challenges(self) -> List[Dict]:
        """Get active community challenges"""
        response = self._make_request('GET', '/community/challenges')
        
        if response and response.get('success'):
            return response.get('challenges', [])
        
        # Demo challenges if API not available
        return [
            {
                'id': 1,
                'title': '30-Day Push-up Challenge',
                'description': 'Complete 100 push-ups in 30 days',
                'participants': 245,
                'deadline': '2024-12-31'
            },
            {
                'id': 2,
                'title': 'Weekly Cardio Challenge',
                'description': 'Complete 150 minutes of cardio this week',
                'participants': 180,
                'deadline': '2024-12-07'
            }
        ]
    
    def submit_feedback(self, feedback_data: Dict) -> bool:
        """Submit user feedback"""
        response = self._make_request('POST', '/feedback', feedback_data)
        return response and response.get('success', False)
    
    def get_weather_workout_suggestions(self, location: str) -> Dict:
        """Get weather-based workout suggestions"""
        data = {'location': location}
        response = self._make_request('POST', '/weather/suggestions', data)
        
        if response and response.get('success'):
            return response.get('suggestions', {})
        
        # Default suggestions if API not available
        return {
            'indoor': ['Push-ups', 'Squats', 'Planks'],
            'outdoor': ['Running', 'Walking', 'Cycling'],
            'weather': 'Unknown'
        }


# Singleton instance
api_client = APIClient()

# Convenience functions
def sync_user_data(username: str, workouts: List[Dict]) -> bool:
    """Sync user workout data to backend"""
    return api_client.sync_workout_data(username, workouts)

def get_recommendations(user_profile: Dict) -> List[Dict]:
    """Get workout recommendations"""
    return api_client.get_workout_recommendations(user_profile)

def authenticate(username: str, password: str) -> Optional[Dict]:
    """Authenticate user"""
    return api_client.authenticate_user(username, password)

def register(user_data: Dict) -> bool:
    """Register new user"""
    return api_client.register_user(user_data)

def get_challenges() -> List[Dict]:
    """Get community challenges"""
    return api_client.get_community_challenges()

def check_api_status() -> bool:
    """Check if API is available"""
    try:
        response = api_client._make_request('GET', '/health')
        return response and response.get('status') == 'healthy'
    except:
        return False 