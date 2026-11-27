"""Affiche l'état des derniers posts Buffer (sans afficher la clé)."""
import json, sys
sys.path.insert(0, "bot")
from publish import gql
def inp(n):
    t=gql("query($n:String!){__type(name:$n){inputFields{name type{name kind ofType{name kind ofType{name}}}}}}",{"n":n})["__type"]
    return [(f["name"],f["type"]["name"] or (f["type"]["ofType"] or {}).get("name")) for f in (t or {}).get("inputFields") or []]
q=gql('{__type(name:"Query"){fields{name args{name type{name kind ofType{name kind ofType{name}}}}}}}')["__type"]["fields"]
pa=[f for f in q if f["name"]=="posts"][0]["args"]
it=[a for a in pa if a["name"]=="input"][0]["type"];iname=it["name"] or it["ofType"]["name"] or it["ofType"]["ofType"]["name"]
print("POSTSINPUT",iname,inp(iname))
for n,_ in inp(iname):pass
for sub in [t for _,t in inp(iname) if t and t.endswith("Input")]:
    print("SUB",sub,inp(sub))
et=gql('{__type(name:"Post"){fields{name type{name kind ofType{name}}}}}')["__type"]["fields"]
print("ERRTYPE",[ (f["name"],f["type"]) for f in et if f["name"] in("error","status","channel")])
org=gql("{account{organizations{id}}}")["account"]["organizations"][0]["id"]
try:
    d=gql("query($i:%s!){posts(first:8,input:$i){edges{node{id channelService status dueAt sentAt externalLink error{message}}}}}"%iname,{"i":{"organizationId":org,"sort":[{"field":"dueAt","direction":"desc"}]}})
    print("POSTS",json.dumps(d,ensure_ascii=False)[:3000])
except Exception as e:print("ERRQ",str(e)[:800])
