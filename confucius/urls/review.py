from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('confucius.views',
    url(r'^auto-assignment/$', 'auto_assignment', name='auto_assignment'),
    url(r'^finalize-assignment/$', 'finalize_assignment', name='finalize_assignment'),
    url(r'^submit/(?P<pk_assignment>\d+)$', 'submit_review', name="submit_review"),
    url(r'^paper-selection/$', 'paper_selection_list', name="paper_selection_list"),
    url(r'^read/(?P<pk_paper>\d+)$', 'read_reviews', name="read_reviews"),
    url(r'^finalize-selection/$', 'finalize_selection', name="finalize_selection"),
    url(r'^assignments/$', 'assignments', name="assignments"),
    url(r'^updateAssignmentsTables/$', 'updateAssignmentsTables', name="updateAssignmentsTables"),
    url(r'^updateReviewerList/$', 'updateReviewerList', name="updateReviewerList"),
    url(r'^deleteAssignmentRow/$', 'deleteAssignmentRow', name="deleteAssignmentRow"),
    url(r'^refreshAssignationNumber/$', 'refreshAssignationNumber', name="refreshAssignationNumber"),
    url(r'^clean-assignments/$', 'clean_assignments', name='clean_assignments'),
)
