#!/usr/bin/env python3
"""
Database Management Utility for Daily Questions System
"""
import sqlite3
import json
from db import db_manager
from questions import questions

def view_sent_questions(limit=10):
    """View recently sent questions"""
    conn = sqlite3.connect(db_manager.sent_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT original_id, subject, question, sent_date 
        FROM sent_problems 
        ORDER BY sent_date DESC 
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    print(f"\nRecently Sent Questions (last {limit}):")
    print("-" * 50)
    for row in results:
        print(f"ID: {row[0]} | Subject: {row[1]} | Date: {row[2]}")
        print(f"Question: {row[2][:100]}...")
        print()

def view_unsent_questions(limit=10):
    """View unsent questions"""
    conn = sqlite3.connect(db_manager.unsent_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, subject, question 
        FROM practice_problems 
        WHERE sent = FALSE 
        ORDER BY created_date 
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    print(f"\nUnsent Questions (next {limit}):")
    print("-" * 50)
    for row in results:
        print(f"ID: {row[0]} | Subject: {row[1]}")
        print(f"Question: {row[2][:100]}...")
        print()

def reset_all_questions():
    """Reset all questions to unsent status"""
    print("This will reset all questions to unsent status.")
    confirm = input("Are you sure? (y/N): ")
    
    if confirm.lower() == 'y':
        # Clear sent database
        conn = sqlite3.connect(db_manager.sent_db)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sent_problems")
        conn.commit()
        cursor.close()
        conn.close()
        
        # Reset all questions in unsent database
        conn = sqlite3.connect(db_manager.unsent_db)
        cursor = conn.cursor()
        cursor.execute("UPDATE practice_problems SET sent = FALSE")
        conn.commit()
        cursor.close()
        conn.close()
        
        print("All questions have been reset to unsent status.")
    else:
        print("Reset cancelled.")

def export_sent_questions():
    """Export sent questions to a JSON file"""
    conn = sqlite3.connect(db_manager.sent_db)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT original_id, subject, question, options, answer, explanation, resource, sent_date 
        FROM sent_problems 
        ORDER BY sent_date DESC
    """)
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    sent_questions = []
    for row in results:
        sent_questions.append({
            'original_id': row[0],
            'subject': row[1],
            'question': row[2],
            'options': json.loads(row[3]),
            'answer': row[4],
            'explanation': row[5],
            'resource': row[6],
            'sent_date': row[7]
        })
    
    with open('sent_questions_export.json', 'w') as f:
        json.dump(sent_questions, f, indent=2)
    
    print(f"Exported {len(sent_questions)} sent questions to sent_questions_export.json")

def main():
    """Main menu for database management"""
    while True:
        print("\n" + "="*50)
        print("Daily Questions Database Manager")
        print("="*50)
        print("1. View database statistics")
        print("2. View recently sent questions")
        print("3. View unsent questions")
        print("4. Reset all questions to unsent")
        print("5. Export sent questions to JSON")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == '1':
            stats = db_manager.get_stats()
            print(f"\nDatabase Statistics:")
            print(f"  Unsent questions: {stats['unsent']}")
            print(f"  Sent questions: {stats['sent']}")
            print(f"  Total questions: {stats['total']}")
            
        elif choice == '2':
            limit = input("How many recent questions to show? (default 10): ")
            limit = int(limit) if limit.isdigit() else 10
            view_sent_questions(limit)
            
        elif choice == '3':
            limit = input("How many unsent questions to show? (default 10): ")
            limit = int(limit) if limit.isdigit() else 10
            view_unsent_questions(limit)
            
        elif choice == '4':
            reset_all_questions()
            
        elif choice == '5':
            export_sent_questions()
            
        elif choice == '6':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 