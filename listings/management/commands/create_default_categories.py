from django.core.management.base import BaseCommand
from listings.models import Category, SubCategory

class Command(BaseCommand):
    help = 'Creates default job-related categories and subcategories'

    def handle(self, *args, **kwargs):
        # Define job categories and their subcategories
        job_categories = {
            'Technology': [
                'Software Development',
                'Web Development',
                'Mobile Development',
                'Data Science',
                'DevOps',
                'IT Support',
                'Cybersecurity',
                'UI/UX Design',
                'Project Management',
                'Quality Assurance',
            ],
            'Healthcare': [
                'Nursing',
                'Medical Doctor',
                'Pharmacy',
                'Physical Therapy',
                'Mental Health',
                'Dental',
                'Healthcare Administration',
                'Medical Research',
            ],
            'Education': [
                'Teaching',
                'Tutoring',
                'School Administration',
                'Curriculum Development',
                'Educational Technology',
                'Special Education',
                'Higher Education',
            ],
            'Finance': [
                'Accounting',
                'Banking',
                'Financial Analysis',
                'Investment',
                'Insurance',
                'Tax',
                'Financial Planning',
            ],
            'Marketing': [
                'Digital Marketing',
                'Content Marketing',
                'Social Media',
                'SEO/SEM',
                'Brand Management',
                'Market Research',
                'Public Relations',
            ],
            'Sales': [
                'B2B Sales',
                'B2C Sales',
                'Account Management',
                'Business Development',
                'Sales Operations',
                'Inside Sales',
                'Outside Sales',
            ],
            'Customer Service': [
                'Call Center',
                'Technical Support',
                'Customer Success',
                'Client Relations',
                'Help Desk',
            ],
            'Human Resources': [
                'Recruiting',
                'HR Management',
                'Training & Development',
                'Compensation & Benefits',
                'Employee Relations',
                'HR Information Systems',
            ],
            'Engineering': [
                'Civil Engineering',
                'Mechanical Engineering',
                'Electrical Engineering',
                'Chemical Engineering',
                'Aerospace Engineering',
                'Environmental Engineering',
                'Structural Engineering',
            ],
            'Remote Work': [
                'Remote Full-time',
                'Remote Part-time',
                'Remote Contract',
                'Remote Freelance',
                'Remote Internship',
            ],
        }

        # Create categories and subcategories
        categories_created = 0
        subcategories_created = 0

        for category_name, subcategories in job_categories.items():
            # Create or get the category
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                categories_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
            else:
                self.stdout.write(f'Category already exists: {category_name}')

            # Create subcategories
            for subcategory_name in subcategories:
                subcategory, created = SubCategory.objects.get_or_create(
                    name=subcategory_name,
                    category=category
                )
                if created:
                    subcategories_created += 1
                    self.stdout.write(self.style.SUCCESS(f'  - Created subcategory: {subcategory_name}'))
                else:
                    self.stdout.write(f'  - Subcategory already exists: {subcategory_name}')

        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {categories_created} categories and {subcategories_created} subcategories'
        ))