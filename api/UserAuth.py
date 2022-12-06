from rest_framework import permissions
import jwt


class authPermission(permissions.BasePermission):

    def has_permission(self, req, view):
        jwt_token = req.COOKIES.get('jwt')

        if not jwt_token:
            return False
        else:
            try:
                jwt_payload = jwt.decode(
                    jwt_token, 'secrets', algorithms="HS256")
                # more logic goes here if neccessory...

                return True
            except jwt.ExpiredSignatureError:
                return False
