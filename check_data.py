import json
import os

def check_data():
    question_file_path = os.path.dirname(__file__) + '\getQuestionContent.json'
    db_file_path = os.path.dirname(__file__) + '\db数据.json'
    params_file_path = os.path.dirname(__file__) + '\前端参数.json'

    with open(question_file_path, 'r', encoding="UTF-8") as file:
        question_data = file.read()

    with open(db_file_path, 'r', encoding="UTF-8") as file:
        db_data = file.read()

    with open(params_file_path, 'r', encoding="UTF-8") as file:
        params_data = file.read()

    question_data = json.loads(question_data)
    question = question_data["data"]["question"]
    db_data = json.loads(db_data)
    params_data = json.loads(params_data)

    lids = list()
    
    for p in params_data:
        lids.append(str(p["lid"]))

    lids = list(set(lids))
    print(lids)

    flag = True

    for d in db_data:
        if not d["id"] in lids:
            flag = False
            break

    return flag

if __name__ == "__main__":
    check_data()


