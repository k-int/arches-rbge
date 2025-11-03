from django.core.management.base import BaseCommand
from arches.app.models.tile import Tile
class Command(BaseCommand):
    """
    Command for repairing invalid resource instance data

    """
    def add_arguments(self, parser):
        parser.add_argument("operation", nargs="?")
    def handle(self, *args, **options):
        self.update_tiles()
    def update_tiles(self):
        ## testing data for Cyrus
        # nodeinfo = [{
        #         "nodegroup":"2174dd12-17d5-11eb-98cd-acde48001122",
        #         "cardname":"place",
        #         "node":"2174dd12-17d5-11eb-98cd-acde48001122"
        #     }]
        nodeinfo = [{
                    "nodegroup":"cdfc974a-4ee7-11e9-8676-001851d058ba",
                    "cardname":"people",
                    "node":"cdfc974a-4ee7-11e9-8676-001851d058ba"
                }, 
            ]
        for item in nodeinfo:
            nodegroupid = item["nodegroup"]
            nodeid = item["node"]
            tiles = Tile.objects.filter(nodegroup_id = nodegroupid)  
            for tile in tiles: # only operate on first tile
                val = tile.data
                try:
                    for file in val[nodeid]:
                       #print(file['url'])
                       listurl = str(file['url']).split('/')
                       new = "/files/uploadedfiles/"+listurl[-1]
                       file['url'] = new
                    print(val)
                    tile.data = val
                    tile.save()
                    print('updated tile:', tile.tileid)
                    print('updated resourceid:', tile.resourceinstance_id)
                except (KeyError, AttributeError, TypeError): #skip if the data is already a list or the nodeid is not on the tile
                    pass
