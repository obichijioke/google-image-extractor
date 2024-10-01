# Google Images Scraper

Google Images Scraper is a Python tool designed to scrape high-resolution images from Google Images based on provided links. It now supports multi-threading for faster scraping and can be easily deployed using Docker. This tool overcomes the limitations of some browser extensions that only download image thumbnails.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Docker
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/google-images-scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd google-images-scraper
   ```

3. Create the environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the Virtual Environment:

   ```bash
   # For Linux
   source .venv/bin/activate

   # For Windows

   # For Powershell
   .venv/Scripts/Activate.ps1
   # For Command Prompt
   .venv/Scripts/activate.bat
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   <br>

## Docker Setup

1. Build the Docker image:

   ```bash
   docker build -t google-images-scraper .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 5000:5000 google-images-scraper
   ```

   This will start the Flask application inside the container and map port 5000 of the container to port 5000 on your host machine.

## Usage

Once the Docker container is running, you can use the API as follows:

1. Send a POST request to `http://localhost:5000/scrape` with a JSON payload:

   ```json
   {
     "queries": ["cute puppies", "beautiful landscapes"],
     "images_per_query": 20
   }
   ```

2. The API will return a JSON response with the queries and their corresponding image URLs:

   ```json
   [
     {
       "query": "cute puppies",
       "image_urls": ["/images/cute_puppies_1234567890.jpg", ...]
     },
     {
       "query": "beautiful landscapes",
       "image_urls": ["/images/beautiful_landscapes_1234567891.jpg", ...]
     }
   ]
   ```

3. To download an image, send a GET request to `http://localhost:5000/images/<filename>`.

## Configuration

You can customize the behavior of the scraper by modifying the `config.yaml` file. This file is used to set up email configurations, search queries, and image limits.

## Project Structure

- `app.py`: The main Flask application file.
- `scraping/scraper.py`: Contains the Scraper class for web scraping.
- `downloader/downloader.py`: Handles image downloading.
- `config.yaml`: Configuration file for the scraper.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Instructions for building the Docker image.

## Contributing

Contributions to Google Images Scraper are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This program lets you download tons of images from Google Images. Please do not download or use any image that violates its copyright terms.

## Google Images Scraper API

This project provides an API for scraping image links from Google Images based on given queries.

## Setup

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have Chrome and ChromeDriver installed and properly configured.

## Running the API

Run the Flask application:

```
python app.py
```
