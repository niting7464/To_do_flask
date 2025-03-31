from flask_jwt_extended import JWTManager

jwt = JWTManager()    # Initialize JWT without app
blacklisted_tokens = set()  # Store revoked tokens

# This function checks if a token is in the blacklist
@jwt.token_in_blocklist_loader            
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # Get token's unique identifier
    return jti in blacklisted_tokens       # If True, the request is denied