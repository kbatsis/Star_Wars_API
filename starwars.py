from requests_cache import CachedSession
import argparse


class StarWars:
    def __init__(self):
        self.session = CachedSession(cache_name="cache",backend="filesystem",
                                     serializer="yaml")
        
    def searchCharacter(self,character,worldInformation=False):
        response = self.session.get(
                      "https://www.swapi.tech/api/people/?name=%s"%(character))
        respJSON = response.json()
        if respJSON["result"] != []:
            characterInfo = respJSON["result"][0]["properties"]
            print("Name: ",characterInfo["name"])
            print("Height: ",characterInfo["height"])
            print("Mass: ", characterInfo["mass"])
            print("Birth Year: ",characterInfo["birth_year"])
            if(worldInformation):
                world = self.session.get(characterInfo["homeworld"])
                worldInfo = world.json()["result"]["properties"]
                print("\n\nHomeworld\n---------")
                print("Name: ",worldInfo["name"])
                print("Population",worldInfo["population"])
                yearCorr = float(worldInfo["orbital_period"])/365
                dayCorr = float(worldInfo["rotation_period"])/24
                print("On %s 1 year on Earth is %.2f years and 1 day %.2f days"
                      %(worldInfo["name"],yearCorr,dayCorr))
        else:
            print("The force is not strong within you.")
             
    def clearCache(self):
        self.session.cache.clear()
        print("Removed cache.")

def parseArgs():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    parser_a = subparsers.add_parser("search",help="Search for a character.")
    parser_a.add_argument("name",type=str,help="Character's name.")
    parser_a.add_argument("--world",action="store_true",help=
                          "Display information about the character's world.")
    parser_b = subparsers.add_parser("cache",help="Cache operations.")
    parser_b.add_argument("--clean",action="store_true",help=
                          "Clears the cache.")
    return parser.parse_args()
    
def main(): 
    args = parseArgs()
    
    sw = StarWars()
    if vars(args)["subparser_name"] == "search":
        if args.world:
            sw.searchCharacter(args.name,True)
        else:
            sw.searchCharacter(args.name)
    elif vars(args)["subparser_name"] == "cache":
        if args.clean:
            sw.clearCache()

if __name__ == "__main__":
    main()