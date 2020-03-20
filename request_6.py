db_name = input()
global_init(db_name)
session = create_session()
jobs = session.query(Jobs).all()
max_team = max([len(job.collaborators.split(", ")) for job in jobs])
team_leaders = set()
for job in jobs:
    if len(job.collaborators.split()) == max_team:
        user = session.query(User).filter(User.id == job.team_leader).first()
        team_leaders.add(user.name + ' ' + user.surname)
print("\n".join(team_leaders))
