import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# 初始化日志记录，并指定编码为UTF-8
logging.basicConfig(
    filename='course_selection.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    encoding='utf-8'
)

# 选课逻辑封装为函数，支持多线程调用
def select_course(course_name, teacher_name):
    # 初始化Edge浏览器驱动
    driver = webdriver.Edge()

    max_attempts = 20  # 最大选课尝试次数
    attempt = 0  # 选课尝试计数

    # 打开本地127.0.0.1的网页（首次执行）
    driver.get("http://127.0.0.1:5000/")
    logging.info(f'{course_name} - {teacher_name}: 成功打开网页')

    # 开始循环选课过程
    while attempt < max_attempts:
        attempt += 1
        logging.info(f'{course_name} - {teacher_name}: 第 {attempt} 次选课尝试')

        try:
            # 等待课程选择框加载并查找课程名称为变量中的课程名的元素并高亮
            wait = WebDriverWait(driver, 10)
            course_element = wait.until(EC.presence_of_element_located((By.XPATH, f"//select[@id='course-select']/option[text()='{course_name}']")))
            driver.execute_script("arguments[0].style.border='3px solid red'", course_element)
            course_element.click()
            logging.info(f'{course_name} - {teacher_name}: 成功选择课程: {course_name}')

            # 查找老师选择框中的老师名称为变量中的老师名的元素并高亮，然后点击
            teacher_element = wait.until(EC.presence_of_element_located((By.XPATH, f"//select[@id='teacher-select']/option[contains(text(), '{teacher_name}')]")))
            driver.execute_script("arguments[0].style.border='3px solid blue'", teacher_element)
            teacher_element.click()
            logging.info(f'{course_name} - {teacher_name}: 成功选择教师: {teacher_name}')

            # 等待保存按钮加载并点击保存按钮
            save_button = wait.until(EC.element_to_be_clickable((By.ID, "save-courses-btn")))
            save_button.click()
            logging.info(f'{course_name} - {teacher_name}: 点击保存按钮')

            # 等待选课状态提示框加载并获取信息
            modal_message = wait.until(EC.visibility_of_element_located((By.ID, "modalMessage")))
            message_text = modal_message.text
            logging.info(f'{course_name} - {teacher_name}: 选课反馈信息: {message_text}')
            print(message_text)

            # 判断选课是否成功
            if "成功选中" in message_text:
                logging.info(f'{course_name} - {teacher_name}: 选课成功，停止操作。第 {attempt} 次选课成功。')
                print(f'{course_name} - {teacher_name}: 选课成功，停止操作。第 {attempt} 次选课成功。')
                close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-footer']//button[@class='btn btn-secondary']")))
                close_button.click()
                logging.info(f'{course_name} - {teacher_name}: 点击关闭按钮')
                break  # 选课成功，退出循环
            elif "选课失败" in message_text:
                logging.info(f'{course_name} - {teacher_name}: 选课失败，第 {attempt} 次选课失败。尝试重新选课。')
                print(f'{course_name} - {teacher_name}: 选课失败，第 {attempt} 次选课失败。尝试重新选课。')
            elif "已经" in message_text:
                logging.info(f'{course_name} - {teacher_name}: 课程已选过啦，停止操作。第 {attempt} 次选课成功。')
                print(f'{course_name} - {teacher_name}: 课程已选过啦，停止操作。第 {attempt} 次选课成功。')
                close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-footer']//button[@class='btn btn-secondary']")))
                close_button.click()
                logging.info(f'{course_name} - {teacher_name}: 点击关闭按钮')
                break
            else:
                logging.warning(f'{course_name} - {teacher_name}: 未知反馈信息: {message_text}')
            
            # 点击模态框中的关闭按钮
            close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='modal-footer']//button[@class='btn btn-secondary']")))
            close_button.click()
            logging.info(f'{course_name} - {teacher_name}: 点击关闭按钮')

        except Exception as e:
            logging.error(f'{course_name} - {teacher_name}: 发生异常: {str(e)}')

        # 暂停一小段时间，模拟重新尝试的延迟
        time.sleep(1)

    # 关闭浏览器
    driver.quit()
    logging.info(f'{course_name} - {teacher_name}: 关闭浏览器')

# 创建多个线程，分别抢不同的课程
threads = []
course_list = [
    {"course_name": "线性代数", "teacher_name": "孙磊"},
    {"course_name": "电路原理", "teacher_name": "罗辉"},
    {"course_name":"工程力学","teacher_name":"李杰"},
]

# 为每个课程创建线程
for course in course_list:
    t = threading.Thread(target=select_course, args=(course["course_name"], course["teacher_name"]))
    threads.append(t)
    t.start()

# 等待所有线程执行完毕
for t in threads:
    t.join()

logging.info('所有选课线程已完成')
