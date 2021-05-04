#!/usr/bin/env python
import pandas as pd
import sys

if len(sys.argv)!=5:
  print('[usage] python xlfilter.py <source_data.xlsx> <min_occurrences> <vs30min> <vs30max>')
  raise SystemExit

fn=sys.argv[1]
thresh=int(sys.argv[2])
vmin=float(sys.argv[3])
vmax=float(sys.argv[4])

df=pd.read_excel(fn)
rsn='Record Sequence Number'
ssn='Station Sequence Number'
sn='Station Name'
vs30='Vs30 (m/s) selected for analysis'
collst=[rsn,ssn,vs30]

vsdf=df[(df[vs30]>=vmin) & (df[vs30]<=vmax)]
subdf=vsdf.groupby(sn).filter(lambda x: len(x)>=thresh)
print(subdf[collst].to_csv(index=False,header=False))

