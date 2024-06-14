import re
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import House, Tenant, User, Payment

# Create tables
Base.metadata.create_all(bind=engine)

def register_user():
    username = input('Enter username: ')
    phone = input('Enter phone number: ')
    password = input('Enter password: ')

    with next(get_db()) as db:
        user = User(username=username, phone=phone, password=password, role='tenant')
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f'User {user.username} created with role {user.role} and ID {user.id}')

def login():
    username = input('Enter username: ')
    password = input('Enter password: ')

    with next(get_db()) as db:
        user = db.query(User).filter(User.username == username, User.password == password).first()
        if user:
            print(f'Logged in as {user.username} ({user.role})')
            return user
        else:
            print('Invalid credentials')
            return None

def view_my_info(user):
    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.phone == user.phone).first()
        if tenant:
            house = db.query(House).filter(House.id == tenant.house_id).first()
            if house:
                print(f"\nTenant Info\nName: {tenant.name}\nPhone: {tenant.phone}\nHouse Address: {house.address}\n")
                print(f"Expected Payments (in Ksh):\nRent: {house.rent}\nWater: {house.water}\nElectricity: {house.electricity}\nWiFi: {house.wifi}")

                # Display payment status
                payments = db.query(Payment).filter(Payment.tenant_id == tenant.id).all()
                print("\nPayment Status:")
                for payment in payments:
                    status = payment.status
                    if status == 'partial':
                        status += f" (Remaining: {payment.remaining_amount} Ksh)"
                    print(f"{payment.type.capitalize()}: {status}")
            else:
                print("No house assigned")
        else:
            print('Tenant not found')

def list_houses():
    with next(get_db()) as db:
        houses = db.query(House).all()
        for house in houses:
            print(f"House ID: {house.id}, Address: {house.address}")

def list_tenants():
    with next(get_db()) as db:
        tenants = db.query(Tenant).all()
        for tenant in tenants:
            house = db.query(House).filter(House.id == tenant.house_id).first()
            print(f"Tenant ID: {tenant.id}, Name: {tenant.name}, Phone: {tenant.phone}, House Address: {house.address if house else 'No house assigned'}")

def create_house(user):
    if user.role != 'caretaker':
        print('Permission denied: only caretakers can create houses.')
        return

    address = input('Enter house address: ')
    rent = float(input('Enter rent amount: '))
    water = float(input('Enter water amount: '))
    electricity = float(input('Enter electricity amount: '))
    wifi = float(input('Enter wifi amount: '))

    with next(get_db()) as db:
        house = House(address=address, rent=rent, water=water, electricity=electricity, wifi=wifi)
        db.add(house)
        db.commit()
        db.refresh(house)
        print(f'House {house.address} created with ID {house.id}')

def create_tenant(user):
    if user.role != 'caretaker':
        print('Permission denied: only caretakers can create tenants.')
        return

    name = input('Enter tenant name: ')
    phone = input('Enter tenant phone number: ')
    password = input('Enter tenant password: ')

    if not re.match("^[A-Za-z]+$", name):
        print("Error: Tenant name must contain only alphabetic characters.")
        return

    with next(get_db()) as db:
        tenant = Tenant(name=name, phone=phone, password=password)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        # Also create a corresponding user entry for the tenant
        user = User(username=name, phone=phone, password=password, role='tenant')
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f'Tenant {tenant.name} created with ID {tenant.id}')

def delete_house():
    house_id = int(input('Enter house ID to delete: '))
    with next(get_db()) as db:
        house = db.query(House).filter(House.id == house_id).first()
        if house:
            db.delete(house)
            db.commit()
            print(f'House ID {house_id} deleted')
        else:
            print('House not found')

def delete_tenant():
    tenant_id = int(input('Enter tenant ID to delete: '))
    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant:
            db.delete(tenant)
            db.commit()
            print(f'Tenant ID {tenant_id} deleted')
        else:
            print('Tenant not found')

def assign_house():
    tenant_id = int(input('Enter tenant ID: '))
    house_id = int(input('Enter house ID: '))
    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        house = db.query(House).filter(House.id == house_id).first()
        if tenant and house:
            tenant.house_id = house_id
            db.commit()
            print(f'Assigned House ID {house_id} to Tenant ID {tenant_id}')
        else:
            print('Invalid Tenant ID or House ID')

def list_empty_houses():
    with next(get_db()) as db:
        houses = db.query(House).outerjoin(Tenant).filter(Tenant.house_id == None).all()
        for house in houses:
            print(f"House ID: {house.id}, Address: {house.address}")

def make_payment(user):
    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.phone == user.phone).first()
        if tenant:
            house = db.query(House).filter(House.id == tenant.house_id).first()
            if house:
                payment_type_dict = {'1': 'rent', '2': 'water', '3': 'electricity', '4': 'wifi'}
                required_amount_dict = {'rent': house.rent, 'water': house.water, 'electricity': house.electricity, 'wifi': house.wifi}

                print(f"Payment Types:\n1. Rent (Required: {house.rent} Ksh)\n2. Water (Required: {house.water} Ksh)\n3. Electricity (Required: {house.electricity} Ksh)\n4. WiFi (Required: {house.wifi} Ksh)")
                payment_type = input("Enter payment type (1-4): ")
                payment_type = payment_type_dict.get(payment_type)

                if payment_type:
                    required_amount = required_amount_dict[payment_type]
                    amount = float(input(f"Enter amount for {payment_type} (Required: {required_amount} Ksh): "))
                    if amount != required_amount:
                        print("Error: Partial payments are not accepted.")
                        return

                    print("Payment Gateways:\n1. Mpesa\n2. Bank")
                    gateway = input("Choose payment gateway (1-2): ")
                    payment_code = input("Enter payment code: ")

                    # Create a new payment
                    payment = Payment(
                        tenant_id=tenant.id,
                        amount=amount,
                        type=payment_type,
                        status='processing',
                        remaining_amount=0,
                        payment_code=payment_code
                    )
                    db.add(payment)
                    db.commit()
                    db.refresh(payment)
                    print(f"Payment received: {payment.amount} Ksh for {payment.type}. Status: {payment.status}.")

                    # Forward payment details to caretaker and Telegram
                    forward_payment_to_caretaker(payment)
                    forward_payment_to_telegram(payment)
                else:
                    print("Invalid payment type.")
            else:
                print("No house assigned")
        else:
            print("Tenant not found")

def forward_payment_to_caretaker(payment):
    # Placeholder for sending payment details to the caretaker
    print(f"Payment of {payment.amount} for {payment.type} by tenant {payment.tenant_id} forwarded to caretaker.")

def forward_payment_to_telegram(payment):
    # Placeholder for sending payment details to a Telegram account
    print(f"Payment of {payment.amount} for {payment.type} by tenant {payment.tenant_id} forwarded to Telegram.")

def caretaker_menu(user):
    while True:
        print("\nCaretaker Menu:\n1. Create House\n2. Create Tenant\n3. List Houses\n4. List Tenants\n5. Delete House\n6. Delete Tenant\n7. Assign House to Tenant\n8. List Empty Houses\n9. View Pending Payments\n10. View All Payments\n11. Logout")
        choice = input("Enter choice (1-11): ")

        if choice == '1':
            create_house(user)
        elif choice == '2':
            create_tenant(user)
        elif choice == '3':
            list_houses()
        elif choice == '4':
            list_tenants()
        elif choice == '5':
            delete_house()
        elif choice == '6':
            delete_tenant()
        elif choice == '7':
            assign_house()
        elif choice == '8':
            list_empty_houses()
        elif choice == '9':
            view_pending_payments()
        elif choice == '10':
            view_all_payments()
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

def view_pending_payments():
    with next(get_db()) as db:
        payments = db.query(Payment).filter(Payment.status == 'processing').all()
        for payment in payments:
            print(f"Payment ID: {payment.id}, Tenant ID: {payment.tenant_id}, Amount: {payment.amount}, Type: {payment.type}, Status: {payment.status}")
            confirm = input("Confirm payment (y/n)? ")
            if confirm.lower() == 'y':
                payment.confirmed = True
                payment.status = 'paid'
                db.commit()
                print(f"Payment ID {payment.id} confirmed and marked as paid.")
            else:
                print(f"Payment ID {payment.id} remains unconfirmed.")

def view_all_payments():
    with next(get_db()) as db:
        payments = db.query(Payment).all()
        for payment in payments:
            print(f"Payment ID: {payment.id}, Tenant ID: {payment.tenant_id}, Amount: {payment.amount}, Type: {payment.type}, Status: {payment.status}")

def tenant_menu(user):
    while True:
        print("\nTenant Menu:\n1. View My Info\n2. Make Payment\n3. Logout")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            view_my_info(user)
        elif choice == '2':
            make_payment(user)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter choice (1-3): ")

        if choice == '1':
            register_user()
        elif choice == '2':
            user = login()
            if user:
                if user.role == 'tenant':
                    tenant_menu(user)
                elif user.role == 'caretaker':
                    caretaker_menu(user)
                else:
                    print("Invalid role.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
