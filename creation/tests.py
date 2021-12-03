from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from resources.categories.models import Category, DayCategory
from resources.days.models import Day, DayVenue
from resources.venues.models import Venue

# Create your tests here.


class CreationIndex(TestCase):
    def setUp(self):
        self.client = Client()
        self.creation_url = "/creation/"

        User = get_user_model()
        self.test_username = "test"
        self.test_password = "test"
        self.test_user = User.objects.create_user(
            username=self.test_username,
            email="test2@test.test",
            password=self.test_password,
            first_name="test",
            last_name="test",
        )

    def test_creation_page_url_nouser(self):
        response = self.client.get(self.creation_url)
        self.assertEqual(response.status_code, 302)

    def test_creation_page_empty_days(self):
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(self.creation_url)
        self.assertTrue(response.context["userDayList"].count() == 0)

    def test_creation_page_present_days(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(self.creation_url)
        self.assertTrue(response.context["userDayList"].count() > 0)


class CreationEdit(TestCase):
    def setUp(self):
        self.client = Client()
        self.creation_url = "/creation"

        User = get_user_model()
        self.test_username = "test"
        self.test_password = "test"
        self.test_user = User.objects.create_user(
            username=self.test_username,
            email="test2@test.test",
            password=self.test_password,
            first_name="test",
            last_name="test",
        )

        self.test_day = Day.objects.create(creator=self.test_user, name="test")

    def test_creation_page_present_days(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")

        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(
            "%s/%d/detail" % (self.creation_url, self.test_day.id)
        )
        self.assertTrue(response.context["day"].name == "test")

    def test_creation_page_delete_dayvenue(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_venue = Venue.objects.create(yelp_id="test_yelp_id")
        self.test_dayvenue = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=1
        )

        self.assertTrue(self.test_day.dayvenue_set.count() == 1)

        self.client.login(username=self.test_username, password=self.test_password)
        self.client.get(
            "%s/%d/edit/delete_dayvenue/%d"
            % (self.creation_url, self.test_day.id, self.test_dayvenue.id)
        )

        self.assertTrue(self.test_day.dayvenue_set.count() == 0)

    def test_creation_page_move_up_dayvenue(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_venue = Venue.objects.create(yelp_id="test_yelp_id")
        self.test_dayvenue1 = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=1
        )

        self.test_dayvenue2 = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=2
        )

        self.client.login(username=self.test_username, password=self.test_password)
        self.client.get(
            "%s/%d/edit/%d/up"
            % (self.creation_url, self.test_day.id, self.test_dayvenue2.id)
        )

        self.assertTrue(DayVenue.objects.get(pk=self.test_dayvenue2.id).pos == 1)

    def test_creation_page_move_down_dayvenue(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_venue = Venue.objects.create(yelp_id="test_yelp_id")
        self.test_dayvenue1 = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=1
        )
        self.test_dayvenue2 = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=2
        )

        self.client.login(username=self.test_username, password=self.test_password)
        self.client.get(
            "%s/%d/edit/%d/down"
            % (self.creation_url, self.test_day.id, self.test_dayvenue1.id)
        )
        self.assertTrue(DayVenue.objects.get(pk=self.test_dayvenue1.id).pos == 2)

    def test_creation_page_addVenue(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_venue = Venue.objects.create(yelp_id="test_yelp_id")
        self.test_dayvenue1 = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=1
        )
        self.test_dayvenue2 = DayVenue.objects.create(
            day=self.test_day, venue=self.test_venue, pos=2
        )
        self.assertTrue(self.test_day.dayvenue_set.count() == 2)

        self.client.login(username=self.test_username, password=self.test_password)
        self.client.get(
            "%s/%d/edit/searchpage?yelp_id=test_yelp_id"
            % (self.creation_url, self.test_day.id)
        )
        self.assertTrue(self.test_day.dayvenue_set.count() == 3)


class DayCategoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.creation_url = "/creation"

        User = get_user_model()
        self.test_username = "test"
        self.test_password = "test"
        self.test_user = User.objects.create_user(
            username=self.test_username,
            email="test2@test.test",
            password=self.test_password,
            first_name="test",
            last_name="test",
        )
        self.test_day = Day.objects.create(creator=self.test_user, name="test")

    def test_day_category_page(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")

        self.client.login(username=self.test_username, password=self.test_password)
        response = self.client.get(
            "%s/%d/edit/categories" % (self.creation_url, self.test_day.id)
        )
        self.assertTrue(response.status_code == 200)

    def test_add_day_category(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_category = Category.objects.create(cat="sushi")
        self.assertTrue(len(DayCategory.objects.filter(day=self.test_day)) == 0)
        self.client.login(username=self.test_username, password=self.test_password)
        self.client.get(
            "%s/%d/edit/categories/add/%d"
            % (self.creation_url, self.test_day.id, self.test_category.id)
        )
        self.assertTrue(len(DayCategory.objects.filter(day=self.test_day)) == 1)

    def test_remove_day_category(self):
        self.test_day = Day.objects.create(creator=self.test_user, name="test")
        self.test_category = Category.objects.create(cat="sushi")
        self.test_day_category = DayCategory.objects.create(
            day=self.test_day, cat=self.test_category
        )
        self.assertTrue(len(DayCategory.objects.filter(day=self.test_day)) == 1)
        self.client.login(username=self.test_username, password=self.test_password)
        self.client.get(
            "%s/%d/edit/categories/remove/%d"
            % (self.creation_url, self.test_day.id, self.test_category.id)
        )
        self.assertTrue(len(DayCategory.objects.filter(day=self.test_day)) == 0)
