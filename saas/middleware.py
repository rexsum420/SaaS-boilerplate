from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .context_processor import get_role
from django.utils import timezone
from owners.models import Owner
from management.models import Manager
from employees.models import Employee

User = get_user_model()

class ContextMiddleware(MiddlewareMixin):    
    def process_request(self, request):
        try:
            self.authenticate_user(request)
            if hasattr(request, 'user') and request.user.is_authenticated:
                role = get_role()
                if role == 'Owner':
                    rmodel = Owner.objects.get(user=request.user)
                elif role == 'Manager':
                    rmodel = Manager.objects.get(user=request.user)
                elif role == 'Employee':
                    rmodel = Employee.objects.get(user=request.user)
                rmodel.last_active = timezone.now()
                # run other functions here
                rmodel.save()
        except AuthenticationFailed:
            return self._unauthorized_response()
        
    # def fuction(self, request):
    #     do something here
    #     return request

    def authenticate_user(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        request.user = token_obj.user

    def _unauthorized_response(self):
        from django.http import JsonResponse
        return JsonResponse({'detail': 'Invalid token.'}, status=401)