from django.db import IntegrityError
from django.test import TransactionTestCase

from main.models import Post


class PostTestCase(TransactionTestCase):
    def test_thread_vs_reply(self):
        # Happy path:

        thread = Post.objects.create(subject="Hey", comment="Monica")
        self.assertTrue(thread.is_thread)

        reply = Post.objects.create(parent_thread=thread, comment="Cool")
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
