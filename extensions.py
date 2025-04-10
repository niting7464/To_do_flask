from flask_jwt_extended import JWTManager
from models import db 
from models.revoked_token import RevokedToken

jwt = JWTManager()    # Initialize JWT without app

# This function checks if a token is in the blacklist
@jwt.token_in_blocklist_loader            
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # Get token's unique identifier
    return RevokedToken.query.filter_by(jti = jti).first() is not None # if found , token is blacklisted 




