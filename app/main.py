from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

#TODO Fix recitation hours to be correct for this semester.
RECITATION_HOURS = {"a": "10:00~10:50", "b": "10:00~10:50",
                    "c": "13:00~13:50", "d": "13:00~13:50", "e":"14:00~14:50", "f": "14:00~14:50"}
MICROSERVICE_LINK = "https://cmu-313.github.io/section_info/"


@app.get("/section_info/{section_id}")
def get_section_info(section_id: str):

    if section_id is None:
        raise HTTPException(status_code=404, detail="Missing section id")

    section_id = section_id.lower()

    response = requests.get(MICROSERVICE_LINK + section_id + ".json")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Invalid section id")

    # You can check out what the response body looks like in terminal using the print statement
    data = response.json()
    print(data)
    # Note: some sections have only one TA
    ta_name_list = data["ta"]
    print(ta_name_list)

    # TODO Fix this to return correct values for correct sections.
    if section_id in RECITATION_HOURS:
        return {
            "section": section_id,
            "start_time": RECITATION_HOURS[section_id][0:5],
            "end_time": RECITATION_HOURS[section_id][6:],
            "ta": ta_name_list
        }
    else:
        raise HTTPException(status_code=404, detail="Invalid section id")
