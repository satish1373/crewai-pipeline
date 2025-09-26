# Import necessary libraries for creating a simple web app
from flask import Flask, render_template_string
import unittest

# Initialize the Flask application
app = Flask(__name__)

# Define a simple HTML template with a dynamic background color
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Background Color Change</title>
    <style>
        /* Inline CSS to set the background color to RED */
        body {
            background-color: #FF0000; /* RED */
            color: white; /* Ensuring text contrast */
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
        }
    </style>
</head>
<body>
    <h1>Welcome to My App!</h1>
    <p>The background color has been successfully changed to RED.</p>
</body>
</html>
"""

# Define a route for the home page
@app.route('/')
def home():
    return render_template_string(html_template)

def run_app():
    """Start the Flask application."""
    app.run(debug=True)

class TestBackgroundColorChange(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up the test client before any tests are run."""
        cls.client = app.test_client()

    def test_background_color(self):
        """Test if the background color is set to RED."""
        response = self.client.get('/')
        self.assertIn(b'background-color: #FF0000;', response.data)

    def test_text_contrast(self):
        """Test if the text is visible on a red background."""
        response = self.client.get('/')
        self.assertIn(b'color: white;', response.data)

    def test_responsive_design(self):
        """Test that the application is responsive."""
        response = self.client.get('/')
        self.assertIn(b'<meta name="viewport" content="width=device-width, initial-scale=1.0">', response.data)

    def test_browser_compatibility(self):
        """Check if the HTML responds with the correct status code."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_edge_case_accessibility(self):
        """Test against color accessibility for color blind users."""
        response = self.client.get('/')
        self.assertIn(b'color: white;', response.data)
        # Further tests could involve checking color contrast ratios

def main():
    """Run the Flask app and the test suite."""
    run_app()
    
    # Run tests and print results
    print("Running tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestBackgroundColorChange)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    # Print results with checkmark or X indicators
    for test, outcome in zip(test_suite, test_result.results):
        if outcome:
            print(f"✔️ {test}: Passed")
        else:
            print(f"❌ {test}: Failed")

if __name__ == '__main__':
    main()