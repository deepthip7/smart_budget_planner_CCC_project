#  Smart Budget Planner — Dynamic Programming

A **Smart Budget Optimization System** that helps users select the best combination of items within a given budget using the **0/1 Knapsack Algorithm**.

This project demonstrates how **Dynamic Programming (DP)** can be applied to solve real-world decision-making problems like shopping within constraints.

---

##  Features

-  Uses **0/1 Knapsack Algorithm** for optimal selection  
-  **Tkinter GUI Application** for interactive experience  
-  Optional **Web Interface (HTML/CSS/JS)**  
-  Displays **DP Table Visualization**  
-  Add custom items dynamically  
-  Preloaded dataset of common items  
-  Real-time calculation of:
  - Total value
  - Total cost
  - Remaining budget  

---

##  Problem Statement

Given:
- A set of items (each with **price** and **value**)
- A fixed **budget**

###  Goal
Select items such that:
> **Total value is maximized without exceeding the budget**

---

##  Algorithm Used

### 0/1 Knapsack (Dynamic Programming)

- Each item can either be:
  - ✅ Selected  
  - ❌ Not selected  

- DP builds a table:
  - Rows → Items  
  - Columns → Budget values  

- Final solution is obtained using **backtracking**

---

###  Complexity

- **Time Complexity:**  
O(N × W)

- **Space Complexity:**  
O(N × W)

---

##  Project Structure
Smart-Budget-Planner
│
├── knapsack.py # Core DP logic

├── items_data.py # Sample items dataset

├── cli_version.py # CLI version 

├── main.py # Tkinter GUI application

├── index.html # Web version

└── README.md # Project documentation

---

##  How to Run

###  CLI Version
Run in terminal:
python cli_version.py

---

###  GUI Version 
python main.py

---

###  Web Version
Open:
index.html
in your browser.

---

##  Sample Input

| Item        | Price (₹) | Value |
|------------|----------|-------|
| Laptop     | 55000    | 95    |
| Smartphone | 20000    | 85    |
| Book       | 600      | 70    |

---

##  Sample Output

---
![Dark mode](https://github.com/user-attachments/assets/d12939d3-6d66-427a-81e9-04d218bbf706)

![Dark mode](https://github.com/user-attachments/assets/64c14180-b7a0-40d0-8491-5b8ce1430d18)


##  Key Concepts Learned

- Dynamic Programming (DP)
- Optimization Problems
- Space-Time Tradeoffs
- Backtracking technique
- Real-world application of algorithms

---

##  Limitations

- Works only for **0/1 selection**
- Large budgets → higher memory usage
- Value depends on user preference 

---

##  Future Enhancements

- 📱 Mobile application version  
- ☁️ Cloud-based recommendation system  
- 🧠 AI-based value prediction  
- 📊 Graph-based visual analytics  
- 💸 Multi-budget comparison  

---


##  How This Project Stands Out

- Combines **theory + real-world application**
- Includes **CLI + GUI + Web version**
- Visualizes **DP table for better understanding**
- Clean and user-friendly design

---
