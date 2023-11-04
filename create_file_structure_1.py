import os

project_name = "content-creator-website"

# Define the expected directory structure and files
structure = {
    'public': {
        'assets/images': [],
        'assets/videos': [],
        'assets/styles': [],
        'assets/scripts': []
    },
    'views': {
        'partials': []
    },
    'routes': [],
    'models': [],
    'controllers': [],
    'middleware': [],
    'config': [],
    'utils': []
}

populate_me_content = {
    'public/assets/images': "Place image assets here, such as logos, banners, and other graphics.",
    'public/assets/videos': "Place video assets here, such as trailers, gameplay videos, etc.",
    'public/assets/styles': "Place CSS stylesheets here.",
    'public/assets/scripts': "Place client-side JavaScript files here.",
    'views/partials': "Place reusable EJS components here, such as headers, footers, etc.",
    'routes': "Define route handlers here. For example, you might have 'userRoutes.js' for user-related routes.",
    'models': "Define data models here. For example, 'userModel.js' for user data structure and database interactions.",
    'controllers': "Place the business logic for your routes here. For example, 'userController.js' for user-related logic.",
    'middleware': "Place middleware functions here, such as authentication checks, logging, etc.",
    'config': "Place configuration files here, such as database connection settings.",
    'utils': "Place utility functions here, such as SEO helpers, data processing functions, etc."
}

# Iterate through the structure and create missing directories/files
for main_dir, sub_dirs in structure.items():
    main_path = os.path.join(project_name, main_dir)
    if not os.path.exists(main_path):
        os.makedirs(main_path)
    
    if isinstance(sub_dirs, list):
        # If any main directory is expected to have specific files, handle here
        if not sub_dirs:
            populate_me_path = os.path.join(main_path, "POPULATE_ME.txt")
            with open(populate_me_path, 'w') as f:
                f.write(populate_me_content.get(main_path, "Populate this directory with appropriate content."))
    else:
        for sub_dir, sub_sub_dirs in sub_dirs.items():
            sub_path = os.path.join(project_name, main_dir, sub_dir)
            if not os.path.exists(sub_path):
                os.makedirs(sub_path)
            
            # Create POPULATE_ME.txt for subdirectories
            if not sub_sub_dirs:
                populate_me_path = os.path.join(sub_path, "POPULATE_ME.txt")
                with open(populate_me_path, 'w') as f:
                    f.write(populate_me_content.get(sub_path, "Populate this directory with appropriate content."))

print("Directory structure has been verified and missing elements have been created.")
