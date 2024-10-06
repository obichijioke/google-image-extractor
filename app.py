from flask import Flask, request, jsonify, send_from_directory
from scraping.scraper import Scraper
import os
import shutil

app = Flask(__name__)

# Global variable to store the download path
DOWNLOAD_PATH = '/app/downloaded_images'

@app.route('/scrape', methods=['POST'])
def scrape_images():
    data = request.json
    query = data.get('query', '')
    images_per_query = data.get('images_per_query', 10)
    
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    
    try:
        scraper = Scraper(show_ui=False, download_path=DOWNLOAD_PATH)
        image_paths = scraper.scrape(query, images_per_query)
        # Convert local paths to downloadable URLs
        image_urls = [f"/images/{os.path.basename(path)}" for path in image_paths]
        return jsonify({'query': query, 'image_urls': image_urls})
    except Exception as e:
        print(f"Error scraping query '{query}': {str(e)}")
        return jsonify({'query': query, 'error': str(e)}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(DOWNLOAD_PATH, filename)

@app.route('/delete-images', methods=['POST'])
def delete_images():
    try:
        # Check if the directory exists
        if os.path.exists(DOWNLOAD_PATH):
            # Remove all files and subdirectories
            for filename in os.listdir(DOWNLOAD_PATH):
                file_path = os.path.join(DOWNLOAD_PATH, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
            
            return jsonify({'message': 'All images deleted successfully'}), 200
        else:
            return jsonify({'message': 'Download directory does not exist'}), 404
    except Exception as e:
        return jsonify({'error': f'An error occurred while deleting images: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)