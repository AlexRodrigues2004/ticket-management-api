import factory
from faker import Faker
from django.contrib.auth import get_user_model
from customers.models import Customer
from categories.models import Category
from tickets.models import Ticket
from interactions.models import Interaction

fake = Faker('pt_BR')
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    password = factory.PostGenerationMethodCall('set_password', 'senha123')
    role = 'cliente'


class AttendantFactory(UserFactory):
    role = 'atendente'


class AdminFactory(UserFactory):
    role = 'admin'
    is_staff = True


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email())
    phone = factory.LazyAttribute(lambda _: fake.phone_number()[:20])
    is_active = True


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence())


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=5))
    description = factory.LazyAttribute(lambda _: fake.paragraph())
    customer = factory.SubFactory(CustomerFactory)
    category = factory.SubFactory(CategoryFactory)
    status = Ticket.Status.ABERTO
    priority = Ticket.Priority.MEDIA
    created_by = factory.SubFactory(UserFactory)


class InteractionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Interaction

    ticket = factory.SubFactory(TicketFactory)
    user = factory.SubFactory(UserFactory)
    message = factory.LazyAttribute(lambda _: fake.paragraph())