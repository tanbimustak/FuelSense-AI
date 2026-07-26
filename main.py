import pandas as pd
import json
import random
import smtplib
from email.message import EmailMessage
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
 


dataset_json = json.dumps({
    "log": [
        "Pump 1 stopped suddenly",
        "Nozzle jammed at pump 3",
        "Compressor overheated during refill",
        "Motor vibration detected in pump 2",
        "Pump 5 making unusual noise",
        "Short circuit at control board",
        "Display malfunction at dispenser 4",
        "Voltage fluctuation detected at control unit",
        "Fuse blown in circuit panel",
        "Power surge detected at dispenser",
        "Fuel leakage detected at station 2",
        "Smoke detected near dispenser 5",
        "Overheating detected in pump area",
        "Fire alarm triggered at fuel bay",
        "Fuel overflow in underground tank",
        "Low fuel pressure detected at pump 7",
        "Pressure drop in main fuel line",
        "High pressure alarm triggered at dispenser",
        "Pressure valve stuck at dispenser 3",
        "Temperature sensor not responding at pump 6",
        "Fuel flow sensor sending wrong data",
        "Sensor calibration failed at pump 8",
        "Level sensor disconnected at dispenser",
        "Sensor not showing correct value",
        "Internet connection lost at pump controller",
        "Network timeout error at station 9",
        "Data not uploading to server from dispenser",
        "Communication failure between sensors at pump 10",
        "WiFi signal weak at fuel station control unit"
    ],
    "label": [
        "Mechanical failure",
        "Mechanical failure",
        "Mechanical failure",
        "Mechanical failure",
        "Mechanical failure",
        "Electrical issue",
        "Electrical issue",
        "Electrical issue",
        "Electrical issue",
        "Electrical issue",
        "Safety hazard",
        "Safety hazard",
        "Safety hazard",
        "Safety hazard",
        "Safety hazard",
        "Pressure issue",
        "Pressure issue",
        "Pressure issue",
        "Pressure issue",
        "Sensor failure",
        "Sensor failure",
        "Sensor failure",
        "Sensor failure",
        "Sensor failure",
        "Network issue",
        "Network issue",
        "Network issue",
        "Network issue",
        "Network issue"
    ]
})



data = json.loads(dataset_json)
df = pd.DataFrame(data)

print(f"Dataset created in memory using JSON with {len(df)} records.\n")



X_train, X_test, y_train, y_test = train_test_split(df["log"], df["label"], test_size=0.3, random_state=42)

 

model = make_pipeline(CountVectorizer(), MultinomialNB())
model.fit(X_train, y_train)

 

new_logs = [
    "Pump 1 stopped suddenly",
    "Leak detected near dispenser",
    "Fuel overflow in storage tank",
    "Display screen flickering",
    "Compressor overheated during refill",
    "Sensor not showing correct value"
]

sample_text = random.choice(new_logs)
predicted_label = model.predict([sample_text])[0]

 


machine_status = {
    1: random.choice(["Working normally", "Stopped suddenly", "Overheating"]),
    2: random.choice(["Working normally", "Pressure issue detected", "Overheating"]),
    3: random.choice(["Problem occurred", "Working normally", "Sensor issue"]),
    4: random.choice(["Electrical fault", "Working normally", "No response"]),
}

 


fuel_level = random.randint(500, 5000)   
fuel_capacity = 5000
fuel_percentage = (fuel_level / fuel_capacity) * 100




water_found = random.choice([True, False])

print(f"New log: {sample_text}")
print(f"Predicted category: {predicted_label}")
print(f"\nMachine Status:")
for machine, status in machine_status.items():
    print(f"Machine {machine}: {status}")

print(f"\nCurrent fuel level: {fuel_level} L ({fuel_percentage:.1f}% full)")
print(f"Water contamination detected: {'Yes' if water_found else 'No'}\n")

 
 
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_row = pd.DataFrame({
    "timestamp": [timestamp],
    "log": [sample_text],
    "category": [predicted_label],
    "fuel_level(L)": [fuel_level],
    "water_found": ["Yes" if water_found else "No"]
})
report_row.to_csv("report.csv", mode="a", header=False, index=False)
print("Report saved to CSV.")

 


pdf_filename = f"fuel_log_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
styles = getSampleStyleSheet()

story = []
story.append(Paragraph("Fuel Station AI Log Report", styles["Title"]))
story.append(Spacer(1, 20))
story.append(Paragraph(f"<b>Time:</b> {timestamp}", styles["Normal"]))
story.append(Paragraph(f"<b>Log:</b> {sample_text}", styles["Normal"]))
story.append(Paragraph(f"<b>Predicted Category:</b> {predicted_label}", styles["Normal"]))
story.append(Spacer(1, 10))
story.append(Paragraph("<b>Machine Status:</b>", styles["Heading3"]))
for machine, status in machine_status.items():
    story.append(Paragraph(f"Machine {machine}: {status}", styles["Normal"]))
story.append(Spacer(1, 10))
story.append(Paragraph(f"<b>Fuel Level:</b> {fuel_level} L ({fuel_percentage:.1f}% full)", styles["Normal"]))
story.append(Paragraph(f"<b>Water in Tank:</b> {'Yes' if water_found else 'No'}", styles["Normal"]))
story.append(Spacer(1, 20))
story.append(Paragraph("This report was auto-generated by the AI maintenance log analyzer.", styles["Italic"]))

doc.build(story)
print(f"PDF Report saved as: {pdf_filename}")

 

 
def send_gmail_notification(subject, body, attachment=None):
    sender_email = "tanbimustak@gmail.com"
    password = "wdwm sxou ippt qxgz"   
    receiver_email = "tanbimustak@gmail.com"

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment:
        with open(attachment, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=attachment)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)

subject = f"Fuel Station Alert: {predicted_label}"
body = (
    f"Log: {sample_text}\n"
    f"Category: {predicted_label}\n"
    f"Fuel Level: {fuel_level} L ({fuel_percentage:.1f}% full)\n"
    f"Water Found: {'Yes' if water_found else 'No'}\n"
    f"Time: {timestamp}"
)
send_gmail_notification(subject, body, pdf_filename)

print("Gmail notification sent successfully!")
