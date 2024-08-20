from flask import Blueprint, request, jsonify, Response
from model import db, User
from routes.elastic_routes import sync_users
from RAGpipeline.pipeline import get_response
import json

RAG_bp = Blueprint('RAG_bp', __name__)

@RAG_bp.route('/smartSearch', methods=['POST'])
def returnRAGresults():
    data = request.get_json()

    # # Assuming the query is the last item in the list
    # query = data[-1].get('query', '') if isinstance(data, list) and data else ''

    if not data or 'query' not in data:
        return Response(json.dumps({'error': 'Invalid input'}), status=400, mimetype='application/json')

    query = data['query']

    print('here is the query:', query)

    def generate():
        try:
            for chunk in get_response(query):
                yield chunk

                # print('chunk:', chunk)
        except Exception as e:
            error_message = json.dumps({'error': str(e)})
            yield error_message  # Return the error message as JSON string
    
    return Response(generate(), content_type='application/json')







# from flask import Blueprint, request, jsonify, Response
# from model import db, User
# from routes.elastic_routes import sync_users
# from RAGpipeline.pipeline import get_response
# import json
# import asyncio

# RAG_bp = Blueprint('RAG_bp', __name__)

# @RAG_bp.route('/smartSearch', methods=['POST'])
# def returnRAGresults():
#     data = request.get_json()

#     # # Assuming the query is the last item in the list
#     # query = data[-1].get('query', '') if isinstance(data, list) and data else ''

#     if not data or 'query' not in data:
#         return Response(json.dumps({'error': 'Invalid input'}), status=400, mimetype='application/json')

#     query = data['query']

#     print('here is the query:', query)

#     async def generate():
#         try:
#             async for chunk in get_response(query):
#                 yield chunk

#                 # print('chunk:', chunk)
#         except Exception as e:
#             error_message = json.dumps({'error': str(e)})
#             yield error_message  # Return the error message as JSON string
    
#     async def stream_response():
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         async for chunk in generate():
#             yield chunk

#     return Response(stream_response(), content_type='application/json')

