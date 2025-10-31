import external_api
from models import TF2_Networks,db
from app import app, db

#+++++++++++++++++++++++++++++++++++++++++++++++++
#TO BE EXECUTED ONCE THROUGH DIGITAL OCEAN CONSOLE
#+++++++++++++++++++++++++++++++++++++++++++++++++
def scan_all_networks(startID, endID):
    for id in range(startID, endID):
        tf_network = external_api.getTitanfallNetwork(id)
        network_to_check = TF2_Networks.query.filter_by(id = id).first()
        if tf_network == None:
            print(f"{id} is a Private Network... Skipping....")
        elif network_to_check:
            print(f"{id} already exists in db skipping")
        else:
            newNetwork = TF2_Networks(
                id=tf_network.get("id"),
                name=tf_network.get("name"),
                motd=tf_network.get("motd"),
                clantag=tf_network.get('clantag'),
                category=tf_network.get("category"),
                type=tf_network.get("type"),
                visibility=tf_network.get("visibility"),
                regions=tf_network.get("regions"),
                languages=tf_network.get("languages"),
                utcHappyHourStart=tf_network.get("utcHappyHourStart"),
                happyHourStart=tf_network.get("happyHourStart"),
                creatorName=tf_network.get("creatorName"),
                creatorUID=tf_network.get("creatorUID"),
                kills=tf_network.get("kills"),
                wins=tf_network.get("wins"),
                xp=tf_network.get("xp"),
                memberCount=tf_network.get("memberCount")
            )
            
            db.session.add(newNetwork)
            db.session.commit()
            print(f"{id} should be added {tf_network.get('name')}")
            print(f"should be added {tf_network.get('clantag')}")

