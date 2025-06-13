import customtkinter as ctk
from PIL import Image
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
import re
from tkcalendar import DateEntry


# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CyberTodoApp:
    def __init__(self):
        self.root = ctk.CTk()
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.title("CYBER TODO MATRIX")
        self.root.geometry(f"{width}x{height}+0+0")
        
        self.root.configure(fg_color=("#0a0a0a", "#0a0a0a"))
        
        # Database connection
        self.connection = None
        self.setup_database()
        
        # Color scheme - Cyber theme
        self.colors = {
            'bg': '#0a0a0a',
            'card_bg': '#1a1a2e',
            'accent': '#00ffff',
            'accent_dark': '#0066cc',
            'text': '#ffffff',
            'text_dim': '#cccccc',
            'success': '#00ff41',
            'warning': '#ffaa00',
            'danger': '#ff0040'
        }
        
        self.setup_ui()
        self.load_tasks()
    
    def setup_database(self):
        """Setup MySQL database connection and create table if not exists"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='todo_db',  # Change as needed
                user='root',           # Change as needed
                password='root'    # Change as needed
            )
            
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                
                # Create database if not exists
                cursor.execute("CREATE DATABASE IF NOT EXISTS todo_db")
                cursor.execute("USE todo_db")
                
                # Create table if not exists
                create_table_query = """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status ENUM('pending', 'complete', 'incomplete') DEFAULT 'pending',
                    due_date DATE,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
                cursor.execute(create_table_query)
                self.connection.commit()
                
                
        except Error as e:
            messagebox.showerror("Database Error", f"Error connecting to MySQL: {e}")
            
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Content container
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        # Left panel - Add task
        self.create_left_panel(content_frame)
        
        # Right panel - Task list
        self.create_right_panel(content_frame)
    
    def create_header(self, parent):
        """Create the header section"""
        header_frame = ctk.CTkFrame(parent, height=80, fg_color=self.colors['card_bg'], corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        timg = Image.open("t.png")
        
        t_image = ctk.CTkImage(light_image=timg, dark_image=timg,size=(75,75))
        label = ctk.CTkLabel(header_frame, image=t_image, text="")
        label.pack(side="left",padx=15)
        title_label = ctk.CTkLabel(
            header_frame, 
            text="CYBER TODO MATRIX", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors['accent']
        )
        title_label.pack(side="left", padx=5, pady=20)
        simg = Image.open("search.png")
        
        
        # Search section
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=30, pady=20)

        s_image = ctk.CTkImage(light_image=simg, dark_image=simg,size=(30,30))
        slabel = ctk.CTkLabel(search_frame, image=s_image, text="")
        slabel.pack(side="left",padx=15)
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search tasks...",
            width=300,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#2a2a3e", "#2a2a3e"),
            border_color=self.colors['accent']
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_tasks)


        self.date_filter = DateEntry(search_frame,height=10,borderwidth=2,date_pattern='yyyy-mm-dd')
        self.date_filter.pack(side="left",pady=1,padx =10)

        snimg = Image.open("scan.png")
        sn_image = ctk.CTkImage(light_image=snimg, dark_image=snimg,size=(30,30))
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="SCAN",
            width=80,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_dark'],
            text_color="black",
            command=self.scan_btn_q,
            image=sn_image
        )
        search_btn.pack(side="left")
        
        refimg = Image.open("refresh.png")
        ref_image = ctk.CTkImage(light_image=refimg, dark_image=refimg,size=(30,30))
        refresh_btn = ctk.CTkButton(
            search_frame,
            text="REFRESH",
            width=100,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.colors['accent'],
            hover_color=self.colors['accent_dark'],
            text_color="black",
            command=self.search_tasks,
            image=ref_image
        )
        refresh_btn.pack(side="left", padx=5)
    
    def create_left_panel(self, parent):
        """Create the left panel for adding tasks"""
        left_frame = ctk.CTkFrame(parent, width=400, fg_color=self.colors['card_bg'], corner_radius=15)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)
        
        

        
        
        

        # Panel title
        panel_title = ctk.CTkLabel(
            left_frame,
            
            text="INITIALIZE NEW TASK",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        panel_title.pack(pady=(15, 10))
        
        # Task title input
        title_label = ctk.CTkLabel(left_frame, text="TASK IDENTIFIER:", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(anchor="w", padx=25, pady=(10, 5))
        
        self.title_entry = ctk.CTkEntry(
            left_frame,
            placeholder_text="Enter task title...",
            width=350,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#2a2a3e", "#2a2a3e"),
            border_color=self.colors['accent']
        )
        self.title_entry.pack(padx=25, pady=(0, 10))
        
        # Task description
        desc_label = ctk.CTkLabel(left_frame, text="TASK DESCRIPTION:", font=ctk.CTkFont(size=14, weight="bold"))
        desc_label.pack(anchor="w", padx=25, pady=(8, 3))
        
        self.desc_text = ctk.CTkTextbox(
            left_frame,
            width=350,
            height=120,
            font=ctk.CTkFont(size=12),
            fg_color=("#2a2a3e", "#2a2a3e"),
            border_color=self.colors['accent']
        )
        self.desc_text.pack(padx=25, pady=(0, 10))
        
        # Status selection
        status_label = ctk.CTkLabel(left_frame, text="INITIAL STATUS:", font=ctk.CTkFont(size=14, weight="bold"))
        status_label.pack(anchor="w", padx=25, pady=(10, 5))
        
        self.status_combo = ctk.CTkComboBox(
            left_frame,
            values=["pending", "complete", "incomplete"],
            width=350,
            height=35,
            font=ctk.CTkFont(size=14),
            fg_color=("#2a2a3e", "#2a2a3e"),
            border_color=self.colors['accent'],
            button_color=self.colors['accent'],
            button_hover_color=self.colors['accent_dark']
        )
        self.status_combo.pack(padx=25, pady=(0, 10))
        self.status_combo.set("pending")

        dpimg = Image.open("deploy.png")
        dp_image = ctk.CTkImage(light_image=dpimg, dark_image=dpimg,size=(30,30))
        # Add button
        add_btn = ctk.CTkButton(
            left_frame,
            text="DEPLOY TASK",
            width=350,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#00cc33",
            text_color="black",
            command=self.add_task,
            image=dp_image
        )
        add_btn.pack(padx=25, pady=(0, 15))
        
        # Stats panel
        self.create_stats_panel(left_frame)
    
    def create_stats_panel(self, parent):
        """Create statistics panel"""
        stats_frame = ctk.CTkFrame(parent, fg_color=("#2a2a3e", "#2a2a3e"), corner_radius=10)
        stats_frame.pack(fill="x", padx=25, pady=(5, 15))
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 SYSTEM STATUS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['accent']
        )
        stats_title.pack(pady=(5))
        
        # Stats labels
        self.total_label = ctk.CTkLabel(stats_frame, text="TOTAL TASKS: 0", font=ctk.CTkFont(size=12))
        self.total_label.pack(pady=2)
        
        self.pending_label = ctk.CTkLabel(stats_frame, text="PENDING: 0", font=ctk.CTkFont(size=12), text_color=self.colors['warning'])
        self.pending_label.pack(pady=1)
        
        self.complete_label = ctk.CTkLabel(stats_frame, text="COMPLETE: 0", font=ctk.CTkFont(size=12), text_color=self.colors['success'])
        self.complete_label.pack(pady=1)
        
        self.incomplete_label = ctk.CTkLabel(stats_frame, text="INCOMPLETE: 0", font=ctk.CTkFont(size=12), text_color=self.colors['danger'])
        self.incomplete_label.pack(pady=(2))
    
    def create_right_panel(self, parent):
        """Create the right panel for task list"""
        right_frame = ctk.CTkFrame(parent, fg_color=self.colors['card_bg'], corner_radius=15)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Panel title
        panel_title = ctk.CTkLabel(
            right_frame,
            text="📋 ACTIVE TASK MATRIX",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['accent']
        )
        panel_title.pack(pady=(25, 20))
        
        # Task list container
        self.task_container = ctk.CTkScrollableFrame(
            right_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.task_container.pack(fill="both", expand=True, padx=25, pady=(0, 25))
    
    def add_task(self):
        """Add a new task to the database"""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", "end-1c").strip()
        status = self.status_combo.get()
        
        if not title:
            messagebox.showwarning("Input Error", "Task title is required!")
            return
        
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO tasks (title, description, status, created_date)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (title, description, status, date.today()))
            self.connection.commit()
            
            # Clear inputs
            self.title_entry.delete(0, "end")
            self.desc_text.delete("1.0", "end")
            self.status_combo.set("pending")
            
            # Reload tasks
            self.load_tasks()
            
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding task: {e}")
    
    def load_tasks(self, search_query=None):
        """Load tasks from database"""
        # Clear existing tasks
        for widget in self.task_container.winfo_children():
            widget.destroy()
        
        try:
            cursor = self.connection.cursor()
            if search_query:
                query = """
                SELECT id, title, description, status, created_date, updated_date
                FROM tasks 
                WHERE title LIKE %s OR description LIKE %s
                ORDER BY created_date DESC, updated_date DESC
                """
                search_term = f"%{search_query}%"
                cursor.execute(query, (search_term, search_term))
            else:
                query = """
                SELECT id, title, description, status, created_date, updated_date
                FROM tasks 
                ORDER BY created_date DESC, updated_date DESC
                """
                cursor.execute(query)
            
            tasks = cursor.fetchall()
            
            if not tasks:
                no_tasks_label = ctk.CTkLabel(
                    self.task_container,
                    text="🌌 NO TASKS IN THE MATRIX",
                    font=ctk.CTkFont(size=16),
                    text_color=self.colors['text_dim']
                )
                no_tasks_label.pack(pady=50)
            else:
                for task in tasks:
                    self.create_task_widget(task)
            
            # Update stats
            self.update_stats()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading tasks: {e}")
    
    def create_task_widget(self, task):
        """Create a widget for individual task"""
        task_id, title, description, status, created_date, updated_date = task
        
        # Task frame
        task_frame = ctk.CTkFrame(
            self.task_container,
            fg_color=("#2a2a3e", "#2a2a3e"),
            corner_radius=10,
            border_width=2,
            border_color=self.get_status_color(status)
        )
        task_frame.pack(fill="x", pady=5, padx=5)
        
        # Task header
        header_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        # Title and status
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x")
        
        task_title = ctk.CTkLabel(
            title_frame,
            text=f"🎯 {title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        task_title.pack(side="left", fill="x", expand=True)
        
        # Status dropdown
        status_combo = ctk.CTkComboBox(
            title_frame,
            values=["pending", "complete", "incomplete"],
            width=120,
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color=self.get_status_color(status),
            text_color="black",
            command=lambda new_status, tid=task_id: self.update_task_status(tid, new_status)
        )
        status_combo.pack(side="right", padx=(10, 0))
        status_combo.set(status)
        
        # Description
        if description:
            desc_label = ctk.CTkLabel(
                task_frame,
                text=description[:100] + ("..." if len(description) > 100 else ""),
                font=ctk.CTkFont(size=18),
                text_color=self.colors['text_dim'],
                anchor="w",
                justify="left"
            )
            desc_label.pack(fill="x", padx=15, pady=(0, 5))
        
        # Footer with dates and delete button
        footer_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        date_info = ctk.CTkLabel(
            footer_frame,
            text=f"📅 Created: {created_date} | Updated: {updated_date.strftime('%Y-%m-%d %H:%M')}",
            font=ctk.CTkFont(size=10),
            text_color=self.colors['text_dim']
        )
        date_info.pack(side="left")
        
        delimg = Image.open("del.png")
        del_image = ctk.CTkImage(light_image=delimg, dark_image=delimg,size=(30,30))
        delete_btn = ctk.CTkButton(
            footer_frame,
            text="",
            width=30,
            height=30,
            font=ctk.CTkFont(size=14),
            fg_color=self.colors['danger'],
            hover_color="#cc0033",
            command=lambda tid=task_id: self.delete_task(tid),
            image=del_image
        )
        delete_btn.pack(side="right")
    
    def get_status_color(self, status):
        """Get color based on status"""
        colors = {
            'pending': self.colors['warning'],
            'complete': self.colors['success'],
            'incomplete': self.colors['danger']
        }
        return colors.get(status, self.colors['accent'])
    
    def update_task_status(self, task_id, new_status):
        """Update task status in database"""
        try:
            cursor = self.connection.cursor()
            query = "UPDATE tasks SET status = %s WHERE id = %s"
            cursor.execute(query, (new_status, task_id))
            self.connection.commit()
            self.load_tasks()
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating task: {e}")
    
    def delete_task(self, task_id):

        """Delete task from database"""
        
        cursor = self.connection.cursor()
        query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(query, (task_id,))
        self.connection.commit()
        self.load_tasks()
                
            
    
    def search_tasks(self, event=None):
        """Search tasks based on query"""
        search_query = self.search_entry.get().strip()
        self.load_tasks(search_query if search_query else None)
    
    def update_stats(self):
        """Update statistics display"""
        try:
            cursor = self.connection.cursor()
            
            # Total tasks
            cursor.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]
            
            # Status counts
            cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
            status_counts = dict(cursor.fetchall())
            
            pending = status_counts.get('pending', 0)
            complete = status_counts.get('complete', 0)
            incomplete = status_counts.get('incomplete', 0)
            
            self.total_label.configure(text=f"TOTAL TASKS: {total}")
            self.pending_label.configure(text=f"PENDING: {pending}")
            self.complete_label.configure(text=f"COMPLETE: {complete}")
            self.incomplete_label.configure(text=f"INCOMPLETE: {incomplete}")
            
        except Error as e:
            exit()
    def scan_date(self,s_date=None):
        for widget in self.task_container.winfo_children():
            widget.destroy()

        try:
            cursor = self.connection.cursor()
            if s_date:
                query = """SELECT id,title,description,status,created_date,updated_date 
                FROM tasks 
                WHERE DATE(created_date) = %s
                ORDER BY created_date 
                """

                
                cursor.execute(query,(s_date,))

            else:
                query = """
                SELECT id, title, description, status, created_date, updated_date
                FROM tasks 
                ORDER BY created_date DESC, updated_date DESC
                """
                cursor.execute(query)
            tasks = cursor.fetchall()
            
            if not tasks:
                text_display = "🌌 NO TASKS IN THE MATRIX ON THE DATE: " + str(s_date)
                no_tasks_label = ctk.CTkLabel(
                    self.task_container,
                    text=text_display,
                    font=ctk.CTkFont(size=16),
                    text_color=self.colors['text_dim']
                )
                no_tasks_label.pack(pady=50)
            else:
                for task in tasks:
                    self.create_task_widget(task)
            
            # Update stats
            self.update_stats()
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading tasks: {e}")

    def scan_btn_q(self,event=None):
        
        scan_dateee = self.date_filter.get_date()
        print(scan_dateee)
        self.scan_date(scan_dateee if scan_dateee else None)

    def on_closing(self):
        """Handle application closing"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
        self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # Run the application
    app = CyberTodoApp()
    app.run()