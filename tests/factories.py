import factory
from apps.profiles.models import Profile
from django.db.models.signals import post_save
from faker import Factory as FakerFactory
from real_estate.settings.base import AUTH_USER_MODEL

"""
In Django testing, a factories.py file is often used to define factory functions for creating test data. T
hese factory functions help in generating model instances with predefined or random data,
making it easier to set up test scenarios and ensuring that your tests are more robust and repeatable.

Here are a few reasons why using a factories.py file can be beneficial:

1. Easier Test Data Creation: Instead of manually creating instances of your models with specific data each time you write a test, 
you can use factory functions to generate instances with default or customized values. This simplifies the process of creating test data.

2. Maintainability: If the structure of your models changes, 
you only need to update the factory functions in one place (the factories.py file) rather than making changes throughout your test suite.

3. Code Reusability: Once you define a factory for a specific model, you can reuse it across multiple tests. 
This promotes code reusability and reduces redundancy in your test code.

4. Randomized Data: Factories often provide a way to generate randomized data, 
which is useful for testing scenarios with diverse data sets. 
This helps in uncovering potential issues related to unexpected data values.

5. Readable Tests: Using factory functions makes your test code more readable and concise. 
Test readers can quickly understand the intent of the test without getting bogged down in the details of data creation.
"""

faker = FakerFactory.create()

@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("tests.factories.UserFactory")
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    about_me = factory.LazyAttribute(lambda x: faker.sentence(nb_words=5))
    license = factory.LazyAttribute(lambda x: faker.text(max_nb_chars=6))
    profile_photo = factory.LazyAttribute(
        lambda x: faker.file_extension(category="image")
    )
    gender = factory.LazyAttribute(lambda x: f"other")
    country = factory.LazyAttribute(lambda x: faker.country_code())
    city = factory.LazyAttribute(lambda x: faker.city())
    is_buyer = False
    is_seller = False
    is_agent = False
    top_agent = False
    rating = factory.LazyAttribute(lambda x: faker.random_int(min=1, max=5))
    num_reviews = factory.LazyAttribute(lambda x: faker.random_int(min=0, max=25))

    class Meta:
        model = Profile


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    username = factory.LazyAttribute(lambda x: faker.first_name())
    email = factory.LazyAttribute(lambda x: f"bilvad2@gmail.com")
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    class Meta:
        model = AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)