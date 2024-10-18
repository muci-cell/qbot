import requests

requests.post('http://localhost:3000/send_forward_msg', json={
    'user_id': 2567460580,
    'message': [{
        'type': 'text',
        'data': {
            'text': 'Hello, World2!'
        }
    }]
})