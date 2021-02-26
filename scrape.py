import json
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "/Users/asriyan/chromedriver"
driver = webdriver.Chrome(PATH)
BASE_URL = "https://www.udemy.com"
EXAM_URL = "/course/aws-certified-cloud-practitioner-practice-test/learn/quiz/4426390#overview"

data = {
    "exam_number": "2",
    "exam_type": "Cloud Practitioner",
    "time": "5400000",
    "current_question": 1,
    "is_paused": 0,
    "is_finished": 0,
    "correct": 0,
    "questions": {}
}

# Implicit wait of 4 seconds
driver.implicitly_wait(4)
driver.get("https://www.udemy.com/join/login-popup/")

# Login
nameInput = driver.find_element_by_id("email--1")
nameInput.send_keys(os.environ["EMAIL"])
passInput = driver.find_element_by_id("id_password")
passInput.send_keys(os.environ["PASSWORD"])
passInput.send_keys(Keys.RETURN)

driver.get(BASE_URL+EXAM_URL)

# Tests have already been completed
# Click "begin test" button
# button = driver.find_elements_by_xpath(
#     '/html/body/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div/div/footer/div[3]/button[1]')
# button.click()

# # Click "stop" button
# stopButton = driver.find_elements_by_xpath(
#     "/html/body/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/button[2]")
# stopButton.click()

# # Click "finish test" button
# finishTestButton = driver.find_elements_by_xpath(
#     "/html/body/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div[3]/button[2]")
# finishTestButton.click()

# Click "review questions" button
reviewPane = driver.find_element_by_class_name(
    "fx-lt")
reviewQuestions = reviewPane.find_elements_by_tag_name("button")[0]
reviewQuestions.click()

# Select panel body
container = driver.find_elements_by_xpath(
    "/html/body/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div")

questionIndex = 0
# Loop all questions
for questions in container:
    questionContainer = questions.find_element_by_css_selector(
        "div[class^='detailed-result-panel--question-container']")

    # get question text
    questionText = questionContainer.find_elements_by_xpath(
        './/*[@id="question-prompt"]/p').text
    # Initialize entry
    newEntry = {
        "question": questionText,
        "explanation": "",
        "is_multiple_choice": 1,
        "status": 0,
        "answers": {}
    }
    answersContainer = questionContainer.find_elements_by_xpath(
        './/div/div[2]/form/ul')
    # Get answers
    answerIndex = 0
    for answer in answersContainer:
        answerText = answer.find_elements_by_xpath(
            './/div/label/div[2]/div/div/div/p').text

        correctEl = answer.find_element_by_css_selector(
            "div[class^='correct']")
        is_correct = 1 if correctEl else 0
        newAnswerEntry = {
            "choice": answerText,
            "is_selected": 0,
            "is_correct": is_correct
        }
        newEntry["answers"][answerIndex] = newAnswerEntry
        answerIndex += 1

    is_multiple_choice = 1 if len(
        newEntry["answers"][answerIndex-1]) == 4 else 0

    newEntry["is_multiple_choice"] = is_multiple_choice
    # Get explanation

    explanationContainer = questionContainer.find_element_by_css_selector(
        "div[class^='mc-quiz-question--explanation']")
    print("explanation", explanationContainer)
    sanitizedHTMLString = re.sub('<div.*?>', '<div>', explanationContainer)
    data["questions"][questionIndex] = newEntry
    questionIndex += 1
    break


# with open("./examData.json", 'w') as fp:
#     json.dump(data, fp)
