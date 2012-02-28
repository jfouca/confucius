from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('confucius.views',
    url(r'^auto-assignment/$', 'auto_assignment', name='auto_assignment'),
    url(r'^submit/(?P<pk_assignment>\d+)$', 'submit_review', name="submit_review"),
    url(r'^selection/$', 'paper_selection_list', name="paper_selection_list"),
    url(r'^read/(?P<pk_paper>\d+)$', 'read_reviews', name="read_reviews"),
    url(r'^finalize/$', 'finalize_selection', name="finalize_selection"),
    url(r'^assignments/$', 'assignments', name="assignments"),
    url(r'^updateAssignmentsTables/$', 'updateAssignmentsTables', name="updateAssignmentsTables"),
    url(r'^updateReviewerList/$', 'updateReviewerList', name="updateReviewerList"),
    url(r'^deleteAssignmentRow/$', 'deleteAssignmentRow', name="deleteAssignmentRow"),
)
