# Vaccine_Slot_Check
This repo would help you to find available slots for a particular pincode.

# Output
![image](https://user-images.githubusercontent.com/21328515/117718157-5c649200-b1f9-11eb-8e6f-50cd1ce75217.jpeg)

## APIs
Using Co-Win's [Public APIs](https://apisetu.gov.in/public/marketplace/api/cowin).

## Scope
It's a simple script which will fetch the avaiable slots for a particular pincode and email the results to the recipients in a readable tabular manner. 
As this script isn't deployed anywhere the user would need to keep his/her system up and running for the time he/she wants to track the slots. 

## Get Started
- After installing all the necessary libraries, enter recipients email, sender's email, sender's password in SendEmail.py(make sure to allow less secure apps to make changes in gmail)
- Enter your 'User-Agent' in FetchAPIData.py
- Run the code.
- User would be prompted to enter a pincode.
- After entering the correct pincode, the script would hit the API every 10 seconds and would mail the slots (if available)

## Contributions
Contributions are welcomed. Especially related to hosting this to cloud.
