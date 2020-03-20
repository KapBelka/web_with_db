db_name = input()
global_init(db_name)
session = create_session()
users = session.query(User).filter(User.age < 18)
for user in users:
    print(user, user.age, "years")
