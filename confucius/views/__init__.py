<<<<<<< HEAD
from confucius.views.confviews import (list_conference, edit_conference, home_conference, change_conference, close_conference, open_conference, invite_reviewer, reviewer_invitation_response)
from confucius.views.authviews import (close_account, edit_account, main_page, create_account, activate_account)
from confucius.views.conferenceviews import (create_conference)
=======
from confucius.views.account import (close_account, confirm_close_account, edit_account)
from confucius.views.conference import (ConferenceToggleView, ConferenceUpdateView, MembershipListView, exit_mockuser, use_mockuser, create_alert)
>>>>>>> e0d3239ba6faa716125af99f0376c67cef0e3223
