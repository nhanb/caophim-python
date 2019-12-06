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
    """

    subject = CharField(max_length=250, blank=True)
    comment = TextField(max_length=2500)
    parent_thread = ForeignKey(
        "self", on_delete=CASCADE, null=True, blank=True, related_name="replies"
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
        ]

    @property
    def is_thread(self):
        return self.parent_thread is None

    def __str__(self):
        if self.is_thread:
            return f"Thread ({self.id}) {self.subject[:50]}"
        else:
            return f"Reply ({self.id}) {self.comment[:50]}"
