from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Manager,
    Model,
    Q,
    TextField,
)
from django.db.models.constraints import CheckConstraint
from django.urls import reverse


class Board(Model):
    id = CharField(max_length=10, primary_key=True)
    name = CharField(max_length=50)
    description = TextField(max_length=2500)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "board"

    def __str__(self):
        return f"/{self.id}/ - {self.name}"

    def get_absolute_url(self):
        return reverse("board", kwargs={"board_id": self.id})


class ThreadManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent_thread=None)


class ReplyManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent_thread__isnull=False)


class Post(Model):
    """
    A Post can either be a Thread or Reply.
    It's a Reply iff it has a parent_thread.

    This is basically a poor man's Single Table Inheritance implementation:
        - CheckConstraints at least provide some guarantees.
        - thread_objects/reply_objects help avoid mistakes when querying one of the two.

    In return we can cleanly implement universal "link to post" regardless of if the
    post is a thread or reply.

    (if someone finds a cleaner way to model this in Django, I'm all ears tbh)
    """

    subject = CharField(max_length=250, blank=True)
    comment = TextField(max_length=2500)
    parent_thread = ForeignKey(
        "self", on_delete=CASCADE, null=True, blank=True, related_name="replies"
    )
    board = ForeignKey(
        Board, on_delete=CASCADE, related_name="threads", null=True, blank=True
    )
    created_at = DateTimeField(auto_now_add=True)

    objects = Manager()
    thread_objects = ThreadManager()
    reply_objects = ReplyManager()

    class Meta:
        db_table = "post"
        constraints = [
            CheckConstraint(
                name="has_subject_iff_is_thread",
                check=(
                    (Q(parent_thread__isnull=True) & ~Q(subject=""))
                    | Q(parent_thread__isnull=False, subject="")
                ),
            ),
            CheckConstraint(
                name="has_board_iff_is_thread",
                check=(
                    Q(parent_thread__isnull=True, board__isnull=False)
                    | Q(parent_thread__isnull=False, board__isnull=True)
                ),
            ),
        ]

    @classmethod
    def create_thread(cls, board_id, subject, comment):
        return cls.objects.create(board_id=board_id, subject=subject, comment=comment)

    @classmethod
    def create_reply(cls, thread_id, comment):
        return cls.objects.create(parent_thread_id=thread_id, comment=comment)

    @property
    def is_thread(self):
        return self.parent_thread is None

    def __str__(self):
        if self.is_thread:
            return f"Thread ({self.id}) {self.subject[:50]}"
        else:
            return f"Reply ({self.id}) {self.comment[:50]}"

    def get_absolute_url(self):
        if self.is_thread:
            return reverse(
                "thread", kwargs={"board_id": self.board_id, "thread_id": self.id}
            )
        else:
            thread = self.parent_thread
            thread_url = reverse(
                "thread", kwargs={"board_id": thread.board_id, "thread_id": thread.id}
            )
            return f"{thread_url}#p{self.id}"
