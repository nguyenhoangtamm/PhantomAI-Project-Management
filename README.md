# PhantomAI Project Management

## Project Structure

Below is an overview of the project structure and the purpose of each key file or directory:

-   **`.venv`**: A virtual environment for Python dependencies, ensuring isolated package management.
-   **`src`**: The main directory containing the project's source code.
-   **`__pycache__`**: Python's bytecode cache directory, automatically generated.
-   **`.env`**: A file for storing environment variables, typically used for sensitive information or configuration.
-   **`.gitignore`**: Specifies files and directories that Git should ignore.
-   **`README.md`**: This file (you are reading it now) provides an overview of the project.
-   **`requirements.txt`**: Lists the Python dependencies required for the project.

## Getting Started

1. **Set up the virtual environment**:
    ```bash
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    ```
2. **Install dependencies**:

    ````bash
        pip install -r requirements.txt
        ```

    ````

3. **Update the configuration**:
   Navigate to the `src` directory
   Modify the `config.py` file to include the following `Config` class for database configuration:

    ```python
    class Config:
        SQLALCHEMY_DATABASE_URI = "postgresql://<username>:<password>@localhost:5432/PhantomAI"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    ```


4. **Run the application**:  
   Navigate to the `src` directory and execute the `app.py` script:
    ````bash
    cd src
    python app.py
        ```
    ````

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).
