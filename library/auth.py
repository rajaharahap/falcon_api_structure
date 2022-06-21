from config import jwt_config, path_config, params
import jwt
import json
import falcon


class Auth(object):

    def __init__(self):

        self.secret_key = jwt_config.jwt_profile["key"]
        self.algoritma = jwt_config.jwt_profile["algoritma"]
        self.__user_id = None

    def check_path(self, path:str):
        data = path_config.path_routes_not_auth
        for pathx in data:
            # print(pathx)
            if path.find(pathx)!= -1:
                return False
        return True

    def process_request(self, req, resp):
        challenges = ['Token type="JWT"']
        if not self.__valid(req) and self.check_path(req.path):
            description = ('The provided auth token is not valid. ' 
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://rni.co.id')


    def create_token(self, payload_data):
        token = jwt.encode(payload_data, self.secret_key, self.algoritma)
        return token

    def __valid(self, req):
        token = req.get_header('Authorization')
        if token is not None:
            try:

                token_auth = str(token).split(" ")[1]
                payload = jwt.decode(token_auth, self.secret_key, self.algoritma)
                params.par = payload
                return True
            except(jwt.DecodeError):
                return False
        else:
            return False

    def get_data_params(self, params_):
        return params.par[params_]