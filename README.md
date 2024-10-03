# Course Selection Demo

## Introduction

This is a demo project for developing and testing course selection system scripts, built using the Flask framework. The project supports course selection, course withdrawal features, and simulates the random success logic in the course selection process. Users can select courses through the front-end page, and course selection success is determined based on course capacity and the random success mechanism.

## Main Features

- **Course Selection**: Users can select a teacher for a course and submit a course selection request. The system will return the result based on course capacity and a 20% success probability.
- **Course Withdrawal**: Selected courses can be dropped at any time, and the system will update the course's enrolled count.
- **CSV File Storage**: Course and teacher information is stored in a CSV file, and course selection results are updated in real-time.

## Project Structure

```
course_selection_project/
│
├── app.py                    # Flask main application
├── courses.csv                # CSV file for course data
├── templates/
│   └── index.html             # Front-end HTML template
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Usage Instructions

### 1. Clone the Project

First, clone the project to your local machine using `git`:

```bash
git clone https://github.com/your-username/CourseSelectionDemo.git
cd CourseSelectionDemo
```

### 2. Create a Virtual Environment and Install Dependencies

Create a virtual environment and install the project dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows users, use venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Project

Run the following command in the project directory to start the Flask application:

```bash
python app.py
```

Once started, open `http://127.0.0.1:5000/` in your browser to access the course selection system. **It is recommended to use Chrome for better compatibility!**

## CSV File Explanation

Course data is stored in the `courses.csv` file, structured as follows:

```
course_id,course_name,teacher_name,capacity,selected_count
1,Mathematical Analysis,Mr. Zhang,2,0
1,Mathematical Analysis,Mr. Li,1,0
2,Linear Algebra,Mr. Wang,3,0
3,Computer Basics,Mr. Zhao,1,0
3,Computer Basics,Mr. Qian,2,0
```

- `course_id`: Course ID.
- `course_name`: Course name.
- `teacher_name`: Teacher name.
- `capacity`: Course capacity.
- `selected_count`: Current number of enrolled students.

# 测试选课系统

## 简介

这是一个用于开发和测试选课系统脚本的 demo 项目，使用 Flask 框架构建。项目支持课程选择、退课功能，以及模拟选课过程中随机成功的逻辑。用户可以通过前端页面选择课程，并根据课程容量和随机成功机制决定选课是否成功。

## 主要功能

- **课程选择**：用户可以选择某门课程的教师，并提交选课请求。系统会根据课程容量和 20% 的成功概率返回选课结果。
- **退课功能**：已选课程可以随时退选，系统会更新课程的选课人数。
- **CSV 文件存储**：课程和教师信息存储在 CSV 文件中，选课结果会实时更新。

## 项目结构

```
course_selection_project/
│
├── app.py                    # Flask 主应用程序
├── courses.csv                # 课程数据的 CSV 文件
├── templates/
│   └── index.html             # 前端 HTML 模板
├── requirements.txt           # 项目依赖文件
└── README.md                  # 项目说明文档
```

## 使用说明

### 1. 克隆项目

首先，使用 `git` 克隆项目到本地：

```bash
git clone https://github.com/your-username/CourseSelectionDemo.git
cd CourseSelectionDemo
```

### 2. 创建虚拟环境并安装依赖

创建一个虚拟环境并安装项目的依赖项：

```bash
python3 -m venv venv
source venv/bin/activate  # 对于 Windows 用户，使用 venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 运行项目

在项目目录下运行以下命令启动 Flask 应用程序：

```bash
python app.py
```

启动后，在浏览器中访问 `http://127.0.0.1:5000/` 来使用选课系统，**推荐使用chrome浏览器访问！**

## CSV 文件说明

课程数据存储在 `courses.csv` 文件中，格式如下：

```
course_id,course_name,teacher_name,capacity,selected_count
1,数学分析,张老师,2,0
1,数学分析,李老师,1,0
2,线性代数,王老师,3,0
3,计算机基础,赵老师,1,0
3,计算机基础,钱老师,2,0
```

- `course_id`: 课程 ID。
- `course_name`: 课程名称。
- `teacher_name`: 教师名称。
- `capacity`: 课程容量。
- `selected_count`: 当前选课人数。

### 选课机制

- 用户每次选择一门课程时，系统会随机决定是否选课成功，有 20% 的成功概率。
- 课程满员时，选课将自动失败。
- 成功选课后，CSV 文件中的 `selected_count` 会实时更新。



### Course Selection Mechanism

- Each time a user selects a course, the system will randomly determine whether the selection is successful with a 20% success probability.
- When a course is full, the selection will automatically fail.
- After a successful selection, the `selected_count` in the CSV file will be updated in real-time.
