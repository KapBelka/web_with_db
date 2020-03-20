db_name = input()
global_init(db_name)
session = create_session()
users = session.query(User).filter(User.address == "module_1",
                                   User.speciality.notlike('%ingeneer%'),
                                   User.position.notlike('%ingeneer%'))
for user in users:
    print(user.id)