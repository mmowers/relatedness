from __future__ import division
import pandas as pd

df = pd.read_csv('ins/1997 DH1 RFLP data.csv')
homo = ['LL','UU']
hetero = ['LU']
accept_vals = homo + hetero + ['NA']

lines = df['ENT'].values.tolist()
df = df.drop('ENT',1)
df = df.fillna('NA')
dlist = df.values.tolist()

clean = True
for i, ls in enumerate(dlist):
    for j, el in enumerate(ls):
        if el not in accept_vals:
            clean = False
            print('Fix ' + str(lines[i]) + ' '+str(j)+'= '+str(el))

if clean == False:
    raise SystemExit
#make resulting list of lists
out = []

for i, line in enumerate(lines):
    other_lines = lines[i:]
    for o, other_line in enumerate(other_lines):
        j = i + o
        line_length = len(dlist[i])
        result = 0
        for k in range(line_length):
            if i == j:
                result += 1
            elif dlist[i][k] == 'NA' or dlist[j][k] == 'NA':
                result += 0.5
            elif dlist[i][k] in hetero and dlist[j][k] in homo:
                result += 0.75
            elif dlist[i][k] in homo and dlist[j][k] in hetero:
                result += 0.75
            elif dlist[i][k] == dlist[j][k]:
                result += 1
        out.append([line, other_line, result/line_length])
out_reflect = [[x[1],x[0],x[2]] for x in out]
out = out + out_reflect
df_out = pd.DataFrame(out, columns=['line','other_line','val'])
df_out = df_out.pivot_table(index='line', columns='other_line', values='val')
df_out.to_csv('outs/out.csv')