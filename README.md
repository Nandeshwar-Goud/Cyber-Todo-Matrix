# Cyber-Todo-Matrix
This is a todo project built with customtkinter.


## Description
➡️ This is built to explore the custom tkinter library.

➡️ CustomTkinter is a powerful Python UI library that modernizes the traditional Tkinter framework with contemporary widgets, themes, and styling options. This library allows developers to create visually appealing applications while maintaining the simplicity and cross-platform compatibility that made Tkinter popular.

🛢️ I used MYSQL to save the tasks in the DataBase and fetch them from the DataBase.

➡️ Just used the cyber theme with a search bar, date filter button with date entry menu, and refresh button.

☰ Search uses keyrelease event and fetches the matched title from the database and shows the information on the frame which is created for the task views.

📅 Datefilter uses the input date, which can be taken from the date entry menu, and fetches all tasks on the date created.

➜ Left side, we have the title task and description, and a deploy button. So, one can add the task, and the date will be saved from the current timestamp. We can also see the total task with the count of their status
.

➜Right side, we have all the tasks with information, and an individual delete button on each of them.
### 🇵🇾 Python Libraries used.
<ol>
<li>customtkinter</li>
  <li>mysql.connector</li>
  <li>PIL(pillow)</li>
  <li>tkinter</li>
  <li>tkcalendar</li>
</ol>

### 🔑 Initial credentials in code
<ul>
  <li>host='localhost'</li>
  <li>database='todo_db' </li>
  <li>user='root' </li>         
  <li>password='root' </li>
  
</ul>

### 🗄️ Database Schema


![Screenshot 2025-06-13 202125](https://github.com/user-attachments/assets/e1d94497-5399-4595-af78-02e6303629b9)

### 📱 Screenshot Of UI

![Screenshot 2025-06-13 200747](https://github.com/user-attachments/assets/291c0a21-3ba0-4566-9317-522bd47e78a6)






























