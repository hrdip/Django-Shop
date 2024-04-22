import random 
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from ...models import ProductModel, ProductCategoryModel, ProductStatusType
from accounts.models import User, UserType
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent

class Command(BaseCommand):
    help = 'Generate fake products'
    def handle(self, *args, **options):
        fake = Faker()
        user = User.objects.get(type=UserType.admin.value)
        # list of images
        image_list = [
            "./images/img1.jpg",
            "./images/img2.jpg",
            "./images/img3.jpg",
            "./images/img4.jpg",
            "./images/img5.jpg",
            "./images/img6.jpg",
            "./images/img7.jpg",
            "./images/img8.jpg",
            "./images/img9.jpg",
            "./images/img10.jpg",
        ]
        categories = ProductCategoryModel.objects.all()
        # generate 10 fake productscategories only with title an slug
        for _ in range(50):
            user = user
            
            # choise between 1 to 4 categories
            num_categories = random.randint(1,4)
            selected_categories = random.sample(list(categories), num_categories)
            
            title = ' '.join([fake.word() for _ in range(1,3)])

            # generated slug with slugify like title
            # unicode for multy language
            slug = slugify(title,allow_unicode=True)
            selected_image = random.choice(image_list)
            image_obj = File(file=open(BASE_DIR / selected_image,"rb"), name=Path(selected_image).name)
            description = fake.paragraph(nb_sentences=1)
            stock = fake.random_int(min=0,max=10)
            status = random.choice(ProductStatusType.choices)[0]
            price = fake.random_int(min=10, max=1000)
            discount_pecent = fake.random_int(min=0, max=50)
            
            product = ProductModel.objects.create(
                user=user,
                title=title,
                slug=slug,
                image=image_obj,
                description=description,
                stock=stock,
                status=status,
                price=price,
                discount_pecent=discount_pecent,
            )
            product.category.set(selected_categories)
        self.stdout.write(self.style.SUCCESS('successfully generated 10 fake products '))