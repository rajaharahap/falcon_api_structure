import falcon
from library import auth
# from falcon_multipart.middleware import MultipartMiddleware

cors = falcon.CORSMiddleware(allow_origins="*",
            expose_headers="*",
            allow_credentials="*")
# cors = CORS(allow_all_origins=True,
#             allow_all_methods=True,
#             allow_all_headers=True,
#             allow_credentials_all_origins=True)


api = falcon.App(middleware=[cors, auth.Auth()])
# api.req_options.auto_parse_qs_csv = False