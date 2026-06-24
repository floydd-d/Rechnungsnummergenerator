#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rechnungsnummergenerator für Atchen
Web application for generating unique invoice numbers
"""

from flask import Flask, render_template, jsonify
from datetime import datetime
import sys
import os

app = Flask(__name__)

# Store generated codes per year to ensure uniqueness
generated_codes = {}
last_generated_code = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'invoice_history.log')


def _normalize_code(code):
    return code % 1000


def _calculate_next_code(previous_code):
    # Use bitwise shift and XOR operations to continue the series
    next_code = ((previous_code << 2) ^ (previous_code >> 1) ^ 0x2A) & 0x3FF
    return _normalize_code(next_code)


def _resolve_collision(code):
    collision_code = (code ^ 0xAA) & 0x3FF
    return _normalize_code(collision_code)


def load_history():
    global last_generated_code
    if not os.path.exists(LOG_FILE):
        return
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as history_file:
            for line in history_file:
                line = line.strip()
                if not line or not line.isdigit() or len(line) < 7:
                    continue
                year = line[:4]
                try:
                    code = int(line[4:])
                except ValueError:
                    continue

                if year not in generated_codes:
                    generated_codes[year] = {
                        'codes': set(),
                        'last_code': None
                    }

                year_data = generated_codes[year]
                year_data['codes'].add(code)
                year_data['last_code'] = code
                last_generated_code = code
    except OSError:
        pass


def append_invoice_to_log(invoice_number):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as history_file:
            history_file.write(f"{invoice_number}\n")
    except OSError:
        # Logging should not break the app runtime
        pass


def get_next_code(year):
    """
    Generate the next unique 3-digit code for the given year.
    Uses bitwise shift and XOR operations.

    Args:
        year: The year to generate code for

    Returns:
        A 3-digit string (000-999) that is unique for the year
    """
    year_str = str(year)
    if year_str not in generated_codes:
        generated_codes[year_str] = {
            'codes': set(),
            'last_code': None
        }

    year_data = generated_codes[year_str]
    if year_data['last_code'] is None:
        if last_generated_code is not None:
            candidate = _calculate_next_code(last_generated_code)
        else:
            candidate = 0
    else:
        candidate = _calculate_next_code(year_data['last_code'])

    attempts = 0
    while candidate in year_data['codes'] and attempts < 1000:
        candidate = _resolve_collision(candidate)
        attempts += 1

    if candidate in year_data['codes']:
        for candidate in range(1000):
            if candidate not in year_data['codes']:
                break

    year_data['codes'].add(candidate)
    year_data['last_code'] = candidate
    return f"{candidate:03d}"


load_history()


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate a new invoice number"""
    current_year = datetime.now().year
    code = get_next_code(current_year)
    invoice_number = f"{current_year}{code}"
    
    append_invoice_to_log(invoice_number)
    print(f"Generated invoice number: {invoice_number}")
    
    return jsonify({
        'success': True,
        'invoice_number': invoice_number,
        'year': current_year,
        'code': code
    })


@app.route('/api/stats', methods=['GET'])
def stats():
    """Get statistics about generated codes"""
    current_year = str(datetime.now().year)
    
    if current_year in generated_codes:
        count = len(generated_codes[current_year]['codes'])
    else:
        count = 0
    
    history_loaded = os.path.exists(LOG_FILE)
    
    return jsonify({
        'year': current_year,
        'codes_generated': count,
        'history_file_exists': history_loaded,
        'history_file': LOG_FILE if history_loaded else None
    })


if __name__ == '__main__':
    # Get port from command line argument
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Using default port 5000")
    
    print(f"Starting Rechnungsnummergenerator on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
