import falcon
import falcon.media
from library import auth


cors = falcon.CORSMiddleware(allow_origins="*",
            expose_headers="*",
            allow_credentials="*")
# cors = CORS(allow_all_origins=True,
#             allow_all_methods=True,
#             allow_all_headers=True,
#             allow_credentials_all_origins=True)


api = falcon.App(middleware=[cors, auth.Auth()])

handler = falcon.media.MultipartFormHandler()
#
# # Assume text fields to be encoded in latin-1 instead of utf-8
# handler.parse_options.default_charset = 'latin-1'
#
# # Allow an unlimited number of body parts in the form
handler.parse_options.max_body_part_buffer_size = 1048576
api.req_options.media_handlers[falcon.MEDIA_MULTIPART] = handler
#
# # Afford parsing msgpack-encoded body parts directly via part.get_media()
# extra_handlers = {
#     falcon.MEDIA_MSGPACK: falcon.media.MessagePackHandler()
# }
# handler.parse_options.media_handlers.update(extra_handlers)
# from falcon_multipart.middleware import MultipartMiddleware

# api.req_options.auto_parse_qs_csv = False