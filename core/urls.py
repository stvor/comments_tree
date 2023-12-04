from django.urls import path

from core.views import IndexView, GetComments, EditCommentView, DeleteCommentView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('get-all-comments/', GetComments.as_view(), name='get_comments'),

    path('edit-comment/', EditCommentView.as_view(), name='edit_comment'),
    path('delete-comment/', DeleteCommentView.as_view(), name='delete_comment'),
]
