import sqlite3
import argparse
import logging
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db_file = "tasks.db"

def init_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) NOT NULL DEFAULT 'pending'
            )
        ''')
        conn.commit()

def add_task(title, description, due_date):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)", (title, description, due_date))
        conn.commit()
    logging.info(f"Task '{title}' add.")

def update_task(task_id, status):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
    logging.info(f"Task status {task_id} was changed to '{status}'.")

def delete_task(task_id):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    logging.info(f"Task {task_id} was deleted.")

def list_tasks():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, due_date, status FROM tasks ORDER BY due_date")
        tasks = cursor.fetchall()
        for task in tasks:
            print(task)

def main():
    parser = argparse.ArgumentParser(description="Task manager")
    subparsers = parser.add_subparsers(dest="command")
    
    parser_add = subparsers.add_parser("add", help="Add task")
    parser_add.add_argument("title", help="Task title")
    parser_add.add_argument("description", help="Task description")
    parser_add.add_argument("due_date", help="Task due_date(YYYY-MM-DD)")
    
    parser_update = subparsers.add_parser("update", help="Update task status")
    parser_update.add_argument("task_id", type=int, help="ID of the task")
    parser_update.add_argument("status", choices=["pending", "in_progress", "completed"], help="New status")
    
    parser_delete = subparsers.add_parser("delete", help="Delete task")
    parser_delete.add_argument("task_id", type=int, help="ID of the task")
    
    parser_list = subparsers.add_parser("list", help="Show all tasks")
    
    args = parser.parse_args()
    
    init_db()
    
    if args.command == "add":
        add_task(args.title, args.description, args.due_date)
    elif args.command == "update":
        update_task(args.task_id, args.status)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "list":
        list_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
