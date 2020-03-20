db_name = input()
global_init(db_name)
session = create_session()
users = session.query(User).filter(User.position.like("%chief%") | User.position.like("%middle%"))
for user in users:
    print(user, user.position)