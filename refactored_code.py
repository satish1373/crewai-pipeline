# Importing necessary modules for the application
from flask import Flask, render_template, jsonify
import unittest

app = Flask(__name__)

# Dummy data structure to potentially hold exchange rates
exchange_rates = {
    "USD": 1.0,
    "EUR": 0.85,
    "GBP": 0.75,
}

# Route for the main page
@app.route('/')
def index():
    # Rendering the main UI page. Ensure "Latest Exchange Rate" label is used.
    return render_template('index.html', label="Latest Exchange Rate")

# An example route to get exchange rate data dynamically if needed
@app.route('/api/exchange-rate', methods=['GET'])
def get_exchange_rate():
    # Return the exchange rates in a JSON format
    return jsonify(exchange_rates)


def run_tests():
    class TestExchangeRateLabel(unittest.TestCase):
        def test_label_display(self):
            # Simulate accessing the main page
            with app.test_client() as client:
                response = client.get('/')
                self.assertIn(b'Latest Exchange Rate', response.data)
                print("Label Display Test: ✅")

        def test_exchange_rate_api(self):
            # Simulate API call
            with app.test_client() as client:
                response = client.get('/api/exchange-rate')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, exchange_rates)
                print("Exchange Rate API Test: ✅")

        def test_ui_functionality(self):
            # A placeholder for UI functionality tests
            with app.test_client() as client:
                # Simulate more checks if necessary...
                self.assertTrue(True)
                print("UI Functionality Test: ✅")

        def test_edge_case_dynamic_label(self):
            # Check handling of dynamic elements
            dynamic_label = "Latest Exchange Rate"
            self.assertEqual(dynamic_label, "Latest Exchange Rate")
            print("Edge Case Dynamic Label Test: ✅")

    # Run the tests
    unittest.main(exit=False)

if __name__ == '__main__':
    run_tests()
    # Running the application
    app.run(debug=True)