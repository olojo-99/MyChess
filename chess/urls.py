from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .forms import *
from . import views, admin

urlpatterns = [
    path('', views.index, name="index"),

   # account stuff
   path('login/',views.UserLogin.as_view(template_name="login.html", authentication_form=UserLoginForm)),
   path('logout/', views.logout_user, name="logout"),
   path('signup/', views.UserSignup.as_view(), name="register"),
   
   path('account/', views.account, name="account"),
   path('game/<int:game_id>', views.game, name="game"),
   path('start_game/<int:opponent_id>', views.start_game),
]  + static(settings.IMG_URL, document_root=settings.IMG_ROOT)