import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from core.models import User, Company, Customer, Interaction

class Command(BaseCommand):
    help = 'Poblar base de datos con datos masivos'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        self.stdout.write("Creando Usuarios...")
        users = [User(username=f'agent_{i}', email=f'agent{i}@test.com', is_staff=True) for i in range(3)]
        for u in users: u.set_password('123456')
        User.objects.bulk_create(users)
        users = list(User.objects.all())

        self.stdout.write("Creando Compañías...")
        companies = [Company(name=fake.company()) for _ in range(10)] # 10 compañías ejemplo
        Company.objects.bulk_create(companies)
        companies = list(Company.objects.all())

        self.stdout.write("Creando Clientes...")
        customers = []
        for _ in range(1000):
            customers.append(Customer(
                name=fake.name(),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=60),
                company=random.choice(companies),
                agent=random.choice(users)
            ))
        Customer.objects.bulk_create(customers)
        # Recuperamos IDs
        customers = list(Customer.objects.all())

        self.stdout.write("Creando 500k Interacciones (paciencia)...")
        interactions_batch = []
        interaction_types = ['Call', 'Email', 'SMS', 'Meeting']
        
        # Generamos 500 interacciones por cada uno de los 1000 clientes
        count = 0
        for customer in customers:
            for _ in range(500):
                interactions_batch.append(Interaction(
                    customer=customer,
                    type=random.choice(interaction_types),
                    date=timezone.now() - timedelta(days=random.randint(0, 365), minutes=random.randint(0, 1440))
                ))
                
            # Guardamos en lotes de 50k para no reventar la memoria RAM
            if len(interactions_batch) >= 50000:
                Interaction.objects.bulk_create(interactions_batch)
                interactions_batch = []
                self.stdout.write(f"   ...{count+1} clientes procesados")
            count += 1

        if interactions_batch:
            Interaction.objects.bulk_create(interactions_batch)

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada exitosamente!'))