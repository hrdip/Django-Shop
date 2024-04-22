from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from ...models import ProductCategoryModel

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        # generate 10 fake productscategories only with title an slug
        for _ in range(10):
            title = fake.word()
            # generated slug with slugify like title
            # unicode for multy language
            slug = slugify(title,allow_unicode=True)
            ProductCategoryModel.objects.get_or_create(
                title=title,
                slug=slug
            )
        self.stdout.write(self.style.SUCCESS('successfully generated 10 fake categories '))