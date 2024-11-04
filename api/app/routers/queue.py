from fastapi import APIRouter
from app.models.queue_operations import QueueItem, get_queue, add_to_queue, start_service, update_service, delete_from_queue, get_stats, reset_visits_count

router = APIRouter()


@router.get("/queue")
async def get_queue_endpoint():
    return get_queue()

@router.post("/queue/add")
async def add_to_queue_endpoint(item: QueueItem):
    return add_to_queue(item)

@router.post("/start_service")
async def start_service_endpoint(item: QueueItem):
    return start_service(item)

@router.post("/update_service")
async def update_service_endpoint(item: QueueItem):
    return update_service(item)

@router.delete("/queue/{name}")
async def delete_from_queue_endpoint(name: str):
    return delete_from_queue(name)

@router.get("/stats")
async def get_stats_endpoint():
    return get_stats()

@router.post("/reset_visits_count")
async def reset_visits_count_endpoint():
    return reset_visits_count()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@router.post("/send-email")
def send_email_alert(service):
    sender_email = "autolinkserviceco@gmail.com"
    password = "nuvk tpun zcek vnfa"
    receiver_email = "manuelmoralesdiaz0@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Service Status Update Notification"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"""
    Hi {service['name']},

    The status of your service for {service['model']} with license plate {service['license_plate']} has been updated.

    Service Details:
    Service Type: {service['service']}
    New Status: {service['status']}

    Thank you for choosing our services.

    Best Regards,
    AutoLink Service Team
    """

    part = MIMEText(text, "plain")
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
