# mock_piggybank.py
from flask import Flask, jsonify, request, send_file, redirect
from flask_cors import CORS
from zeroconf import ServiceInfo, Zeroconf
import socket
import threading
import json

app = Flask(__name__)
CORS(app)

"""
    "games": [
        {
            "gameType": "AddEmUp" | "CoinCombo",
            "difficulty": "VERY_EASY" | "EASY" | "MEDIUM" | "HARD",
            "gameWon": True | False,
            "timestamp": "" | "HH:MM:SS-DD/MM/YYYY"
        },
        ...
    ]
"""
mock_game_history = {
    "games": [
        {
            "gameType": "AddEmUp",
            "difficulty": "VERY_EASY",
            "gameWon": False,
            "timestamp": "14:24:22-01/01/2025"
        },
        {
            "gameType": "CoinCombo",
            "difficulty": "MEDIUM",
            "gameWon": True,
            "timestamp": "14:30:22-01/01/2025"
        },
        {
            "gameType": "AddEmUp",
            "difficulty": "HARD",
            "gameWon": True,
            "timestamp": "14:40:22-01/01/2025"
        },
        {
            "gameType": "CoinCombo",
            "difficulty": "HARD",
            "gameWon": False,
            "timestamp": "14:50:22-01/01/2025"
        },
        {
            "gameType": "AddEmUp",
            "difficulty": "HARD",
            "gameWon": True,
            "timestamp": "15:00:22-01/01/2025"
        }, #do another day
        {
            "gameType": "AddEmUp",
            "difficulty": "VERY_EASY",
            "gameWon": False,
            "timestamp": "14:24:22-02/01/2025"
        },
        {
            "gameType": "CoinCombo",
            "difficulty": "MEDIUM",
            "gameWon": True,
            "timestamp": "14:30:22-02/01/2025"
        },
        {
            "gameType": "AddEmUp",
            "difficulty": "HARD",
            "gameWon": True,
            "timestamp": "14:40:22-02/01/2025"
        },
        {
            "gameType": "CoinCombo",
            "difficulty": "HARD",
            "gameWon": False,
            "timestamp": "14:50:22-01/02/2025"
        },
        {
            "gameType": "AddEmUp",
            "difficulty": "HARD",
            "gameWon": True,
            "timestamp": "15:00:22-01/02/2025"
        }


    ]
}
#add pin and lock
pin = 1301
unlocked = True

@app.route('/')
def serve_index():
    return send_file('index.html')

@app.route('/api/bankvalues', methods=['GET'])
def get_bank_values():
    #in the form of {coin_value: number_of_coins}
    # so {"1": 50, "2": 50, "5": 50, "10": 50, "20": 50, "50": 50, "100": 50, "200": 50}
    # means we have 50 1p coins, 50 2p coins, etc.
    with open('mock_bank.json') as f:
        mock_bank = json.load(f)
    return jsonify(mock_bank)

@app.route('/favicon.ico',methods=['GET'])
def serve_favicon():
    return send_file('favicon.ico')

@app.route('/api/gamehistory', methods=['GET'])
def get_game_history():
    print(f"sending game history {jsonify(mock_game_history)}")
    return jsonify(mock_game_history)


def find_combination(target, coins):
    n = len(coins)
    INF = 10**9
    dp = [[INF for _ in range(target+1)] for _ in range(n+1)]
    choice = [[0 for _ in range(target+1)] for _ in range(n+1)]
    dp[0][0] = 0
    for i in range(1, n+1):
        for j in range(0, target+1):
            dp[i][j] = dp[i-1][j]
            choice[i][j] = 0
            for k in range(1, coins[i-1][1]+1):
                coin_value_sum = k * coins[i-1][0]
                if j >= coin_value_sum and dp[i-1][j-coin_value_sum] != INF:
                    candidate = dp[i-1][j-coin_value_sum] + k
                    if candidate < dp[i][j]:
                        dp[i][j] = candidate
                        choice[i][j] = k
    if dp[n][target] == INF:
        return []
    result = [0 for _ in range(n)]
    remaining = target
    for i in range(n, 0, -1):
        used = choice[i][remaining]
        result[i-1] = [coins[i-1][0], used]
        remaining -= used * coins[i-1][0]
    return result

@app.route('/api/exactdispense', methods=['POST'])
def dispense_exact():
    if not unlocked:
        return "bank is locked", 401

    amount = request.data.decode()
    #first we should check that they sent a valid request
    if not amount.isdigit():
        return "Invalid request", 400
    # check that the bank has enough money for it
    with open('mock_bank.json') as f:
        mock_bank = json.load(f)
    
    ## use the find_combination function to get the coins
    coins = find_combination(int(amount), [[int(k), v] for k, v in mock_bank.items()])
    if not coins:
        return f"can't make {amount} with the coins in the bank", 400
    # now we need to update the bank
    for coin in coins:
        mock_bank[str(coin[0])] -= coin[1]
    with open('mock_bank.json', 'w') as f:
        json.dump(mock_bank, f)
    return "dispensed coins", 200

@app.route('/api/emptybank', methods=['DELETE'])
def empty_bank():
    #mock_bank.update({k:0 for k in mock_bank})
    if not unlocked:
        return "bank is locked", 401
    
    with open('mock_bank.json') as f:
        mock_bank = json.load(f)
    for k in mock_bank:
        mock_bank[k] = 0
    
    with open('mock_bank.json', 'w') as f:
        json.dump(mock_bank, f)
    return "emptied bank", 200

@app.route('/api/factoryreset', methods=['DELETE'])
def factory_reset():
    if not unlocked:
        return "bank is locked", 401
    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ', code=302)

@app.route('/api/lockbank', methods=['POST'])
#check the pin and lock the bank if correct. the pin should be in the request body as a string
def lock_bank():
    global unlocked
    if request.data.decode() == str(pin):
        unlocked = False
        return "locked bank", 200
    return "incorrect pin", 401

@app.route('/api/unlockbank', methods=['POST'])
#check the pin and unlock the bank if correct. the pin should be in the request body
def unlock_bank():
    global unlocked
    if request.data.decode() == str(pin):
        unlocked = True
        return "unlocked bank", 200
    return "incorrect pin", 401

@app.route('/api/changepin', methods=['POST'])
#     //json in the form of {"oldpin":"oldpin","newpin":"newpin"}
def change_pin():
    global pin
    data = request.get_json()
    if data.get("oldpin") == str(pin):
        pin = str(data["newpin"])
        return "changed pin", 200
    return "incorrect pin", 401

@app.route('/api/lockstatus', methods=['GET'])
def get_lock_status():
    return jsonify({"locked": not unlocked}), 200

def advertise_service():
    hostname = "piggybank.local"
    ip = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
    
    service_info = ServiceInfo(
        "_http._tcp.local.",
        "PiggyBank Service._http._tcp.local.",
        addresses=[ip],
        port=80,
        properties={},
        server=hostname,
    )
    
    zeroconf = Zeroconf()
    zeroconf.register_service(service_info)



if __name__ == '__main__':
    advertise_service()
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=80)).start()