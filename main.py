import requests

def send_post_request(url, token, data):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print('Запрос успешно отправлен!')
    else:
        print(f'Произошла ошибка: {response.status_code}')
        print(response.text)

def main():
    url = "https://api.hamsterkombatgame.io/clicker/tap"
    
    token = input("Введите ваш Bearer token: ")
    count = int(input("Введите count: "))
    available_taps = int(input("Введите availableTaps: "))
    timestamp = int(input("Введите timestamp: "))
    
    data = {
        "count": count,
        "availableTaps": available_taps,
        "timestamp": timestamp
    }
    
    send_post_request(url, token, data)

if __name__ == "__main__":
    main()