# Blog Application

This is a Django-based blog application that allows users to create, edit, delete, and like blog posts. Users can also sign up, log in, log out, and update their profiles.

## Features

- User Authentication (Sign Up, Log In, Log Out)
- Create, Edit, Delete Blog Posts
- Like/Unlike Blog Posts
- View User Profiles
- Update User Profiles
- Change Password
- Update Email
- Delete Account

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Deployment on PythonAnywhere

To deploy this Django application on PythonAnywhere, follow these steps:

1. **Create an account on PythonAnywhere:**
   Go to [PythonAnywhere](https://www.pythonanywhere.com/) and sign up for an account.

2. **Create a new web app:**
   After logging in, go to the Dashboard, click on "Web" and then "Add a new web app". Follow the setup instructions and choose Django as your framework.

3. **Upload your code:**
   You can upload your project files using PythonAnywhere's built-in Bash console or via GitHub.

4. **Set up your virtual environment:**
   In the Bash console, create a virtual environment and install your project's dependencies:
   ```bash
   mkvirtualenv myenv --python=/usr/bin/python3.8
   workon myenv
   pip install -r requirements.txt
   ```

5. **Configure the WSGI file:**
   PythonAnywhere requires you to configure the WSGI file to point to your Django project. Update the WSGI configuration file to include your project settings.

6. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

8. **Reload your web app:**
   Go back to the "Web" tab and hit "Reload" to apply the changes.

9. **Visit your site:**
   You can now access your site using the link provided by PythonAnywhere.

## Running Tests

To run the tests for this Django application, execute the following command in your terminal:

```bash
python manage.py test
```

This command will execute all the tests in your project and display the results.
