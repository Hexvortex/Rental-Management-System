from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, CallbackQueryHandler, Filters, ConversationHandler
import logging
from sqlalchemy.orm import sessionmaker
from database import engine, get_db, Base
from models import House, Tenant, User
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN = "7434751458:AAG8roUDGUEex8VIxO2jWmpUpVhmWRD8vsg"

# Create tables
Base.metadata.create_all(bind=engine)

# State definitions for ConversationHandler
REGISTER_USERNAME, REGISTER_PHONE, REGISTER_PASSWORD = range(3)
LOGIN_USERNAME, LOGIN_PASSWORD = range(3, 5)
CREATE_HOUSE = 5
CREATE_TENANT_NAME, CREATE_TENANT_PHONE, CREATE_TENANT_PASSWORD = range(6, 9)
DELETE_HOUSE_ID = 9
DELETE_TENANT_ID = 10
ASSIGN_HOUSE_TENANT_ID, ASSIGN_HOUSE = range(11, 13)
user_sessions = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the Rental Management System\n"

        "1. /login - Login\n"
        "2. /exit - Exit"
    )

def register(update: Update, context: CallbackContext):
    update.message.reply_text("Enter username:")
    return REGISTER_USERNAME

def register_username(update: Update, context: CallbackContext):
    context.user_data['register_username'] = update.message.text
    update.message.reply_text("Enter phone number:")
    return REGISTER_PHONE

def register_phone(update: Update, context: CallbackContext):
    context.user_data['register_phone'] = update.message.text
    update.message.reply_text("Enter password:")
    return REGISTER_PASSWORD

def register_password(update: Update, context: CallbackContext):
    username = context.user_data.get('register_username')
    phone = context.user_data.get('register_phone')
    password = update.message.text

    with next(get_db()) as db:
        user = User(username=username, phone=phone, password=password, role='tenant')
        db.add(user)
        db.commit()
        db.refresh(user)
        update.message.reply_text(f'User {user.username} created with role {user.role} and ID {user.id}')

    return ConversationHandler.END

def login(update: Update, context: CallbackContext):
    update.message.reply_text("Enter username:")
    return LOGIN_USERNAME

def login_username(update: Update, context: CallbackContext):
    context.user_data['login_username'] = update.message.text
    update.message.reply_text("Enter password:")
    return LOGIN_PASSWORD

def login_password(update: Update, context: CallbackContext):
    username = context.user_data.get('login_username')
    password = update.message.text

    with next(get_db()) as db:
        user = db.query(User).filter(User.username == username, User.password == password).first()
        if user:
            user_sessions[update.message.chat_id] = user
            update.message.reply_text(f'Logged in as {user.username} ({user.role})')
            if user.role == 'tenant':
                update.message.reply_text(
                    "\nTenant Menu\n"
                    "1. /view_my_info - View My Info\n"
                    "2.  /exit - Exit"
                )
                return ConversationHandler.END
            elif user.role == 'caretaker':
                update.message.reply_text(
                    "\nCaretaker Menu\n"
                    "1. /create_house - Create House\n"
                    "2. /create_tenant - Create Tenant\n"
                    "3. /list_houses - List Houses\n"
                    "4. /list_tenants - List Tenants\n"
                    "5. /delete_house - Delete House\n"
                    "6. /delete_tenant - Delete Tenant\n"
                    "7. /assign_house - Assign House to Tenant\n"
                    "8. /list_empty_houses - List Empty Houses\n"
                    "9. /logout - Logout"
                )
                return ConversationHandler.END
        else:
            update.message.reply_text('Invalid credentials')
            return ConversationHandler.END

def view_my_info(update: Update, context: CallbackContext):
    user = user_sessions.get(update.message.chat_id)
    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.phone == user.phone).first()
        if tenant:
            house = db.query(House).filter(House.id == tenant.house_id).first()
            update.message.reply_text(f"\nTenant Info\nName: {tenant.name}\nPhone: {tenant.phone}\nHouse Address: {house.address if house else 'No house assigned'}")
        else:
            update.message.reply_text('Tenant not found')

def list_houses(update: Update, context: CallbackContext):
    with next(get_db()) as db:
        houses = db.query(House).all()
        houses_list = "\n".join([f"House ID: {house.id}, Address: {house.address}" for house in houses])
        update.message.reply_text(houses_list)

def list_tenants(update: Update, context: CallbackContext):
    with next(get_db()) as db:
        tenants = db.query(Tenant).all()
    tenants_list = "\n\n".join([f"Tenant ID: {tenant.id}\nName: {tenant.name}\nPhone: {tenant.phone}\nHouse Address: {tenant.house_id if tenant.house_id else 'No house assigned'}" for tenant in tenants])
    update.message.reply_text(tenants_list)

def create_house(update: Update, context: CallbackContext):
    user = user_sessions.get(update.message.chat_id)
    if user.role != 'caretaker':
        update.message.reply_text('Permission denied: only caretakers can create houses.')
        return ConversationHandler.END

    update.message.reply_text("Enter house address:")
    return CREATE_HOUSE

def create_house_address(update: Update, context: CallbackContext):
    address = update.message.text
    with next(get_db()) as db:
        house = House(address=address)
        db.add(house)
        db.commit()
        db.refresh(house)
        update.message.reply_text(f'House {house.address} created with ID {house.id}')

    return ConversationHandler.END

def create_tenant(update: Update, context: CallbackContext):
    user = user_sessions.get(update.message.chat_id)
    if user.role != 'caretaker':
        update.message.reply_text('Permission denied: only caretakers can create tenants.')
        return ConversationHandler.END

    update.message.reply_text("Enter tenant name:")
    return CREATE_TENANT_NAME

def create_tenant_name(update: Update, context: CallbackContext):
    context.user_data['create_tenant_name'] = update.message.text
    update.message.reply_text("Enter tenant phone number:")
    return CREATE_TENANT_PHONE

def create_tenant_phone(update: Update, context: CallbackContext):
    context.user_data['create_tenant_phone'] = update.message.text
    update.message.reply_text("Enter tenant password:")
    return CREATE_TENANT_PASSWORD

def create_tenant_password(update: Update, context: CallbackContext):
    name = context.user_data.get('create_tenant_name')
    phone = context.user_data.get('create_tenant_phone')
    password = update.message.text

    if not re.match("^[A-Za-z]+$", name):
        update.message.reply_text("Error: Tenant name must contain only alphabetic characters.")
        return ConversationHandler.END

    with next(get_db()) as db:
        tenant = Tenant(name=name, phone=phone, password=password)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        update.message.reply_text(f'Tenant {tenant.name} created with ID {tenant.id}')

    return ConversationHandler.END

def delete_house(update: Update, context: CallbackContext):
    update.message.reply_text("Enter house ID to delete:")
    return DELETE_HOUSE_ID

def delete_house_confirm(update: Update, context: CallbackContext):
    house_id = int(update.message.text)
    with next(get_db()) as db:
        house = db.query(House).filter(House.id == house_id).first()
        if house:
            db.delete(house)
            db.commit()
            update.message.reply_text(f'House ID {house_id} deleted')
        else:
            update.message.reply_text('House not found')

    return ConversationHandler.END

def delete_tenant(update: Update, context: CallbackContext):
    update.message.reply_text("Enter tenant ID to delete:")
    return DELETE_TENANT_ID

def delete_tenant_confirm(update: Update, context: CallbackContext):
    tenant_id = int(update.message.text)
    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if tenant:
            db.delete(tenant)
            db.commit()
            update.message.reply_text(f'Tenant ID {tenant_id} deleted')
        else:
            update.message.reply_text('Tenant not found')

    return ConversationHandler.END

def assign_house(update: Update, context: CallbackContext):
    update.message.reply_text("Enter tenant ID:")
    return ASSIGN_HOUSE_TENANT_ID

def assign_house_tenant_id(update: Update, context: CallbackContext):
    context.user_data['assign_house_tenant_id'] = int(update.message.text)
    update.message.reply_text("Enter house ID:")
    return ASSIGN_HOUSE

def assign_house_confirm(update: Update, context: CallbackContext):
    tenant_id = context.user_data.get('assign_house_tenant_id')
    house_id = int(update.message.text)

    with next(get_db()) as db:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        house = db.query(House).filter(House.id == house_id).first()
        if tenant and house:
            tenant.house_id = house_id
            db.commit()
            update.message.reply_text(f'Assigned House ID {house_id} to Tenant ID {tenant_id}')
        else:
            update.message.reply_text('Invalid Tenant ID or House ID')

    return ConversationHandler.END

def list_empty_houses(update: Update, context: CallbackContext):
    with next(get_db()) as db:
        houses = db.query(House).outerjoin(Tenant).filter(Tenant.house_id == None).all()
        empty_houses_list = "\n".join([f"House ID: {house.id}, Address: {house.address}" for house in houses])
        update.message.reply_text(empty_houses_list)

def exit(update: Update, context: CallbackContext):
    update.message.reply_text("Goodbye!")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    register_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            REGISTER_USERNAME: [MessageHandler(Filters.text & ~Filters.command, register_username)],
            REGISTER_PHONE: [MessageHandler(Filters.text & ~Filters.command, register_phone)],
            REGISTER_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, register_password)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login)],
        states={
            LOGIN_USERNAME: [MessageHandler(Filters.text & ~Filters.command, login_username)],
            LOGIN_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, login_password)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    create_house_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_house', create_house)],
        states={
            CREATE_HOUSE: [MessageHandler(Filters.text & ~Filters.command, create_house_address)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    create_tenant_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('create_tenant', create_tenant)],
        states={
            CREATE_TENANT_NAME: [MessageHandler(Filters.text & ~Filters.command, create_tenant_name)],
            CREATE_TENANT_PHONE: [MessageHandler(Filters.text & ~Filters.command, create_tenant_phone)],
            CREATE_TENANT_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, create_tenant_password)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    delete_house_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_house', delete_house)],
        states={
            DELETE_HOUSE_ID: [MessageHandler(Filters.text & ~Filters.command, delete_house_confirm)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    delete_tenant_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delete_tenant', delete_tenant)],
        states={
            DELETE_TENANT_ID: [MessageHandler(Filters.text & ~Filters.command, delete_tenant_confirm)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    assign_house_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('assign_house', assign_house)],
        states={
            ASSIGN_HOUSE_TENANT_ID: [MessageHandler(Filters.text & ~Filters.command, assign_house_tenant_id)],
            ASSIGN_HOUSE: [MessageHandler(Filters.text & ~Filters.command, assign_house_confirm)]
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    dp.add_handler(register_conv_handler)
    dp.add_handler(login_conv_handler)
    dp.add_handler(create_house_conv_handler)
    dp.add_handler(create_tenant_conv_handler)
    dp.add_handler(delete_house_conv_handler)
    dp.add_handler(delete_tenant_conv_handler)
    dp.add_handler(assign_house_conv_handler)
    dp.add_handler(CommandHandler('view_my_info', view_my_info))
    dp.add_handler(CommandHandler('list_houses', list_houses))
    dp.add_handler(CommandHandler('list_tenants', list_tenants))
    dp.add_handler(CommandHandler('list_empty_houses', list_empty_houses))
    dp.add_handler(CommandHandler('exit', exit))
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
