import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "dietplanner.db"


def get_connection():
    INSTANCE_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        # Users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                Email TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                CreateDate TEXT NOT NULL
            )
        """)

        # User Stats table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS userStats (
                UserStatID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NULL,
                Height REAL NULL,
                [1kmBest] REAL NULL,
                [5kmBest] REAL NULL,
                [10kmBest] REAL NULL,
                HalfMarathonBest REAL NULL,
                MarathonBest REAL NULL,
                CreateDate REAL NOT NULL
            )
        """)

        # User Goals table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS userGoals (
                GoalID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NULL,
                Goal TEXT NULL,
                CreateDate REAL NOT NULL
            )
        """)

        # User Nutrition Goals table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS userNutrition (
                UserNutritionID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NULL,
                CalorieGoal TEXT NULL,
                ProteinGoal TEXT NULL,
                CarbohydrateGoal TEXT NULL,
                FatGoal TEXT NULL,
                FoodLikes TEXT NULL,
                FoodDislikes TEXT NULL,
                CreateDate REAL NOT NULL
            )
        """)

        # User Training Schedule table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS userTraining (
                UserTrainingID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NULL,
                WeekDay TEXT NOT NULL,
                Training TEXT NULL,
                LastUpdatedDate REAL NOT NULL,
                CreateDate REAL NOT NULL
            )
        """)

        # DailyLog table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS DailyLog (
                DailyLogID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NULL,
                LogDate TEXT NOT NULL,
                Weight_kg REAL,
                PreviousNightSleepScore INTEGER,
                Steps INTEGER
            )
        """)

        # Daily Self Assesment table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS DailySelfAssessment (
                DailyLogID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NULL,
                LogDate TEXT NOT NULL,
                Notes TEXT NULL
            )
        """)

        
        # WorkoutLog table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS WorkoutLog (
                WorkoutLogID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                WorkoutDate TEXT NOT NULL,
                WorkoutType TEXT NOT NULL,
                Duration_min REAL,
                CaloriesBurned INTEGER,
                RunDistance_miles REAL,
                RunPace TEXT
            )
        """)
         
        # FoodLog table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS FoodLog (
                FoodLogID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                FoodLogDate TEXT NOT NULL,
                Breakfast TEXT NULL,
                Lunch TEXT NULL,
                Dinner TEXT NULL,
                Snacks TEXT NULL,
                Liquid TEXT NULL,
                CaloriesIn INTEGER,
                Protein_g INTEGER,
                Carbs_g INTEGER,
                Fat_g INTEGER,
                Water_l INTEGER
            )
        """)

        # Daily Assesment table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS DailyAssesment (
                DailyAssesmentID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                AssesmentDate TEXT NOT NULL,
                Notes TEXT NOT NULL,
                Score INTEGER,
                ScoreSummary TEXT NOT NULL
            )
        """)

        # Weekly Summary table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS WeeklySummary (
                WeeklySummaryID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                AssesmentStartDate TEXT NOT NULL,
                AssesmentEndDate TEXT NOT NULL,
                TrainingScore INTEGER,
                ProteinScore INTEGER,
                CarbsFuelingScore INTEGER,
                CaloriesControlScore INTEGER,
                AlcoholControlScore INTEGER,
                HydrationScore INTEGER,
                OverallScore INTEGER
            )
        """)

        # Daily AI Analysis table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS DailyAIAnalysis (
                AIAnalysisID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                LogDate TEXT NOT NULL,

                InputPayloadJSON TEXT NOT NULL,
                ResponseJSON TEXT,

                PromptVersion TEXT NOT NULL,
                ModelName TEXT NOT NULL,

                Status TEXT NOT NULL CHECK (
                    Status IN ('SUCCESS', 'FAILED', 'PARTIAL', 'PENDING')
                ),

                ErrorMessage TEXT,
                CreatedAt TEXT NOT NULL DEFAULT (datetime('now')),
                PromptText TEXT,
                ResponseRaw TEXT,

                UNIQUE (UserID, LogDate, PromptVersion) 
            );
        """)

        conn.commit()
