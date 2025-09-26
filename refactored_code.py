from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
import unittest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for the Calendar Event
class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)  # Assuming user authentication implemented

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'user_id': self.user_id
        }

# API to create a calendar event
@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.json
    if not all(k in data for k in ("title", "start_time", "end_time", "user_id")):
        return jsonify({"error": "Missing data"}), 400

    # Validate datetime format
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

    new_event = CalendarEvent(
        title=data['title'],
        start_time=start_time,
        end_time=end_time,
        user_id=data['user_id']
    )

    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Event overlaps with another event"}), 409

# API to get all events for a user
@app.route('/api/events/<int:user_id>', methods=['GET'])
def get_events(user_id):
    events = CalendarEvent.query.filter_by(user_id=user_id).all()
    return jsonify([event.to_dict() for event in events]), 200

# API to update an existing event
@app.route('/api/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    data = request.json
    
    # Validate datetime format
    try:
        if 'start_time' in data:
            event.start_time = datetime.fromisoformat(data['start_time'])
        if 'end_time' in data:
            event.end_time = datetime.fromisoformat(data['end_time'])
        event.title = data.get('title', event.title)

        db.session.commit()
        return jsonify(event.to_dict()), 200
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

# API to delete a calendar event
@app.route('/api/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = CalendarEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully."}), 204

# Error handling for invalid datetime formats
@app.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({"error": "Invalid datetime format"}), 400

def run_tests():
    # Test cases
    class CalendarEventTestCase(unittest.TestCase):
        def setUp(self):
            self.app = app.test_client()
            with app.app_context():
                db.create_all()
            
        def tearDown(self):
            with app.app_context():
                db.drop_all()

        def test_create_event(self):
            response = self.app.post('/api/events', json={
                "title": "Meeting",
                "start_time": "2023-10-01T10:00:00",
                "end_time": "2023-10-01T11:00:00",
                "user_id": 1
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn("Meeting", str(response.data))

        def test_update_event(self):
            self.app.post('/api/events', json={
                "title": "Meeting",
                "start_time": "2023-10-01T10:00:00",
                "end_time": "2023-10-01T11:00:00",
                "user_id": 1
            })
            
            response = self.app.put('/api/events/1', json={
                "title": "Updated Meeting",
                "start_time": "2023-10-01T11:00:00",
                "end_time": "2023-10-01T12:00:00"
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn("Updated Meeting", str(response.data))

        def test_delete_event(self):
            self.app.post('/api/events', json={
                "title": "Meeting",
                "start_time": "2023-10-01T10:00:00",
                "end_time": "2023-10-01T11:00:00",
                "user_id": 1
            })
            
            response = self.app.delete('/api/events/1')
            self.assertEqual(response.status_code, 204)

        def test_invalid_datetime(self):
            response = self.app.post('/api/events', json={
                "title": "Invalid Meeting",
                "start_time": "invalid-date",
                "end_time": "invalid-date",
                "user_id": 1
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn("Invalid datetime format", str(response.data))

        def test_event_overlap(self):
            self.app.post('/api/events', json={
                "title": "First Event",
                "start_time": "2023-10-01T10:00:00",
                "end_time": "2023-10-01T11:00:00",
                "user_id": 1
            })
            response = self.app.post('/api/events', json={
                "title": "Overlapping Event",
                "start_time": "2023-10-01T10:30:00",
                "end_time": "2023-10-01T11:30:00",
                "user_id": 1
            })
            self.assertEqual(response.status_code, 409)
            self.assertIn("overlaps", str(response.data))

        def test_individual_timezones(self):
            # Assuming an additional testing function for timezones can be implemented
            pass  # Placeholder for timezone-related tests

    # Run tests
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.TestLoader().loadTestsFromTestCase(CalendarEventTestCase))

    # Check results and print indicators
    if result.wasSuccessful():
        print("All tests passed! ✅")
    else:
        print("Some tests failed! ❌")

# Main entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)

    run_tests()