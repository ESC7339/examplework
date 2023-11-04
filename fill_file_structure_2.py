import os
import subprocess

import shutil

def check_dependency_installed(dependency_name):
    return shutil.which(dependency_name) is not None


# Check if Node.js and npm are installed
if not check_dependency_installed("node") or not check_dependency_installed("npm"):
    print("Node.js and npm are required. Please install them before running this script.")
    exit()

# Define the directory structure
structure = {
    'public': ['assets/images', 'assets/videos', 'assets/styles', 'assets/scripts'],
    'views': ['partials'],
    'routes': [],
    'models': [],
    'controllers': [],
    'middleware': [],
    'config': [],
    'utils': []
}

# Create the directory structure
project_name = "content-creator-website"
os.makedirs(project_name, exist_ok=True)

for main_dir, sub_dirs in structure.items():
    os.makedirs(f"{project_name}/{main_dir}", exist_ok=True)
    for sub_dir in sub_dirs:
        os.makedirs(f"{project_name}/{main_dir}/{sub_dir}", exist_ok=True)

# Initialize a new Node.js project
subprocess.run(["npm.cmd", "init", "-y"], cwd=project_name)


# Install packages
packages = ["express", "ejs", "mongoose", "passport", "dotenv", "morgan", "body-parser"]
dev_packages = ["nodemon"]
subprocess.run(["npm.cmd", "install", *packages], cwd=project_name)
subprocess.run(["npm.cmd", "install", "--save-dev", *dev_packages], cwd=project_name)

# Create and populate basic files
files_content = {
    ".gitignore": "node_modules/\n.env\n",
    "server.js": """const express = require('express');
const bodyParser = require('body-parser');
const morgan = require('morgan');
require('dotenv').config();

const app = express();

app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(morgan('dev'));

app.get('/', (req, res) => {
    res.render('index');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
""",
    "views/index.ejs": "<h1>Welcome to the Content Creator Website</h1>",
    "routes/index.js": """const express = require('express');
const router = express.Router();

// Define your routes here

module.exports = router;
""",
    "controllers/portfolioController.js": """// Portfolio controller logic here
""",
    "models/user.js": """// User model definition here
""",
    "config/database.js": """// Database configuration here
""",
    "utils/seoHelper.js": """// SEO helper functions here
""",
    ".env": "PORT=3000\nDB_URI=your_mongodb_uri_here\n"
}

for file_path, content in files_content.items():
    with open(f"{project_name}/{file_path}", 'w') as f:
        f.write(content)

# Update package.json with nodemon script
package_json_path = f"{project_name}/package.json"
with open(package_json_path, 'r') as f:
    package_data = f.read().replace('"test": "echo \\"Error: no test specified\\" && exit 1"',
                                    '"start": "nodemon server.js"')

with open(package_json_path, 'w') as f:
    f.write(package_data)

print("Project foundation has been set up!")
