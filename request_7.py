db_name = input()
global_init(db_name)
session = create_session()
users = session.query(User).filter(User.address == "module_1", User.age < 21)
for user in users:
    user.address = "module_3"
