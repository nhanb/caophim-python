from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TransactionTestCase

from caoweb.models import Board, Post


class PostTestCase(TransactionTestCase):
    def test_thread_vs_reply(self):
        # Happy path:

        board = Board.objects.create(id="4.0", name="Công nghệ", description="Ehhhhhh")

        thread = Post.objects.create(
            board=board,
            subject="subject",
            comment="and comment",
            pic=SimpleUploadedFile("pic.png", b""),
        )
        self.assertTrue(thread.is_thread)

        reply = Post.objects.create(parent_thread=thread, comment="comment only")
        self.assertFalse(reply.is_thread)

        self.assertEqual(Post.thread_objects.all().get(), thread)
        self.assertEqual(Post.reply_objects.all().get(), reply)

        # Just confirming my check constraints are working as intended:

        with self.assertRaises(IntegrityError):
            Post.objects.create(comment="Monica")

        with self.assertRaises(IntegrityError):
            Post.objects.create(subject=None, comment="Monica")

        with self.assertRaises(IntegrityError):
            Post.objects.create(subject="", comment="Monica")

        with self.assertRaises(IntegrityError):
            Post.objects.create(subject="sub", comment="comm", parent_thread=thread)

        with self.assertRaises(IntegrityError, msg="Thread must belong to a board."):
            Post.objects.create(subject="sub", comment="comm")
