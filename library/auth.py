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

        #req.set_header('Access-Control-Allow-Origin', '*')
        # print("dddddd")
        #resp.body = "sdsfsdf"
        challenges = ['Token type="JWT"']

        # print(req.path)
        #print(not self.__valid(req))
        #print(req.auth)
        #print(not self._valid(req))
        #print(req.path not in path_config.path_routes_not_auth)
        # print(self.check_path(req.path));
        # print(not self.__valid(req));
        ##if not self.__valid(req) and req.path not in path_config.path_routes_not_auth:
        if not self.__valid(req) and self.check_path(req.path):
            description = ('The provided auth token is not valid. ' 
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://rni.co.id')


    def create_token(self, result_data, username, ip_addr_access):
        #print(result_data)
        payload = {
            'user_id': result_data['id_user'],
            'company_id': result_data['company_id'],
            'username': username,
            'ip_address': ip_addr_access
        }

        # print("create token section secret_key")
        # print(self.secret_key);
        # print("create token section algoritma")
        # print(self.algoritma);
        token = jwt.encode(payload, self.secret_key, self.algoritma)

        # print("create token jwt encode");
        # print(token);
        return json.dumps({'token': token,
                           'user_data':
                               {
                                'nik': result_data['nik'],
                                'name': result_data['name'],
                                'company_id': result_data['company_id'],
                                'user_id': result_data['id_user'],
                                'role': result_data['role']
                                }
                           })

    def __valid(self, req):
        token = req.get_header('Authorization')

        #print(token)
        #print("xxxxx")
        if token is not None:
            try:

                token_auth = str(token).split(" ")[1]
                #print(token_auth)
                payload = jwt.decode(token_auth, self.secret_key, self.algoritma)
                if payload['ip_address'] == req.access_route:

                    #print(payload['ip_address'] + req.access_route)
                    #print("llll")
                    params.par['user_id'] = payload['user_id']
                    params.par['username'] = payload['username']
                    params.par['company_id'] = payload['company_id']
                    #params.par['ip_address'] = payload['ip_address']
                    return True
                else:
                    #return True
                    return False
            except(jwt.DecodeError):
                #return True
                return False
        else:
            return False
            #return True

    def get_data_params(self, params_):
        return params.par[params_]