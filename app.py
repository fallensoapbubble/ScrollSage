from flask import Flask, request, jsonify, render_template
import json
from func import calltoAPI

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Add secret key for session


# venv venvF
# pip freeze > requirements.txt

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        """Main page with the form"""
        return render_template('page.html')
    
    elif request.method == 'POST':
        # Get all form data
        form_data = request.form.to_dict()
        
        print("=" * 50)
        print("FORM DATA RECEIVED:")
        print("=" * 50)
        
        # Parse entities from form data
        entities = []
        entity_index = 0
        
        while f'entity_{entity_index}_name' in form_data:
            name = form_data.get(f'entity_{entity_index}_name')
            entity_type = form_data.get(f'entity_{entity_index}_type')
            
            if name and entity_type:
                entity_data = {
                    'name': name,
                    'type': entity_type
                }
                entities.append(entity_data)
                print(f"Entity {entity_index + 1}: {name} ({entity_type})")
            
            entity_index += 1
        
        print(f"\nTotal entities received: {len(entities)}")
        print("Raw form data:", json.dumps(form_data, indent=2))
        print("=" * 50)
        
        return jsonify({
            'status': 'success',
            'message': f'Received {len(entities)} entities',
            'entities': entities
        })
    
    else:
        return 'Method not allowed', 405

@app.route('/insights', methods=['POST'])
def insights():
    """Handle the insights API endpoint that the JavaScript calls"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        print("=" * 50)
        print("INSIGHTS API DATA RECEIVED:")
        print("=" * 50)
        
        if not data or 'entities' not in data:
            print("Error: No entities data received")
            return jsonify({'error': 'No entities data provided'}), 400
        
        entities = data['entities']
        
        print(f"Number of entities: {len(entities)}")
        for i, entity in enumerate(entities, 1):
            print(f"Entity {i}: {entity.get('name', 'Unknown')} ({entity.get('type', 'Unknown')})")
        
        print("\nFull JSON data:")
        print(json.dumps(data, indent=2))

        
        print("=" * 50)
        
        # Mock response (you can replace this with actual analysis logic)
        # mock_insights = {
        #     'user_entities': entities,
        #     'insights': {
        #         'clusters': [
        #             'Tech-forward early adopters',
        #             'Creative content consumers',
        #             'Mainstream entertainment followers'
        #         ],
        #         'biases': [
        #             'Western-centric media consumption',
        #             'Preference for visual over textual content',
        #             'Algorithm-driven discovery patterns'
        #         ],
        #         'narratives': [
        #             'Digital minimalism vs. consumption culture',
        #             'Authenticity in influencer marketing',
        #             'Platform-specific content optimization'
        #         ],
        #         'recommendations': [
        #             'Diversify content sources beyond English-speaking creators',
        #             'Engage with long-form content to balance quick consumption',
        #             'Follow creators from different cultural backgrounds'
        #         ]
        #     }
        # }
        
        return jsonify(calltoAPI(entities))
        
    except Exception as e:
        print(f"Error processing insights request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/add/<int:a>/<int:b>', methods=['POST', 'GET'])
def add(a, b):
    print("=" * 30)
    print(f"ADD ENDPOINT CALLED: {a} + {b}")
    print(f"Method: {request.method}")
    print("=" * 30)
    
    if request.method == 'GET':
        result = a + b
        print(f"GET request - Result: {result}")
        return f'{result} is answer'
    
    elif request.method == 'POST':
        # Print any POST data if available
        if request.form:
            print("POST form data:", dict(request.form))
        if request.get_json():
            print("POST JSON data:", request.get_json())
        
        return f'Posted: {a} + {b} = {a + b}', 200
    
    else:
        return 'Method not allowed', 405

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Visit http://localhost:5000 to see the application")
    print("Check terminal for received data when forms are submitted")
    app.run(debug=True, host='0.0.0.0', port=5000)