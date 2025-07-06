import sqlite3
import json
from datetime import datetime

class QuestionDatabase:
    def __init__(self, unsent_db='unsent_questions.db', sent_db='sent_questions.db'):
        self.unsent_db = unsent_db
        self.sent_db = sent_db
        self.setup_databases()
    
    def setup_databases(self):
        """Create both databases with proper tables"""
        # Setup unsent questions database
        conn = sqlite3.connect(self.unsent_db)
        cursor = conn.cursor()
        
        create_unsent_table = """
        CREATE TABLE IF NOT EXISTS practice_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            resource TEXT NOT NULL,
            sent BOOLEAN DEFAULT FALSE,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_unsent_table)
        conn.commit()
        cursor.close()
        conn.close()
        
        # Setup sent questions database
        conn = sqlite3.connect(self.sent_db)
        cursor = conn.cursor()
        
        create_sent_table = """
        CREATE TABLE IF NOT EXISTS sent_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_id INTEGER,
            subject TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            answer TEXT NOT NULL,
            explanation TEXT NOT NULL,
            resource TEXT NOT NULL,
            sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_sent_table)
        conn.commit()
        cursor.close()
        conn.close()
    
    def populate_from_questions(self, questions_dict):
        """Populate the unsent database with questions from questions.py"""
        conn = sqlite3.connect(self.unsent_db)
        cursor = conn.cursor()
        
        # Check if database is already populated
        cursor.execute("SELECT COUNT(*) FROM practice_problems")
        count = cursor.fetchone()[0]
        
        if count == 0:
            for subject, question_list in questions_dict.items():
                for question_data in question_list:
                    cursor.execute("""
                        INSERT INTO practice_problems 
                        (subject, question, options, answer, explanation, resource)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        subject,
                        question_data['question'],
                        json.dumps(question_data['options']),
                        question_data['answer'],
                        question_data['explanation'],
                        question_data['resource']
                    ))
            
            conn.commit()
            print(f"Populated database with {len(questions_dict)} subjects and their questions")
        else:
            print(f"Database already contains {count} questions")
        
        cursor.close()
        conn.close()
    
    def get_random_unsent_question(self):
        """Get a random unsent question from the database"""
        conn = sqlite3.connect(self.unsent_db)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, subject, question, options, answer, explanation, resource 
            FROM practice_problems 
            WHERE sent = FALSE 
            ORDER BY RANDOM() 
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'subject': result[1],
                'question': result[2],
                'options': json.loads(result[3]),
                'answer': result[4],
                'explanation': result[5],
                'resource': result[6]
            }
        return None
    
    def mark_question_as_sent(self, question_id):
        """Mark a question as sent and move it to the sent database"""
        conn = sqlite3.connect(self.unsent_db)
        cursor = conn.cursor()
        
        # Get the question data
        cursor.execute("""
            SELECT subject, question, options, answer, explanation, resource 
            FROM practice_problems 
            WHERE id = ?
        """, (question_id,))
        
        question_data = cursor.fetchone()
        
        if question_data:
            # Mark as sent in unsent database
            cursor.execute("""
                UPDATE practice_problems 
                SET sent = TRUE 
                WHERE id = ?
            """, (question_id,))
            
            # Move to sent database
            sent_conn = sqlite3.connect(self.sent_db)
            sent_cursor = sent_conn.cursor()
            
            sent_cursor.execute("""
                INSERT INTO sent_problems 
                (original_id, subject, question, options, answer, explanation, resource)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (question_id, *question_data))
            
            sent_conn.commit()
            sent_cursor.close()
            sent_conn.close()
            
            conn.commit()
            print(f"Question {question_id} marked as sent and moved to sent database")
        
        cursor.close()
        conn.close()
    
    def get_stats(self):
        """Get statistics about questions in both databases"""
        conn = sqlite3.connect(self.unsent_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM practice_problems WHERE sent = FALSE")
        unsent_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM practice_problems WHERE sent = TRUE")
        sent_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            'unsent': unsent_count,
            'sent': sent_count,
            'total': unsent_count + sent_count
        }

# Initialize the database manager
db_manager = QuestionDatabase()

# Create the table (keeping original functionality for backward compatibility)
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS practice_problems (
    sent BOOLEAN,
    question VARCHAR(100),
    resources VARCHAR(100)
);
"""

cursor.execute(create_table_query)
conn.commit()

# Close the connection
cursor.close()
conn.close()