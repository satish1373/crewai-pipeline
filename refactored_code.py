from flask import Flask, render_template_string
import webbrowser
import threading

app = Flask(__name__)

# Define a basic HTML template with a red background
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Red Background App</title>
    <style>
        body {{
            background-color: red; /* Set the background color to red */
            color: white; /* Change text color to ensure readability */
            font-family: Arial, sans-serif; /* Set a basic font for readability */
            text-align: center; /* Center the text in the body */
            padding: 50px; /* Add some padding around the content */
        }}
    </style>
</head>
<body>
    <h1>Welcome to the Red Background App!</h1>
    <p>The background color has been successfully changed to red.</p>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

def run_flask_app():
    app.run(debug=False, use_reloader=False)

def test_accessibility():
    # This can be a comprehensive test for color contrast with WCAG guidelines
    # Mock testing that explores contrast and accessibility
    expected_contrast_ratio = 4.5  # Example contrast ratio for normal text
    background_color = (255, 0, 0)  # Red
    text_color = (255, 255, 255)  # White
    contrast_ratio = calculate_contrast(background_color, text_color)
    
    assert contrast_ratio >= expected_contrast_ratio, "Accessibility test failed"
    print(f"Accessibility test: {'✅' if contrast_ratio >= expected_contrast_ratio else '❌'}")  

def calculate_contrast(rgb1, rgb2):
    # Calculate the contrast ratio between two RGB colors
    def luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = (r / 12.92) if (r <= 0.03928) else ((r + 0.055) / 1.055) ** 2.4
        g = (g / 12.92) if (g <= 0.03928) else ((g + 0.055) / 1.055) ** 2.4
        b = (b / 12.92) if (b <= 0.03928) else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    L1 = luminance(rgb1)
    L2 = luminance(rgb2)
    
    return (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)

def run_tests():
    print("Running tests...")

    try:
        test_accessibility()  # Check for accessibility compliance
        print("All tests passed ✅")
    except AssertionError as error:
        print(str(error))
        print("Some tests failed ❌")

if __name__ == '__main__':
    # Start Flask app in a separate thread
    threading.Thread(target=run_flask_app).start()
    webbrowser.open("http://127.0.0.1:5000/")  # Open browser automatically
    run_tests()