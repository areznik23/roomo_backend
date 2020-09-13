from django.conf.urls import url
from .views import (
                    get_next_roommate,
                    get_next_roommate_no_follow,
                    get_initial_option
                )

urlpatterns = [

    url(r'^f$', get_next_roommate),
    url(r'^nf$', get_next_roommate_no_follow),
    url(r'^io$', get_initial_option)

]