# RDPM:

Resmanipulation provides a REST-Service to automatically alter processmodels based on a resources requirements.

## Demo:
A Demo of RDPM is hosted on cpee.org. 
To start the demo, clone this repository and run either the file: 
- `open_model.py`
  
  OR:
- `open_model.ruby`

Add one of the example use cases from the folder "use_cases" as argument.

**Example:**

1. run:

- `python3 open_model.py use_cases/Drill.xml`

  OR
- `ruby open_model.rb use_cases/Drill.xml`

2. A new process instance is opened on the cpee.org demo server. 
2. Choose the Arguments in the section "Properties" to your liking
2. go to the tab "Execution"
2. click "Start"

![Screenshot shows the Cpee interface which will open after running the command](https://github.com/Schlixmann/RDPM/assets/62253687/a12c3817-0859-4125-8bd4-42a5eb2fed4a)

To Host RDPM Local: 

1. pip install -r requirements.txt
1. run rest_api.py

