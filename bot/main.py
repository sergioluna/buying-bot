import os
import time
from sentinels import N64SwitchControllerSentinel
from twilio.rest import Client

def run():
    # URL for N64 Switch Controller
    url = 'https://store.nintendo.com/nintendo-64-controller.html'

    # Initialize sentinel
    print("Initializing sentinel")
    sentinel = N64SwitchControllerSentinel(url)
    sentinel.load_html()
    sentinel.update_status()
    localtime = time.asctime(time.localtime(time.time()))
    print(f'N64SwitchController status: {sentinel.status} ({localtime})')

    # Initialize Twilio messenger
    print("Initializing messenger client")
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    numbers_to_message = os.environ['TWILIO_TO_NUMBERS'].split()
    twilio_client = Client(account_sid, auth_token)

    # Send initial message
    print("Sending initial message")
    msg_body = f'N64SwitchController current status: \'{sentinel.status}\' ({localtime})'
    msg_body += '\n\nYou will receive another text when the availability status changes.'
    msg_body += '\n\nSincerely,\nN64SwitchControllerSentinel'
    for number in numbers_to_message:
        message = twilio_client.messages \
                                .create(
                                    body=msg_body,
                                    from_=os.environ['TWILIO_FROM_NUMBER'],
                                    to=number
                                )
        print("Message sent:")
        print(message.sid)

    # Loop until status changes
    print("Starting loop")
    initial_status = sentinel.status
    while sentinel.status == initial_status:
        time.sleep(60)
        sentinel.clear_html()
        sentinel.load_html()
        sentinel.update_status()
        localtime = time.asctime(time.localtime(time.time()))
        print(f'N64SwitchController status: \'{sentinel.status}\' ({localtime})')

    # Status has changed
    print(f'N64 Switch Controller went from \'{initial_status}\' to \'{sentinel.status}\' within the last minute!')

    # Send notification message
    print("Sending notification")
    msg_body = f'N64 Switch Controller went from \'{initial_status}\' to \'{sentinel.status}\' within the last minute!'
    msg_body += f'\n\nOrder yours now at {url}'
    msg_body += '\n\nSincerely,\nN64SwitchControllerSentinel'
    msg_body += '\n\nGodspeed'
    for number in numbers_to_message:
        message = twilio_client.messages \
                                .create(
                                    body=msg_body,
                                    from_=os.environ('TWILIO_FROM_NUMBER'),
                                    to=number
                                )
        print("Message sent:")
        print(message.sid)

    print("Goodbye.")



if __name__ == '__main__':
    run()