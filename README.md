# Google Images Scraper

This project is a Flask-based web application that scrapes images from Google Images based on user queries. It provides a simple API to scrape images and retrieve them.

## Features

- Scrape images from Google Images based on a search query
- Download and store images on the server
- Retrieve scraped images via API
- Delete all downloaded images from the server

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/google-images-scraper.git
   cd google-images-scraper
   ```

2. Build the Docker image:

   ```bash
   docker build -t google-images-scraper .
   ```

3. Run the Docker container:

   ```bash
   docker run -p 5000:5000 google-images-scraper
   ```

The application will be available at `http://localhost:5000`.

## API Endpoints

### 1. Scrape Images

- **URL:** `/scrape`
- **Method:** POST
- **Data Params:**
  ```json
  {
    "query": "search term",
    "images_per_query": 10
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "query": "search term",
      "image_urls": ["url1", "url2", ...]
    }
    ```

### 2. Retrieve Image

- **URL:** `/images/<filename>`
- **Method:** GET
- **Success Response:**
  - **Code:** 200
  - **Content:** Image file

### 3. Delete All Images

- **URL:** `/delete-images`
- **Method:** POST
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "message": "All images deleted successfully"
    }
    ```

## Error Handling

The API will return appropriate error messages and status codes for various scenarios, such as:

- Invalid requests
- Scraping errors
- File not found errors

## Notes

- The scraper uses Selenium with Chrome in headless mode.
- Images are stored in the `/app/downloaded_images` directory within the container.
- The application runs in debug mode by default. For production, disable debug mode and add appropriate security measures.

## License

[MIT License](LICENSE)

## Disclaimer

This tool is for educational purposes only. Be sure to comply with Google's terms of service and respect copyright laws when using this scraper.
