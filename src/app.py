from flask import Flask, request, jsonify
import psycopg2
import numpy as np
import requests

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="ScottishPowerCodeChallenge",
    user="mohammed.latif",
    password="your_password"
)

# Hybrid search endpoint
@app.route('/search', methods=['GET'])
def hybrid_search():
    keyword = request.args.get('keyword', '')
    vector_str = request.args.get('vector', None)

    # Convert the vector from string to numpy array
    vector = np.array([float(x) for x in vector_str.split(',')]) if vector_str else None

    try:
        with conn.cursor() as cur:
            # Keyword search
            cur.execute("""
                SELECT mi.id, mi.title, mi.author, mi.publication_date, mi.category, mc.content
                FROM magazine_information mi
                JOIN magazine_content mc ON mi.id = mc.magazine_id
                WHERE mi.title ILIKE %s OR mi.author ILIKE %s OR mc.content ILIKE %s
            """, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            keyword_results = cur.fetchall()

            # Vector search
            vector_results = []
            if vector is not None:
                # Ensure the vector is of the correct dimension (300)
                if len(vector) != 300:
                    return jsonify({'error': 'Vector must have exactly 300 dimensions'}), 400

                cur.execute("""
                    SELECT id, 1 - (vector_representation <=> %s::vector) AS similarity
                    FROM magazine_content
                    ORDER BY similarity DESC
                    LIMIT 10
                """, (vector.tolist(),))
                vector_results = cur.fetchall()

        # Combine results
        combined_results = {
            'keyword_results': [dict(zip([desc[0] for desc in cur.description], row)) for row in keyword_results],
            'vector_results': [dict(zip([desc[0] for desc in cur.description], row)) for row in vector_results]
        }

        return jsonify(combined_results)
    
    except psycopg2.DatabaseError as db_err:
        return jsonify({'error': f"Database error occurred: {str(db_err)}"}), 500
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

# Function to test the /search endpoint
def test_search_endpoint():
    try:
        # Example vector with 300 dimensions (fill with actual values for testing)
        vector = [0.1] * 300
        encoded_vector = ','.join(map(str, vector))
        response = requests.get('http://localhost:5000/search', params={'keyword': 'science', 'vector': encoded_vector})

        if response.headers.get('Content-Type') == 'application/json':
            print("Response JSON:", response.json())
        else:
            print("Received non-JSON response")
            print("Response Text:", response.text)
    
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {str(req_err)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    # Run the test function after starting the Flask application
    import threading
    def run_app():
        app.run(debug=True)
    
    threading.Thread(target=run_app).start()
    test_search_endpoint()
