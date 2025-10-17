from django.core.management.base import BaseCommand
from vehicles.models import VehicleCategory, VehicleSubCategory
from bookings.models import Location


class Command(BaseCommand):
    help = 'Populate initial data for Fleet360'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data...')
        
        # Create vehicle categories
        categories_data = [
            {'category_name': 'Car'},
            {'category_name': 'SUV'},
            {'category_name': 'Van'},
            {'category_name': 'Truck'},
        ]
        
        for cat_data in categories_data:
            category, created = VehicleCategory.objects.get_or_create(**cat_data)
            if created:
                self.stdout.write(f'Created category: {category.category_name}')
        
        # Create vehicle subcategories
        subcategories_data = [
            {'category': 'Car', 'sub_category_name': 'Sedan'},
            {'category': 'Car', 'sub_category_name': 'Hatchback'},
            {'category': 'Car', 'sub_category_name': 'Coupe'},
            {'category': 'SUV', 'sub_category_name': 'Compact SUV'},
            {'category': 'SUV', 'sub_category_name': 'Full-size SUV'},
            {'category': 'Van', 'sub_category_name': 'Passenger Van'},
            {'category': 'Van', 'sub_category_name': 'Cargo Van'},
            {'category': 'Truck', 'sub_category_name': 'Pickup Truck'},
            {'category': 'Truck', 'sub_category_name': 'Heavy Truck'},
        ]
        
        for sub_data in subcategories_data:
            category = VehicleCategory.objects.get(category_name=sub_data['category'])
            subcategory, created = VehicleSubCategory.objects.get_or_create(
                category=category,
                sub_category_name=sub_data['sub_category_name']
            )
            if created:
                self.stdout.write(f'Created subcategory: {subcategory.sub_category_name}')
        
        # Create locations
        locations_data = [
            {'name': 'Colombo', 'address': '123 Main Street, Colombo 01'},
            {'name': 'Kandy', 'address': '456 Temple Road, Kandy'},
            {'name': 'Negombo', 'address': '789 Airport Road, Negombo'},
            {'name': 'Galle', 'address': '321 Fort Road, Galle'},
            {'name': 'Jaffna', 'address': '654 Jaffna Road, Jaffna'},
        ]
        
        for loc_data in locations_data:
            location, created = Location.objects.get_or_create(**loc_data)
            if created:
                self.stdout.write(f'Created location: {location.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial data!')
        )
