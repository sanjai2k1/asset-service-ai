from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

def get_registered_serializer() -> JsonPlusSerializer:
    # Pass the list of modules directly into the constructor
    # The key is usually 'allowed_msgpack_modules' as a keyword argument
    serializer = JsonPlusSerializer(
        allowed_msgpack_modules=[
            ('domain.excel_analysis.state', 'InitSummarizerOutput'),
            ('domain.excel_analysis.state','QueryOutput'),
            ('domain.excel_analysis.state','QueryOutputResponse'),
            ('domain.excel_analysis.state','RouterDecision')


            
        ]
    )
    
    return serializer