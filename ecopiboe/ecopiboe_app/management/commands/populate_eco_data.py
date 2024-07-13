# management/commands/populate_eco_data.py
from django.core.management.base import BaseCommand
from users.models import EcoFootprintCategory, EcoFootprintQuestion

class Command(BaseCommand):
    help = 'Populate eco footprint categories and questions'

    def handle(self, *args, **kwargs):
        categories_data = {
            'Energy': [
                "How many hours per day do you typically leave lights on when not in use?",
                "Do you use energy-efficient appliances (e.g., LED light bulbs, ENERGY STAR-rated appliances)?",
                "Do you use renewable energy sources (e.g., solar panels, wind turbines) to power your home?",
                "How often do you adjust your thermostat to conserve energy (e.g., lowering it in winter, raising it in summer)?"
            ],
            'Transportation': [
                "How do you primarily commute to work or school (e.g., car, public transit, walking, biking)?",
                "How often do you carpool or rideshare with others?",
                "Do you own or use a fuel-efficient vehicle?",
                "How often do you travel long distances by plane?"
            ],
            'Waste': [
                "Do you recycle paper, plastic, glass, and metal materials?",
                "Do you compost food waste and yard debris?",
                "How often do you use single-use plastics (e.g., plastic bags, disposable utensils, water bottles)?",
                "Do you participate in local recycling programs or waste reduction initiatives?"
            ],
            'Water': [
                "How long do you typically shower each day?",
                "Do you use water-efficient fixtures (e.g., low-flow showerheads, dual-flush toilets)?",
                "Do you collect rainwater for outdoor use (e.g., watering plants, washing cars)?",
                "How often do you run full loads of laundry and dishes to conserve water?"
            ],
            'Diet': [
                "How often do you consume meat and dairy products?",
                "Do you incorporate plant-based meals into your diet?",
                "How often do you eat locally grown and seasonal foods?",
                "Do you minimize food waste by planning meals, using leftovers, and avoiding over-purchasing groceries?"
            ]
        }

        for category_name, questions in categories_data.items():
            category, created = EcoFootprintCategory.objects.get_or_create(name=category_name)
            for question_text in questions:
                EcoFootprintQuestion.objects.get_or_create(category=category, question_text=question_text)

        self.stdout.write(self.style.SUCCESS('Successfully populated eco footprint categories and questions'))
