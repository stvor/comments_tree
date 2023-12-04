from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from core.models import Comment


class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'index.html'


class GetComments(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(is_deleted=False).order_by('created')
        return JsonResponse({'data': [
            self.serialize_comment(comment)
            for comment in comments
        ]})

    def serialize_comment(self, comment):
        return {
            'id': comment.id,
            'text': comment.text,
            'parent_id': comment.parent_id,
            'created': comment.created.isoformat(),
            'updated': comment.updated.isoformat(),
            'is_deleted': comment.is_deleted,
        }


class EditCommentView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)

        comment.text = request.POST.get('text')
        comment.updated = timezone.now()
        comment.save(update_fields=['text', 'updated'])

        return JsonResponse({})


class DeleteCommentView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id)

        comment.is_deleted = bool(not comment.is_deleted)
        comment.updated = timezone.now()
        comment.save(update_fields=['is_deleted', 'updated'])

        return JsonResponse({})
