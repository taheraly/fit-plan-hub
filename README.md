# FitPlanHub - Full Stack Social Fitness Platform 🏋️‍♂️

### **Project Overview**
FitPlanHub is a dynamic full-stack web application designed to connect fitness trainers with health enthusiasts in a simulated marketplace environment. The platform bridges the gap between social networking and e-commerce, allowing trainers to publish digital workout products and users to curate a personalized fitness feed.

Built on a **RESTful architecture**, the application uses **Python (Flask)** for the backend and **Vanilla JavaScript** with **Bootstrap 5** for a modern, responsive frontend. It features a robust **SQLite** database that manages complex relationships, specifically the many-to-many associations required for a social graph (Users following Trainers) and transactional logic (Users subscribing to Plans).

### **Key Features**
* **Role-Based Access Control (RBAC):** Secure authentication distinguishing between "Trainers" (Creators) and "Users" (Consumers) using **JWT (JSON Web Tokens)**.
* **Dynamic Trainer Dashboard:** A dedicated interface for trainers to create, price, and publish workout plans. Data creates an instant API endpoint consumed by the feed.
* **Smart Social Feed:** A personalized feed algorithm that only displays content from trainers the user follows.
* **Discovery Engine:** A "Find Trainers" feature allowing users to browse professionals and manage their social graph.
* **Interactive UI:** Built with Bootstrap 5 for mobile responsiveness, featuring glass-morphism login effects and asynchronous data fetching for a smooth user experience.

### **Tech Stack**
* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-JWT-Extended.
* **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.
* **Database:** SQLite.
* **Version Control:** Git & GitHub.

---

### **🚀 How to Run Locally**

**1. Clone the Repository**
```bash
git clone [https://github.com/ARPIT-29/fit-plan-hub.git](https://github.com/ARPIT-29/fit-plan-hub.git)
cd fit-plan-hub
### 📖 How to Use the App (User Guide)

**1. Create an Account**
* Open the app and click **"Create an Account"**.
* **For Trainers:** Select **"Trainer"** from the dropdown menu. This grants you special permissions to publish content.
* **For Regular Users:** Select **"Regular User"** to browse and buy plans.

**2. Trainer Workflow**
* Log in with your Trainer account.
* On the feed page, click the yellow **"★ Dashboard"** button at the top.
* Fill out the form (Title, Description, Price, Duration) and click **"Publish Plan"**.
* Your plan is now live in the database!

**3. User Workflow**
* Log in with your User account.
* Initially, your feed will be empty. Click **"Find Trainers"** to browse the directory.
* Click **"Follow"** on any trainer you like.
* Switch back to **"My Feed"** to see plans *only* from the trainers you follow.
* Click **"Buy"** to simulate purchasing a plan (this unlocks the full description).