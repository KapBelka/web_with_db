db_name = input()
global_init(db_name)
session = create_session()
jobs = session.query(Jobs).filter(Jobs.work_size < 20)
for job in jobs:
    if not job.is_finished:
        print(job)
