import ulid
from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    Manager,
    Model,
    PositiveIntegerField,
    Q,
    SlugField,
    TextField,
)
from django.db.models.constraints import CheckConstraint
from django.urls import reverse


class Board(Model):
    id = SlugField(max_length=10, primary_key=True)
    name = CharField(max_length=50)
    description = TextField(max_length=2500)

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


def _upload_to(instance, filename):
    return f"pics/{str(ulid.new()).lower()}/{filename}"


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
    comment = TextField(max_length=2500, blank=True)
    parent_thread = ForeignKey(
        "self", on_delete=CASCADE, null=True, blank=True, related_name="replies"
    )
    board = ForeignKey(
        Board, on_delete=CASCADE, related_name="threads", null=True, blank=True
    )
    created_at = DateTimeField(auto_now_add=True)

    # Of course there's pic and thumbnail
    pic = ImageField(
        upload_to=_upload_to,
        height_field="pic_height",
        width_field="pic_width",
        null=True,
        blank=True,
    )
    pic_height = PositiveIntegerField(null=True)
    pic_width = PositiveIntegerField(null=True)
    thumbnail = ImageField(
        upload_to="thumbnails/",
        height_field="thumbnail_height",
        width_field="thumbnail_width",
        null=True,
        blank=True,
    )
    thumbnail_height = PositiveIntegerField(null=True)
    thumbnail_width = PositiveIntegerField(null=True)

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
            CheckConstraint(
                name="has_pic_if_is_thread",
                check=(
                    Q(parent_thread__isnull=True, pic__isnull=False)
                    | Q(parent_thread__isnull=False)
                ),
            ),
        ]

    @property
    def is_thread(self):
        return self.parent_thread is None

    @property
    def pic_public_url(self):
        # BIIIIG assumption that I name each env's bucket after their domain name.
        # TODO make this support plain old FileSystemStorage backend.
        return (
            f"https://{settings.AWS_STORAGE_BUCKET_NAME}/{self.pic.name}"
            if self.pic
            else ""
        )

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
