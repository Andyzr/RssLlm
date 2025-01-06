# RSS Feed News Summarizer

📰 A Streamlit web application that provides AI-powered summaries of your favorite RSS feeds using Google's Gemini model.

[Demo](https://rssllm.streamlit.app/)

## Features

- Fetch articles from any RSS feed URL.
- Summarize articles using Google's Gemini model.
- User-friendly interface with Streamlit.
- Adjustable number of articles to summarize.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Andyzr/RssLlm.git
    cd RssLlm
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the Gemini API key:
    - Add your Gemini API key to the `secrets.toml` file under a folder named after `.streamlit`.:
        ```toml
        GEMINI_API_KEY = "your-gemini-api-key"
        ```

## Usage

1. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501`.

3. Enter the RSS feed URL and adjust the number of articles to summarize in the sidebar.

4. Click the "Fetch and Summarize" button to get AI-powered summaries of the articles.

## File Structure

- `app.py`: Main application script.
- `requirements.txt`: List of dependencies.
- `secrets.toml`: Configuration file for storing secrets.
- `README.md`: Project documentation.

## License

This project is licensed under the MIT License.