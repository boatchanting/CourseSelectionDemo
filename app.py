from flask import Flask, render_template, request, jsonify
import pandas as pd
import random
print("运行后请使用chrome浏览器打开http://127.0.0.1:5000/")
print("没有做其他浏览器的适配，推荐使用chrome浏览器！")
app = Flask(__name__)

# 定义 CSV 文件路径
CSV_FILE = 'courses.csv'

# 读取课程信息的函数
def load_courses():
    df = pd.read_csv(CSV_FILE)
    courses = []
    grouped = df.groupby('course_id')

    for course_id, group in grouped:
        course_name = group.iloc[0]['course_name']
        teachers = []

        for _, row in group.iterrows():
            teachers.append({
                'name': row['teacher_name'],
                'capacity': row['capacity'],
                'selected_count': row['selected_count']
            })

        courses.append({
            'id': course_id,
            'name': course_name,
            'teachers': teachers
        })
    
    return courses

# 保存课程信息的函数
def save_courses(courses):
    rows = []
    for course in courses:
        for teacher in course['teachers']:
            rows.append({
                'course_id': course['id'],
                'course_name': course['name'],
                'teacher_name': teacher['name'],
                'capacity': teacher['capacity'],
                'selected_count': teacher['selected_count']
            })
    
    df = pd.DataFrame(rows)
    df.to_csv(CSV_FILE, index=False)

# 加载课程信息
courses = load_courses()

# 模拟选课状态
selected_courses = []

@app.route('/')
def index():
    return render_template('index.html', courses=courses)


@app.route('/select_course', methods=['POST'])
def select_course():
    course_id = int(request.json.get('course_id'))
    teacher_name = request.json.get('teacher_name')

    # 查找对应的课程
    course = next((course for course in courses if course['id'] == course_id), None)
    if not course:
        return jsonify(success=False, message='课程不存在！')

    # 查找对应的老师
    teacher = next((teacher for teacher in course['teachers'] if teacher['name'] == teacher_name), None)
    if not teacher:
        return jsonify(success=False, message='老师不存在！')

    # 检查是否已经选过这门课程下的老师
    if any(selected['course_id'] == course_id for selected in selected_courses):
        return jsonify(success=False, message='您已经为该课程选过老师！')

    # 检查该老师的课程是否已满
    if teacher['selected_count'] >= teacher['capacity']:
        return jsonify(success=False, message=f'{teacher_name}的课程已满！')

    # 随机 20% 概率成功选课
    if random.random() > 0.2:  # 80% 概率失败
        return jsonify(success=False, message='选课失败！请再试试！')

    # 选课成功，更新已选课程和老师的选课人数
    selected_courses.append({'course_id': course_id, 'course_name': course['name'], 'teacher_name': teacher_name})
    teacher['selected_count'] += 1
    
    # 保存最新的课程信息到 CSV 文件
    save_courses(courses)
    
    return jsonify(success=True, message=f'成功选中{course["name"]}的{teacher_name}老师！', selected_courses=selected_courses)


@app.route('/drop_course', methods=['POST'])
def drop_course():
    course_id = int(request.json.get('course_id'))
    teacher_name = request.json.get('teacher_name')

    # 查找对应的课程
    course = next((course for course in courses if course['id'] == course_id), None)
    if not course:
        return jsonify(success=False, message='课程不存在！')

    # 查找对应的老师
    teacher = next((teacher for teacher in course['teachers'] if teacher['name'] == teacher_name), None)
    if not teacher:
        return jsonify(success=False, message='老师不存在！')

    # 查找该课程是否在已选列表中
    selected_course = next((selected for selected in selected_courses if selected['course_id'] == course_id and selected['teacher_name'] == teacher_name), None)
    if not selected_course:
        return jsonify(success=False, message='您未选过该课程！')

    # 从已选课程中移除
    selected_courses.remove(selected_course)
    teacher['selected_count'] -= 1  # 减少教师的选课人数

    # 保存最新的课程信息到 CSV 文件
    save_courses(courses)

    return jsonify(success=True, message=f'成功退选{course["name"]}的{teacher_name}老师！', selected_courses=selected_courses)


@app.route('/get_selected_courses', methods=['GET'])
def get_selected_courses():
    return jsonify(selected_courses)


if __name__ == '__main__':
    app.run(debug=True)
