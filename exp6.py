# ======================== CSV FILE: WHAT YOU HAVE TO DO ========================
# 1. In VS Code, create a NEW FILE in the SAME folder as this .py file.
# 2. Name it  exp6.csv
# 3. Copy the lines below into it (WITHOUT the '# ' at the start), save with Ctrl+S.
#
#    event_id,process_id,event_action,target_process
#    E1,P1,SEND,P2
#    E2,P3,LOCAL,-
#    E3,P2,RECV,P1
#    E4,P2,SEND,P3
#    E5,P1,LOCAL,-
#    E6,P3,RECV,P2
#
# RULES: event_action must be SEND, RECV or LOCAL (capitals).
#        Only use P1, P2, P3.
#        For RECV, target_process = who SENT the message.
#        For LOCAL, put - in target_process.
#        A RECV row must come AFTER its SEND row.
#
# 4. Change DOMAIN below to your chit's domain.   5. Run:  python exp6.py
# ===============================================================================

# VECTOR CLOCKS - every process keeps 3 counters [P1, P2, P3]
#   LOCAL : add 1 to my own counter
#   SEND  : add 1 to my own counter   (the message carries a copy of my list)
#   RECV  : at each position keep the bigger number, then add 1 to my own counter

import csv

DOMAIN = "TrustMesh: Blockchain-Enabled Trusted IoT Framework"   # change to your chit
FILE = "exp6.csv"

vc = {"P1": [0, 0, 0], "P2": [0, 0, 0], "P3": [0, 0, 0]}   # everyone starts at 0
pos = {"P1": 0, "P2": 1, "P3": 2}    # where each process sits in the list
msg = {}                             # list carried by each message, e.g. msg["P1->P2"]
events = []                          # every event with its list, for comparing later

print("=== Vector Clocks for", DOMAIN, "===")
print()

for row in csv.DictReader(open(FILE)):
    e = row["event_id"]
    p = row["process_id"]
    kind = row["event_action"]
    other = row["target_process"]
    me = pos[p]                      # my position: P1 -> 0, P2 -> 1, P3 -> 2

    if kind == "SEND":
        vc[p][me] = vc[p][me] + 1
        msg[p + "->" + other] = vc[p].copy()        # put a copy of my list on the message
        print(e, p, "sends to", other, "  ", vc[p])

    elif kind == "RECV":
        m = msg[other + "->" + p]                   # list carried by the message
        for i in range(3):                          # i = 0, 1, 2
            vc[p][i] = max(vc[p][i], m[i])          # keep the bigger number
        vc[p][me] = vc[p][me] + 1
        print(e, p, "receives from", other, "  msg =", m, "  ", vc[p])

    else:                                           # LOCAL
        vc[p][me] = vc[p][me] + 1
        print(e, p, "local event", "  ", vc[p])

    events.append([e, vc[p].copy()])


# is every number in a smaller or equal to the number in b?
def before(a, b):
    for i in range(3):
        if a[i] > b[i]:
            return False
    return True


print()
print("Comparing every pair of events:")
for i in range(len(events)):
    for j in range(i + 1, len(events)):
        e1 = events[i][0]
        v1 = events[i][1]
        e2 = events[j][0]
        v2 = events[j][1]

        if before(v1, v2):
            print(e1, "->", e2, "  Causally Preceding")
        elif before(v2, v1):
            print(e2, "->", e1, "  Causally Preceding")
        else:
            print(e1, "||", e2, "  Concurrent")