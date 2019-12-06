from django.test import TestCase

from caoweb.models import Board, Post


class BoardViewTestCase(TestCase):
    def test_order_threads_by_latest_last_reply_first(self):
        board = Board.objects.create(id="4.0", name="Công nghệ", description="Ehhhhhh")

        thread1 = Post.create_thread(board.id, "ONE", "foo")
        thread2 = Post.create_thread(board.id, "TWO", "foo")
        thread3 = Post.create_thread(board.id, "THREE", "foo")

        Post.create_reply(thread1.id, "thread1 sucks")
        Post.create_reply(thread1.id, "thread1 rocks")

        Post.create_reply(thread2.id, "thread2 sucks")
        Post.create_reply(thread2.id, "thread2 sucks")
        Post.create_reply(thread2.id, "thread2 sucks")

        Post.create_reply(thread3.id, "thread3 sucks")

        Post.create_reply(thread1.id, "thread1 sucks")

        resp = self.client.get("/4.0/")
        text = resp.content.decode()
        i1, i2, i3 = text.find("ONE"), text.find("TWO"), text.find("THREE")
        self.assertTrue(i1 < i3 < i2)


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
