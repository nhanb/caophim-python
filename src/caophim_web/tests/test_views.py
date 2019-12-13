from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from caophim_web.models import Board, Post


class BoardViewTestCase(TestCase):
    def test_order_threads_by_latest_last_reply_first(self):
        board = Board.objects.create(id="cn", name="Công nghệ", description="Ehhhhhh")

        thread1 = Post.objects.create(board=board, subject="ONE", comment="foo")
        thread2 = Post.objects.create(
            board=board, subject="TWO", pic=SimpleUploadedFile("fn", b"")
        )
        thread3 = Post.objects.create(
            board=board,
            subject="THREE",
            comment="foo",
            pic=SimpleUploadedFile("fn", b""),
        )

        Post.objects.create(parent_thread=thread1, comment="thread1 sucks")
        Post.objects.create(parent_thread=thread1, comment="thread1 rocks")

        Post.objects.create(parent_thread=thread2, comment="thread2 sucks")
        Post.objects.create(parent_thread=thread2, pic=SimpleUploadedFile("fn", b""))
        Post.objects.create(parent_thread=thread2, comment="thread2 sucks")

        Post.objects.create(parent_thread=thread3, comment="thread3 sucks")

        Post.objects.create(parent_thread=thread1, pic=SimpleUploadedFile("fn", b""))

        resp = self.client.get("/cn/")
        text = resp.content.decode()
        i1, i2, i3 = text.find("ONE"), text.find("TWO"), text.find("THREE")
        self.assertTrue(i1 < i3 < i2, text)


# class CreateThreadViewTestCase(TestCase):
#     def test_create(self):
#         board = Board.objects.create(id="4.0", name="Công nghệ", description="Ehhhhhh")
#         resp = self.client.post(
#             "/create-thread",
#             {
#                 "subject": "I'm a subject",
#                 "comment": "Lorem ipsum I totally forgot how that went",
#                 "board": "4.0",
#             },
#         )
