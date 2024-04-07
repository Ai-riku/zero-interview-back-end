# Zero Interview Back End

Welcome to the backend repository of the **Zero Interview AI Application**. This application serves as the backbone for an AI-powered interview platform, designed to streamline and enhance the interview preparation process.

To experience the full capabilities of the Zero Interview AI Application, please also run the front-end component available at: [Zero FrontEnd](https://github.com/kay30kim/zero-interview-front-end).

## For Developers

### Setting Up Your Development Environment

1. **Creating a Virtual Environment**

   We recommend using a virtual environment (venv) for Python projects to manage dependencies effectively. To create a virtual environment, execute the following command in your terminal:

   ```bash
   python -m venv venv
   ```

2. **Activating the Virtual Environment**

   After creating the virtual environment, you need to activate it:

   - On Unix/macOS:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```cmd
     .\venv\Scripts\activate
     ```

### Installing Dependencies

To install the necessary dependencies for the project, run the following commands:

You need to install HomeBrew, since PyAudio and FFmpeg need additional dependencies.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install portaudio
brew install ffmpeg
```

Now you can run the following

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Running the Application

To start the backend server, execute:

```bash
cd flaskapp
flask run
```

This command will launch the Flask server, enabling the backend component of the Zero Interview AI Application.

