from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/account/social/google/callback/"
    client_class = OAuth2Client

# Todo: Create GitHub OAuth App
class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = "http://localhost:8000/account/social/github/callback/"
    client_class = OAuth2Client
