from .serializers import *
import jwt
from .models import *

class isLoggedIn:

    def __init__(self,get_response) -> None:
        self.get_response = get_response

    def __call__(self,request,*args,**kwargs):
        token = request.headers.get('Authorization')

        try:
            decoded_token = jwt.decode(token,'secret',algorithms=['HS256'])

            user = Administrator.objects.get(id=decoded_token['id'])

            serializer = AdministratorSerializer(user)

            request.Administrator = user
            request.humaira = 'humaira'

        except Exception as e:
            print(e)
            request.humaira = token

        response = self.get_response(request)

        return response