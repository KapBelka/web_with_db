db_name = input()
selected_id = 1
need_work_time = 20
global_init(db_name)
session = create_session()
departament = session.query(Department).filter(Department.id == selected_id).first()
members = set(map(int, departament.members.split(', ')))
members.add(departament.chief)
for user_id in members:
    user_jobs = session.query(Jobs).filter((Jobs.team_leader == user_id) |
                                           (Jobs.collaborators.like(f"% {user_id}")) |
                                           (Jobs.collaborators.like(f"{user_id},%")) |
                                           (Jobs.collaborators.like(f"{user_id}")) |
                                           (Jobs.collaborators.like(f"% {user_id},%")))
    work_time = 0
    for job in user_jobs:
        if job.is_finished:
            work_time += job.work_size
    if work_time > need_work_time:
        user = session.query(User).filter(User.id == user_id).first()
        print(user.surname, user.name)
