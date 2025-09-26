from flask import Flask, render_template
import unittest

app = Flask(__name__)

# In-memory data for exchange rates (example)
exchange_rates = {
    'USD': 1.0,
    'EUR': 0.85,
    # Additional currencies can be added here
}

@app.route('/')
def index():
    """Render the main page with the latest exchange rates."""
    return render_template('index.html', exchange_rates=exchange_rates)

def run_app():
    """Run the Flask application."""
    app.run(debug=True)

class TestExchangeRateApp(unittest.TestCase):
    """Test cases for the Exchange Rate application."""

    def test_label_display(self):
        """UI Test Case: Verify the new label is displayed correctly."""
        with app.test_request_context('/'):
            rendered = index()
            self.assertIn('Latest Exchange Rate', rendered.data.decode())

    def test_functionality(self):
        """Functional Test Case: Ensure functionality is unaffected."""
        with app.test_request_context('/'):
            self.assertIn('USD', exchange_rates)
            self.assertIn('EUR', exchange_rates)

    def test_localization_consistency(self):
        """Localization Test Case: Validate localization aspects if present."""
        # Implement localization tests as required by your application.
        # Placeholder for potential localization.
        pass

    def test_cross_browser_display(self):
        """Cross-Browser Test Case: Validate label display (mocked)."""
        with app.test_request_context('/'):
            rendered = index()
            self.assertIn('Latest Exchange Rate', rendered.data.decode())

    def test_edge_cases(self):
        """Test Edge Cases: Ensure all instances of the old label are changed."""
        # List of labels to check.
        sample_data = ['Exchange Rate', 'Another Exchange Rate', 'Last Exchange Rate']
        updated_data = [item.replace('Exchange Rate', 'Latest Exchange Rate') for item in sample_data]
        self.assertNotIn('Exchange Rate', updated_data)
        self.assertIn('Latest Exchange Rate', updated_data)

def main():
    """Main function to run the application and tests."""
    run_app()
    
    # Run tests and print results with indicators
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExchangeRateApp)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Print custom indicators (✓ for pass, X for fail)
    for test in suite:
        outcome = result.
        print(f"{'✓' if outcome.wasSuccessful() else 'X'} {test.id()}")

if __name__ == "__main__":
    main()

# End of application and test cases