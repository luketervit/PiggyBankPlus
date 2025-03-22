# PiggyBank Plus

A virtual piggy bank and educational application to help children learn about money through interactive games and coin management.

![PiggyBank Plus](https://via.placeholder.com/800x400?text=PiggyBank+Plus)

## Overview

PiggyBank Plus is an interactive web application designed to teach children about money management and coin recognition. The application simulates a digital piggy bank where users can:

- Track coin collection and total savings
- Dispense coins in specific amounts
- Lock/unlock the bank with a PIN
- Play educational money games with various difficulty levels
- View learning progress through charts and statistics

## Features

### Bank Management
- Real-time tracking of coins and total value
- Dispense specific amounts of coins
- Empty bank functionality
- PIN protection with lock/unlock features

### Educational Games
- **AddEmUp**: Practice adding up coins to reach target amounts
- **CoinCombo**: Learn to make different combinations of coins that equal the same value
- Multiple difficulty levels from Very Easy to Hard
- Progress tracking and statistics

### Security
- PIN protection for important operations
- PIN change functionality
- Lock status indicator

## Technical Information

### Dependencies
- Flask (Python web framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- zeroconf (Zero-configuration networking)
- Chart.js (JavaScript charting library)

### File Structure
- `index.html` - Main frontend interface
- `mock_piggybank.py` - Flask server with mock backend functionality
- `mock_bank.json` - Storage for coin amounts
- `favicon.ico` - Website icon

## Getting Started

### Prerequisites
- Python 3.6+
- pip (Python package manager)

### Installation

1. Clone the repository or download the files
```bash
git clone https://github.com/yourusername/piggybank-plus.git
cd piggybank-plus
```

2. Install the required Python packages
```bash
pip install flask flask-cors zeroconf
```

3. Make sure you have all the necessary files in your directory:
   - `mock_piggybank.py`
   - `index.html`
   - `favicon.ico`
   - `mock_bank.json` (create if it doesn't exist)

4. If `mock_bank.json` doesn't exist, create it with the following content:
```json
{
  "1": 50,
  "2": 50,
  "5": 50,
  "10": 50,
  "20": 50,
  "50": 50,
  "100": 50,
  "200": 50
}
```

### Running the Application

1. Start the Flask server
```bash
python mock_piggybank.py
```

2. Access the application in a web browser
   - `http://localhost:80`
   - `http://127.0.0.1:80`
   - `http://piggybank.local` (requires local DNS configuration)

Note: If you encounter permission issues with port 80, you can modify the code to use port 5000 instead, and then access the application at:
   - `http://localhost:5000`
   - `http://127.0.0.1:5000`
   - `http://piggybank.local:5000`

## Usage

### Bank Operations
- View your current coin collection and total savings
- Enter an amount and click "Dispense" to take coins out
- Use the "Empty Bank" button to remove all coins
- Lock/unlock the bank using the PIN (default: 1301)

### Playing Games
- Switch between games using the tabs
- Select difficulty levels to match learning progress
- View statistics for each game and difficulty level

### PIN Management
- Default PIN: 1301
- Use the "Change PIN" section to update your PIN
- Always keep your PIN secure

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Designed for educational purposes
- UK currency coin system
- Interactive learning approach to money management

---

*Note: PiggyBank Plus is a simulation and educational tool, not a real financial management system.* 