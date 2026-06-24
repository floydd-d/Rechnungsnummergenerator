# Rechnungsnummergenerator für Atchen

A playful web application for generating unique invoice numbers. The application generates 7-digit invoice numbers where the first 4 digits represent the current year and the last 3 digits follow a unique sequence calculated using bitwise operations (shift and XOR).

## Features

- 🎉 Funny, interactive web interface with animated graphics
- 📊 Generates unique 7-digit invoice numbers per year
- 🔢 Uses bitwise shift and XOR operations for code generation
- 🎨 Responsive design with modern UI
- 📈 Tracks number of generated invoices per year
- 💾 Persists generated invoice numbers to `invoice_history.log`
- 🔁 Restores the last generated number on startup and continues the series
- 🚀 Python 3.6+ compatible

## Requirements

- Python 3.6 or higher
- Flask 1.1.2
- Werkzeug 0.16.0

## Installation & Usage

### Quick Start (using the run script)

```bash
# Make the script executable
chmod +x run.sh

# Run on default port 5000
./run.sh

# Or specify a custom port
./run.sh 8080
```

If the app fails on first run because of dependency compatibility, rebuild the virtual environment with:

```bash
chmod +x fix_run_dependencies.sh
./fix_run_dependencies.sh
./run.sh 5000
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 app.py 5000
```

## API Endpoints

### GET /
Returns the main HTML interface

### POST /api/generate
Generates a new invoice number
- Returns JSON with the generated invoice number

### GET /api/stats
Returns statistics about generated invoices
- Returns JSON with year and count of generated invoices

## Persistence Behavior

- Generated invoice numbers are written to `invoice_history.log`.
- On startup, the app reads this file and reconstructs the last generated number.
- The series continues from the last saved invoice number to avoid duplicates across restarts.
- If the log file does not exist, the app starts a new series from `000`.

## How It Works

1. **Invoice Number Format**: `YYYYXXX`
   - YYYY: Current year (e.g., 2024)
   - XXX: Unique 3-digit code (000-999)

2. **Code Generation**: 
   - Uses bitwise shift (`<<`, `>>`) and XOR (`^`) operations
   - Ensures each code is unique within a year
   - Maximum 1000 codes per year (000-999)

3. **Uniqueness Guarantee**:
   - Maintains a set of generated codes per year
   - Detects and resolves collisions automatically
   - Resets counter when switching to a new year

## Number Generator Algorithm

The next 3-digit sequence code is derived from the previous code using the following formula:

```text
next_code = ((previous_code << 2) ^ (previous_code >> 1) ^ 0x2A) & 0x3FF
next_code = next_code % 1000
```

- `previous_code << 2` shifts the previous code left by 2 bits.
- `previous_code >> 1` shifts the previous code right by 1 bit.
- `^ 0x2A` applies a bitwise XOR with the hexadecimal constant `0x2A`.
- `& 0x3FF` keeps the result within 10 bits before reducing to the 3-digit range.
- If the computed code has already been used in the current year, a collision resolution step uses:

```text
next_code = (next_code ^ 0xAA) & 0x3FF
next_code = next_code % 1000
```

- If a collision still remains, the algorithm scans sequentially for the next unused code.

## UI Components

- **Headline**: "Rechnungsnummergenerator für Atchen" with emoji accents
- **Funny Numbers Image**: Animated SVG with playful number characters
- **Generate Button**: Click to generate a new invoice number
- **Result Display**: Shows the generated invoice number with timestamp
- **Statistics**: Displays count of generated invoices for the current year

## Technical Details

- **Framework**: Flask 1.1.2 (lightweight and compatible with Python 3.6)
- **Frontend**: HTML5, CSS3 with animations, vanilla JavaScript
- **Server**: WSGI-compatible (can run on port specified via command line argument)
- **Storage**: Persists generated invoice numbers to `invoice_history.log`
- **Startup recovery**: Reads the history log at launch to continue the series from the last generated code

## Customization

To customize the application:
- Edit `templates/index.html` for UI changes
- Edit `static/css/style.css` for styling
- Edit `static/js/script.js` for frontend behavior
- Edit `app.py` for backend logic and code generation algorithm
