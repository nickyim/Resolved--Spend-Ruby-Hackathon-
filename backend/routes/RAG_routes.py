from flask import Blueprint, request, jsonify, Response
from model import db, User
from routes.elastic_routes import sync_users
from RAGpipeline.pipeline import get_response

user_bp = Blueprint('RAG_bp', __name__)

@user_bp.route('/smartSearch', methods=['POST'])
def returnRAGresults():
    data = request.get_json()

    # Assuming the query is the last item in the list
    query = data[-1].get('query', '') if isinstance(data, list) and data else ''

    print('here is the query:', query)
    def generate():
        try:
            for chunk in get_response(query):
                yield chunk

                # print('chunk:', chunk)
        except Exception as e:
            yield jsonify ({'error': str(e)}), 500  # Return the error message as JSON
    
    return Response(generate(), content_type='application/json')
