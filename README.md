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

## Hosting on a Server

To host this application on a server, follow these steps:

1. Set up a server:

   - Choose a cloud provider (AWS, Google Cloud, DigitalOcean, etc.)
   - Select a Linux-based OS (Ubuntu recommended)
   - Ensure the server has at least 2GB of RAM and 1 CPU core

2. SSH into your server:

   ```bash
   ssh user@your_server_ip
   ```

3. Install Docker (if not pre-installed):

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

4. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/google-images-scraper.git
   cd google-images-scraper
   ```

5. Build and run the Docker container:

   ```bash
   sudo docker build -t google-images-scraper .
   sudo docker run -d -p 80:5000 google-images-scraper
   ```

6. Configure firewall (if needed):

   ```bash
   sudo ufw allow 80/tcp
   sudo ufw enable
   ```

7. (Optional) Set up a domain name:

   - Purchase a domain name from a registrar
   - Configure DNS A record to point to your server's IP address

8. (Recommended) Set up HTTPS:
   - Install Nginx:
     ```bash
     sudo apt update
     sudo apt install nginx
     ```
   - Install Certbot for Let's Encrypt:
     ```bash
     sudo apt install certbot python3-certbot-nginx
     ```
   - Configure Nginx as a reverse proxy (replace example.com with your domain):
     ```nginx
     server {
         listen 80;
         server_name example.com;
         location / {
             proxy_pass http://localhost:5000;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
         }
     }
     ```
   - Obtain SSL certificate:
     ```bash
     sudo certbot --nginx -d example.com
     ```

Your Google Images Scraper should now be accessible at `http://your_server_ip` or `https://your_domain.com` if you set up a domain and HTTPS.

Note: Ensure you comply with the terms of service of your hosting provider and respect the usage limits and policies of Google Images.
