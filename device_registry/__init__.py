import markdown
import os

# import the framework
from flask import Flask

# create an instance of flask
app = Flask(__name__)

@app.route("/")
def hello():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to html
        return markdown.markdown(content)



