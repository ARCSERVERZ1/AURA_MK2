
repo = {
    1:1,
    2:2,
    3:3
}

live = { 1:9 , 4:9 , 5:9 }


for r_alm , r_tm in repo.items():
    if r_alm in live:
        live[r_alm] = r_tm


print(live)