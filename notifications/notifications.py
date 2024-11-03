from firebase_admin import messaging

def send_push_notification(fcm_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=fcm_token
    )
    
    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)
