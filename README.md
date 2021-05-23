# Cowin-vaccine-tracker
18+ vaccine slot availability notifier through Whatsapp

The script is hosted on heroku and runs every 6 hours to check the slot availability for 18+ in chandigarh and panchkula. 
One can change the district_code in main.py to track the slots in their own district. The user gets notified through whatsapp
if the slot is available at the time of the check. 
Probably would change the notifier from Whatsapp to Telegram due to Twilio Whatsapp Sandbox limitations.
