"""Affiche l'état des derniers posts Buffer (sans afficher la clé)."""
import json, sys, os
sys.path.insert(0, "bot")
from publish import gql
def typ(n):
    return gql("query($n:String!){__type(name:$n){fields{name args{name type{name kind ofType{name kind ofType{name}}}} type{name kind ofType{name kind ofType{name}}}}}}", {"n": n})["__type"]
q = typ("Query")
print("QUERY", [(f["name"], [a["name"] for a in f["args"]]) for f in q["fields"]])
for n in ("Post", "PostsInput", "PostsFiltersInput"):
    try:
        t = typ(n)
        print(n, [f["name"] for f in (t or {}).get("fields") or []])
    except Exception as e:
        print(n, "?", e)
