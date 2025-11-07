from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import database
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Enable CORS for all routes

# Initialize database on startup
database.init_db()

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'Server is active on your phone!',
        'total_submissions': database.get_submission_count()
    })

@app.route('/api/submit', methods=['POST'])
def submit_form():
    """Handle form submission"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'age']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'{field} is required'
                }), 400
        
        # Validate age
        try:
            age = int(data['age'])
            if age < 0 or age > 150:
                return jsonify({
                    'success': False,
                    'error': 'Please enter a valid age'
                }), 400
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Age must be a number'
            }), 400
        
        # Save to database
        submission_id = database.save_submission(data)
        
        return jsonify({
            'success': True,
            'message': 'Form submitted successfully!',
            'submission_id': submission_id
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    """Get all submissions"""
    try:
        submissions = database.get_all_submissions()
        return jsonify({
            'success': True,
            'count': len(submissions),
            'data': submissions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting server on your phone...")
    print("📱 Server will be accessible via ngrok URL")
    app.run(host='0.0.0.0', port=8000, debug=True)
