import pytest
from django.urls import reverse

from comments.models import Comment
from history.models import ChangeHistory


@pytest.mark.django_db
def test_manager_can_add_comment_and_history(client, manager_user, contact_visible):
    client.force_login(manager_user)
    response = client.post(
        reverse("add_comment", kwargs={"target_type": "contact", "target_id": contact_visible.id}),
        {"text": "Looks good"},
    )
    assert response.status_code == 302
    comment = Comment.objects.get(target_type="contact", target_id=contact_visible.id)
    assert comment.text == "Looks good"
    assert ChangeHistory.objects.filter(target_type="contact", target_id=contact_visible.id, action_type="comment_created").exists()
