from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import (
    Group,
    AnonymousUser,
)
from .models import (
    Book,
    Review,
    Topic,
    Record,
    SubTopic,
    SubRecord,
)


class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@email.com",
            password="testpass123",
        )
        self.book = Book.objects.create(
            title="Harry Potter",
            preview="Good Book",
            text="Bestseller",
        )

        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review="An excellent review",
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, "Harry Potter")
        self.assertEqual(self.book.preview, "Good Book")
        self.assertEqual(self.book.text, "Bestseller")

    def test_book_new_view_for_logged_in_user(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(reverse("book_new"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Добавление:")
        self.assertTemplateUsed((response, "learning/book_new.html"))

    """def test_book_new_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('book_new'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, '%s?next=/learning/books/new' % (reverse('account_login')))
        response = self.client.get(
            '%s?next=/books/' % (reverse('account_login'))
        )
        self.assertContains(response, 'Вход')
    """

    def test_book_detail_view_with_permissions(self):
        self.client.login(email="reviewuser@email.com", password="testpass123")
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "An excellent review")
        self.assertTemplateUsed(response, "learning/book_detail.html")


class TopicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name="teachers")

        cls.anon_user = AnonymousUser()

        cls.testuser_0 = get_user_model().objects.create_user(
            username="testuser_0",
            email="testuser_0@email.com",
            password="testpass123",
        )

        cls.testuser_1 = get_user_model().objects.create_user(
            username="testuser_1",
            email="testuser_1@email.com",
            password="testpass123",
        )
        cls.testuser_1.groups.add(
            cls.group
        )  # Добавить в группу с индексом 1 ("teachers")

        cls.topic_everyone = Topic.objects.create(
            title="Topic for everyone",
            access_level=0,
            author=cls.testuser_0,
        )

        cls.topic_group = Topic.objects.create(
            title="Topic for group",
            access_level=1,
            author=cls.testuser_1,
        )

        cls.topic_private = Topic.objects.create(
            title="Topic for one person",
            access_level=2,
            author=cls.testuser_0,
        )

    def test_topic_view_content(self):
        self.assertEqual(self.anon_user.__str__(), "AnonymousUser")
        self.assertEqual(self.testuser_1.groups.filter(name="teachers").exists(), True)

        response = self.client.get(self.topic_everyone.get_absolute_url())
        no_response = self.client.get("learning/topic/12345")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Topic for everyone")
        self.assertTemplateUsed(response, "learning/record_list.html")

        self.assertEqual(self.topic_everyone.title, "Topic for everyone")
        self.assertEqual(self.topic_group.title, "Topic for group")
        self.assertEqual(self.topic_private.title, "Topic for one person")

        self.assertEqual(self.topic_everyone.access_level, 0)
        self.assertEqual(self.topic_group.access_level, 1)
        self.assertEqual(self.topic_private.access_level, 2)

        self.assertEqual(self.topic_everyone.author, self.testuser_0)
        self.assertEqual(self.topic_group.author, self.testuser_1)
        self.assertEqual(self.topic_private.author, self.testuser_0)

        self.assertEqual(self.topic_everyone.image, "")

    def test_topic_access_level(self):
        # Аноним
        self.client.login(email="")
        response_everyone = self.client.get(self.topic_everyone.get_absolute_url())
        response_group = self.client.get(self.topic_group.get_absolute_url())
        response_private = self.client.get(self.topic_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 302)
        self.assertEqual(response_private.status_code, 302)

        # Пользователь не состоящий к группе
        self.client.login(email="testuser_0@email.com", password="testpass123")
        response_everyone = self.client.get(self.topic_everyone.get_absolute_url())
        response_group = self.client.get(self.topic_group.get_absolute_url())
        response_private = self.client.get(self.topic_private.get_absolute_url())
        self.assertEqual(self.testuser_0.is_active, True)
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 403)
        self.assertEqual(response_private.status_code, 200)  # Только автор Темы

        # Пользователь состоящий в группе
        self.client.login(email="testuser_1@email.com", password="testpass123")
        response_everyone = self.client.get(self.topic_everyone.get_absolute_url())
        response_group = self.client.get(self.topic_group.get_absolute_url())
        response_private = self.client.get(self.topic_private.get_absolute_url())
        self.assertEqual(self.testuser_1.is_active, True)
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 200)
        self.assertEqual(response_private.status_code, 403)


class RecordTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name="teachers")
        cls.anon_user = AnonymousUser()

        cls.testuser_0 = get_user_model().objects.create_user(
            username="testuser_0",
            email="testuser_0@email.com",
            password="testpass123",
        )

        cls.testuser_1 = get_user_model().objects.create_user(
            username="testuser_1",
            email="testuser_1@email.com",
            password="testpass123",
        )
        cls.testuser_1.groups.set([1])

        cls.topic_for_test_records = Topic.objects.create(
            title="Just Topic",
            access_level=0,
            author=cls.testuser_1,
        )

        cls.record_everyone = Record.objects.create(
            topic=cls.topic_for_test_records,
            title="Record for everyone",
            preview="Preview for everyone",
            text="Text for everyone",
            access_level=0,
            author=cls.testuser_0,
        )

        cls.record_group = Record.objects.create(
            topic=cls.topic_for_test_records,
            title="Record for group",
            preview="Preview for group",
            text="Text for group",
            access_level=1,
            author=cls.testuser_1,
        )

        cls.record_private = Record.objects.create(
            topic=cls.topic_for_test_records,
            title="Record for one person",
            preview="Preview for one person",
            text="Text for one person",
            access_level=2,
            author=cls.testuser_0,
        )

    def test_record_view_content(self):
        response = self.client.get(self.record_everyone.get_absolute_url())
        no_response = self.client.get("learning/topic/record-12345")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Record for everyone")
        self.assertTemplateUsed(response, "learning/record_detail.html")

        self.assertEqual(self.record_everyone.topic, self.topic_for_test_records)
        self.assertEqual(self.record_group.topic, self.topic_for_test_records)
        self.assertEqual(self.record_private.topic, self.topic_for_test_records)

        self.assertEqual(self.record_everyone.title, "Record for everyone")
        self.assertEqual(self.record_group.title, "Record for group")
        self.assertEqual(self.record_private.title, "Record for one person")

        self.assertEqual(self.record_everyone.preview, "Preview for everyone")
        self.assertEqual(self.record_group.preview, "Preview for group")
        self.assertEqual(self.record_private.preview, "Preview for one person")

        self.assertEqual(self.record_everyone.text, "Text for everyone")
        self.assertEqual(self.record_group.text, "Text for group")
        self.assertEqual(self.record_private.text, "Text for one person")

        self.assertEqual(self.record_everyone.access_level, 0)
        self.assertEqual(self.record_group.access_level, 1)
        self.assertEqual(self.record_private.access_level, 2)

        self.assertEqual(self.record_everyone.author, self.testuser_0)
        self.assertEqual(self.record_group.author, self.testuser_1)
        self.assertEqual(self.record_private.author, self.testuser_0)

    def test_record_access_level(self):
        # Anonymous
        self.client.login(email="")
        response_everyone = self.client.get(self.record_everyone.get_absolute_url())
        response_group = self.client.get(self.record_group.get_absolute_url())
        response_private = self.client.get(self.record_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 302)
        self.assertEqual(response_private.status_code, 302)

        # User without group
        self.client.login(username="testuser_0@email.com", password="testpass123")
        response_everyone = self.client.get(self.record_everyone.get_absolute_url())
        response_group = self.client.get(self.record_group.get_absolute_url())
        response_private = self.client.get(self.record_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 403)
        self.assertEqual(response_private.status_code, 200)  # Author

        # Group user
        self.client.login(username="testuser_1@email.com", password="testpass123")
        response_everyone = self.client.get(self.record_everyone.get_absolute_url())
        response_group = self.client.get(self.record_group.get_absolute_url())
        response_private = self.client.get(self.record_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 200)
        self.assertEqual(response_private.status_code, 403)  # dont author


class SubTopicTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name="teachers")
        cls.anon_user = AnonymousUser()

        cls.testuser_0 = get_user_model().objects.create_user(
            username="testuser_0",
            email="testuser_0@email.com",
            password="testpass123",
        )

        cls.testuser_1 = get_user_model().objects.create_user(
            username="testuser_1",
            email="testuser_1@email.com",
            password="testpass123",
        )
        cls.testuser_1.groups.add(cls.group)

        cls.topic_for_test_subtopic = Topic.objects.create(
            title="Just Topic",
            access_level=0,
            author=cls.testuser_1,
        )

        cls.subtopic_everyone = SubTopic.objects.create(
            topic=cls.topic_for_test_subtopic,
            title="Subtopic for everyone",
            access_level=0,
            author=cls.testuser_0,
        )

        cls.subtopic_group = SubTopic.objects.create(
            topic=cls.topic_for_test_subtopic,
            title="Subtopic for group",
            access_level=1,
            author=cls.testuser_1,
        )

        cls.subtopic_private = SubTopic.objects.create(
            topic=cls.topic_for_test_subtopic,
            title="Subtopic for one person",
            access_level=2,
            author=cls.testuser_0,
        )

    def test_subtopic_view_content(self):
        response = self.client.get(self.subtopic_everyone.get_absolute_url())
        no_response = self.client.get("learning/topic/subtopic/subrecord-12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Subtopic for everyone")
        self.assertTemplateUsed(response, "learning/subrecord_list.html")

        self.assertEqual(self.subtopic_everyone.topic, self.topic_for_test_subtopic)
        self.assertEqual(self.subtopic_group.topic, self.topic_for_test_subtopic)
        self.assertEqual(self.subtopic_private.topic, self.topic_for_test_subtopic)

        self.assertEqual(self.subtopic_everyone.title, "Subtopic for everyone")
        self.assertEqual(self.subtopic_group.title, "Subtopic for group")
        self.assertEqual(self.subtopic_private.title, "Subtopic for one person")

        self.assertEqual(self.subtopic_everyone.access_level, 0)
        self.assertEqual(self.subtopic_group.access_level, 1)
        self.assertEqual(self.subtopic_private.access_level, 2)

        self.assertEqual(self.subtopic_everyone.author, self.testuser_0)
        self.assertEqual(self.subtopic_group.author, self.testuser_1)
        self.assertEqual(self.subtopic_private.author, self.testuser_0)

    def test_subtopic_access_level(self):
        # Anonymous
        self.client.login(email="")
        response_everyone = self.client.get(self.subtopic_everyone.get_absolute_url())
        response_group = self.client.get(self.subtopic_group.get_absolute_url())
        response_private = self.client.get(self.subtopic_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 302)
        self.assertEqual(response_private.status_code, 302)

        # User without group
        self.client.login(email="testuser_0@email.com", password="testpass123")
        response_everyone = self.client.get(self.subtopic_everyone.get_absolute_url())
        response_group = self.client.get(self.subtopic_group.get_absolute_url())
        response_private = self.client.get(self.subtopic_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 403)
        self.assertEqual(response_private.status_code, 200)

        # Group user
        self.client.login(email="testuser_1@email.com", password="testpass123")
        response_everyone = self.client.get(self.subtopic_everyone.get_absolute_url())
        response_group = self.client.get(self.subtopic_group.get_absolute_url())
        response_private = self.client.get(self.subtopic_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 200)
        self.assertEqual(response_private.status_code, 403)


class SubRecordTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name="teachers")

        cls.testuser_0 = get_user_model().objects.create_user(
            username="testuser_0",
            email="testuser_0@email.com",
            password="testpass123",
        )

        cls.testuser_1 = get_user_model().objects.create_user(
            username="testuser_1",
            email="testuser_1@email.com",
            password="testpass123",
        )
        cls.testuser_1.groups.add(cls.group)

        cls.topic_for_test_subrecord = Topic.objects.create(
            title="Just Topic",
            access_level=0,
            author=cls.testuser_1,
        )

        cls.subtopic_for_test_subrecord = SubTopic.objects.create(
            topic=cls.topic_for_test_subrecord,
            title="Just SubTopic",
            access_level=0,
            author=cls.testuser_1,
        )

        cls.subrecord_everyone = SubRecord.objects.create(
            subtopic=cls.subtopic_for_test_subrecord,
            title="SubRecord for everyone",
            preview="Preview for everyone",
            text="Text for everyone",
            access_level=0,
            author=cls.testuser_0,
        )

        cls.subrecord_group = SubRecord.objects.create(
            subtopic=cls.subtopic_for_test_subrecord,
            title="SubRecord for group",
            preview="Preview for group",
            text="Text for group",
            access_level=1,
            author=cls.testuser_1,
        )

        cls.subrecord_private = SubRecord.objects.create(
            subtopic=cls.subtopic_for_test_subrecord,
            title="SubRecord for one person",
            preview="Preview for one person",
            text="Text for one person",
            access_level=2,
            author=cls.testuser_0,
        )

    def test_subrecord_view_content(self):
        response = self.client.get(self.subrecord_everyone.get_absolute_url())
        no_response = self.client.get("/learning/topic/subtopic/subrecord-12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "SubRecord for everyone")
        self.assertTemplateUsed(response, "learning/subrecord_detail.html")

        # Foreign Key Topic -> SubTopic -> SubRecord
        self.assertEqual(
            self.subrecord_everyone.subtopic.topic, self.topic_for_test_subrecord
        )
        self.assertEqual(
            self.subrecord_group.subtopic.topic, self.topic_for_test_subrecord
        )
        self.assertEqual(
            self.subrecord_private.subtopic.topic, self.topic_for_test_subrecord
        )

        # Foreign Key SubTopic -> SubRecord
        self.assertEqual(
            self.subrecord_everyone.subtopic, self.subtopic_for_test_subrecord
        )
        self.assertEqual(
            self.subrecord_group.subtopic, self.subtopic_for_test_subrecord
        )
        self.assertEqual(
            self.subrecord_private.subtopic, self.subtopic_for_test_subrecord
        )

        self.assertEqual(self.subrecord_everyone.title, "SubRecord for everyone")
        self.assertEqual(self.subrecord_group.title, "SubRecord for group")
        self.assertEqual(self.subrecord_private.title, "SubRecord for one person")

        self.assertEqual(self.subrecord_everyone.preview, "Preview for everyone")
        self.assertEqual(self.subrecord_group.preview, "Preview for group")
        self.assertEqual(self.subrecord_private.preview, "Preview for one person")

        self.assertEqual(self.subrecord_everyone.text, "Text for everyone")
        self.assertEqual(self.subrecord_group.text, "Text for group")
        self.assertEqual(self.subrecord_private.text, "Text for one person")

        self.assertEqual(self.subrecord_everyone.access_level, 0)
        self.assertEqual(self.subrecord_group.access_level, 1)
        self.assertEqual(self.subrecord_private.access_level, 2)

        self.assertEqual(self.subrecord_everyone.author, self.testuser_0)
        self.assertEqual(self.subrecord_group.author, self.testuser_1)
        self.assertEqual(self.subrecord_private.author, self.testuser_0)

    def test_subrecord_access_level(self):
        # Anonymous
        self.client.login(email="")
        response_everyone = self.client.get(self.subrecord_everyone.get_absolute_url())
        response_group = self.client.get(self.subrecord_group.get_absolute_url())
        response_private = self.client.get(self.subrecord_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 302)
        self.assertEqual(response_private.status_code, 302)

        # User withor group
        self.client.login(email="testuser_0@email.com", password="testpass123")
        response_everyone = self.client.get(self.subrecord_everyone.get_absolute_url())
        response_group = self.client.get(self.subrecord_group.get_absolute_url())
        response_private = self.client.get(self.subrecord_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 403)
        self.assertEqual(response_private.status_code, 200)
        
        # User withor group
        self.client.login(email="testuser_1@email.com", password="testpass123")
        response_everyone = self.client.get(self.subrecord_everyone.get_absolute_url())
        response_group = self.client.get(self.subrecord_group.get_absolute_url())
        response_private = self.client.get(self.subrecord_private.get_absolute_url())
        self.assertEqual(response_everyone.status_code, 200)
        self.assertEqual(response_group.status_code, 200)
        self.assertEqual(response_private.status_code, 403)