#!/usr/bin/env python3
"""Build fixed V108 Kingston heterogeneous graph tensors."""
import csv, json, os
from pathlib import Path
import numpy as np

ROOT=Path(os.environ.get("V109_ROOT",Path(__file__).parent))
SRC=ROOT/"source_artifacts"; MAP=ROOT/"graph_adapter"; OUT=MAP/"ibm_graph_tensors.npz"

def rows(path): return list(csv.DictReader(path.open(newline="",encoding="utf-8-sig")))

def main():
    cfg=rows(SRC/"config_summary.csv"); qubits=rows(SRC/"used_qubits.csv")
    couplers=rows(SRC/"used_edges.csv"); detectors=rows(SRC/"detector_nodes.csv")
    links=rows(MAP/"detector_measurement_physical_edges.csv")
    ids=[r["config_id"] for r in cfg]; assert ids==[f"{b}{r}_L{l}" for b in "XZ" for r in (3,5,7) for l in (0,1)]
    C,D,Q,F=len(ids),56,17,5
    incidence=np.zeros((C,D,Q),np.float32); adjacency=np.zeros((C,Q,Q),np.float32)
    qfeat=np.zeros((C,Q,F),np.float32); dcoord=np.zeros((C,D,4),np.float32)
    for ci,cid in enumerate(ids):
        qr=[r for r in qubits if r["config_id"]==cid]; assert len(qr)==Q
        physical=[int(r["physical_qubit"]) for r in qr]; p2l={p:i for i,p in enumerate(physical)}
        for qi,r in enumerate(qr):
            vals=[r["t1_seconds"],r["t2_seconds"],r["readout_error"],r["measurement_duration_seconds"]]
            qfeat[ci,qi,:4]=[float(x) if x else 0 for x in vals]; qfeat[ci,qi,4]=sum(x=="" for x in vals)
            adjacency[ci,qi,qi]=1
        for r in couplers:
            if r["config_id"]!=cid: continue
            a,b=int(r["physical_q0"]),int(r["physical_q1"])
            if a in p2l and b in p2l: adjacency[ci,p2l[a],p2l[b]]=1
        for r in detectors:
            if r["config_id"]!=cid: continue
            di=int(r["detector_id"]); dcoord[ci,di]=[float(r["x"]),float(r["y"]),float(r["t"]),1]
        for r in links:
            if r["config_id"]==cid: incidence[ci,int(r["detector_id"]),p2l[int(r["physical_qubit"])]]+=1
    incidence/=np.maximum(incidence.sum(2,keepdims=True),1)
    deg=adjacency.sum(2); adjacency=adjacency/np.sqrt(np.maximum(deg[:,:,None]*deg[:,None,:],1))
    for j in range(4):
        v=qfeat[:,:,j]; nz=v!=0; mean=v[nz].mean(); std=v[nz].std()+1e-8; qfeat[:,:,j]=np.where(nz,(v-mean)/std,0)
    for j in range(3):
        v=dcoord[:,:,j]; m=dcoord[:,:,3]>0; lo,hi=v[m].min(),v[m].max(); dcoord[:,:,j]=np.where(m,2*(v-lo)/(hi-lo+1e-8)-1,0)
    np.savez_compressed(OUT,incidence=incidence,adjacency=adjacency,qubit_features=qfeat,detector_coordinates=dcoord,config_ids=np.array(ids))
    report={"status":"validated","configurations":C,"max_detectors":D,"qubits_per_configuration":Q,
            "detector_qubit_nonzero_edges":int((incidence>0).sum()),"coupler_nonzero_edges":int((adjacency>0).sum()),"output":str(OUT)}
    (MAP/"tensor_validation.json").write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__=="__main__": main()

