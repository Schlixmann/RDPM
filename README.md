# RDPM:

Resmanipulation provides a REST-Service to automatically alter processmodels based on a resources requirements.

## Use Case Demo:
A Demo of RDPM is hosted on cpee.org. 
To start the demo, clone this repository and run either the file: `open_model.py` or `open_model.ruby`
Add one of the example use cases from the folder "use_cases" as argument.

**Drill Example:**

1. run:

- `python3 open_model.py use_cases/Drill.xml`

  OR
- `ruby open_model.rb use_cases/Drill.xml`

2. A new process instance is opened on the cpee.org demo server. 
2. Choose the Arguments in the section "Properties" to your liking
2. go to the tab "Execution"
2. click "Start"
2. Allocation will be done, Allocated resources are shown under "Resources"->"allocated_to"

**Python or Ruby must be installed to run examples**

In Python `requests` package is required to run `open_model.py`
- run `pip install -r requirements.txt` to get all dependencies for RDPM or `pip install requests` to get requests package.

## Additional Information: 
- Please open a new instance everytime the allocation is done
- Please "abandon" an instance after successfull allocation
- Sometimes a refresh is needed to show the allocation

![Screenshot shows the Cpee interface which will open after running the command](https://github.com/Schlixmann/RDPM/assets/62253687/a12c3817-0859-4125-8bd4-42a5eb2fed4a)

## To Host RDPM Local: 

1. pip install -r requirements.txt
1. change endpoints "allocation" and "resources" in cpee model
1. Add your server config in `server_config` 
1. python3 rest_api.py

