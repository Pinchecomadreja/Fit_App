# Rochi Fitness Application Guide

## Overview

Rochi Fitness is a comprehensive fitness tracking web application built with Streamlit. It provides users with a complete fitness management system including workout tracking, progress visualization, and routine management.

## Features

### 🏠 **Home Page**
- Welcome interface with application overview
- Quick navigation to all features
- User-friendly introduction

### 🔐 **Authentication System**
- Secure login functionality
- Multiple user profiles support
- Session management

### 📊 **Dashboard**
- **2x2 Metrics Layout:**
  - Total Workouts (Blue card)
  - Total Time (Green card) 
  - Estimated Calories (Orange card)
  - Current Streak (Red card)
- Interactive data visualizations using Matplotlib and Plotly
- Progress tracking over time
- Workout statistics and analytics

### 👤 **User Profile**
- Personal information management
- Fitness goals and preferences
- User statistics and achievements

### 💪 **Routine Viewer**
- Daily workout routines
- Exercise tracking and logging
- Routine history and management

## Installation & Setup

### Prerequisites
- Python 3.8+ installed
- pip package manager

### Installation Steps

1. **Clone or download the application files**
2. **Install dependencies:**
   ```bash
   pip install streamlit pandas matplotlib plotly numpy
   ```

3. **Verify file structure:**
   ```
   /
   ├── app.py
   ├── pages/
   │   ├── login.py
   │   ├── dashboard.py
   │   ├── profile.py
   │   └── routine_viewer.py
   └── utils/
       ├── api_client.py
       └── data_handler.py
   ```

## How to Start the Application

### Method 1: Standard Startup
```bash
streamlit run app.py
```

### Method 2: Custom Port
```bash
streamlit run app.py --server.port 8501
```

### Method 3: External Access
```bash
streamlit run app.py --server.address 0.0.0.0
```

## First Time Usage

1. **Start the application** using one of the methods above
2. **Open your browser** and navigate to the displayed URL (typically `http://localhost:8501`)
3. **Login with test credentials:**
   - **Demo User:** `demo` / `demo123`
   - **Advanced User:** `rocio` / `password123`

## User Profiles

### Demo User (demo/demo123)
- Beginner fitness level
- Bodyweight exercises focus
- Basic workout routines
- Starter statistics

### Advanced User (rocio/password123)  
- Experienced fitness level
- Weight training exercises
- Advanced workout routines
- Rich workout history

## Navigation

The application features a clean, intuitive navigation system:

- **Home** - Welcome page and overview
- **Login** - User authentication
- **Dashboard** - Fitness metrics and visualizations
- **Profile** - Personal information and settings
- **Routine Viewer** - Daily workouts and exercise tracking

## Data Storage

- **Format:** JSON-based data storage for all workout data
- **Backup:** Automatic CSV export for data backup
- **Location:** Data files are created in the application directory
- **Persistence:** All user data is saved between sessions

## Technical Features

### Frontend
- **Streamlit:** Modern web interface
- **Responsive Design:** Works on desktop and mobile
- **Custom CSS:** Professional styling with gradient cards
- **Clean UI:** Minimal, distraction-free interface

### Data Visualization
- **Matplotlib:** Statistical charts and graphs
- **Plotly:** Interactive visualizations
- **Real-time Updates:** Dynamic data display

### Backend Integration
- **API Client:** Ready for external API connections
- **Data Handler:** Robust data management system
- **Error Handling:** Comprehensive error management

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Dependencies Missing**
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Loading Issues**
   - Check if JSON files exist in the application directory
   - Verify file permissions
   - Try logging in as different user

### Support
- Check the terminal/console for error messages
- Ensure all dependencies are installed
- Verify Python version compatibility

## Development Ready

The application is structured for easy development and deployment:
- Modular code architecture
- Separated concerns (pages, utils)
- Ready for cloud deployment
- Extensible design for additional features

---

**Quick Start Command:**
```bash
streamlit run app.py
```

**Default Access:** http://localhost:8501

**Test Login:** demo/demo123 or rocio/password123 