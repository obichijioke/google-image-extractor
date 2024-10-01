from flask import Flask, request, jsonify, send_from_directory
from scraping.scraper import Scraper
import concurrent.futures
import os

app = Flask(__name__)

# Global variable to store the download path
DOWNLOAD_PATH = ''

@app.route('/scrape', methods=['POST'])
def scrape_images():
    global DOWNLOAD_PATH
    data = request.json
    queries = data.get('queries', [])
    images_per_query = data.get('images_per_query', 10)
    DOWNLOAD_PATH = data.get('download_path', 'downloaded_images')
    
    # Convert to absolute path
    DOWNLOAD_PATH = os.path.abspath(DOWNLOAD_PATH)
    
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    
    results = []
    
    def scrape_single_query(query):
        try:
            scraper = Scraper(num_threads=1, show_ui=False, download_path=DOWNLOAD_PATH)
            image_paths = scraper.scrape(query, images_per_query)
            # Convert local paths to downloadable URLs
            image_urls = [f"http://localhost:5000/images/{os.path.basename(path)}" for path in image_paths]
            return {'query': query, 'image_urls': image_urls}
        except Exception as e:
            print(f"Error scraping query '{query}': {str(e)}")
            return {'query': query, 'error': str(e)}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(scrape_single_query, query) for query in queries]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    return jsonify(results)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(DOWNLOAD_PATH, filename)

if __name__ == '__main__':
    app.run(debug=True)