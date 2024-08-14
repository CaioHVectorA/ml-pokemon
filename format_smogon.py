import json
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def convert_to_json(input_text: str) -> str:
    splitted = input_text.split("+----------------------------------------+")
    cleaned_splitted = []
    for i in range(0, len(splitted)):
        cleanned_item = splitted[i].strip().replace("|","").replace("\n", "").strip()
        if (cleanned_item != ""):
            cleaned_splitted.append(cleanned_item)
    INDEXED_POKEMON_NAME = 8
    dictionary = {}
    actual_pokemon = ""
    for i in range(0, len(cleaned_splitted)):
        if (i % INDEXED_POKEMON_NAME == 0 or i == 0):
            actual_pokemon = cleaned_splitted[i].strip()
            dictionary[actual_pokemon] = {}
        index_range = i % INDEXED_POKEMON_NAME # 7 check and counter / 0 name / 1 raw count, avg weight, viability ceiling / 2 abilities / 3 items / 4 spreads / 5 moves / 6 teammates / checks and counters
        if (index_range == 1):
            if (actual_pokemon == "" or actual_pokemon == None): continue
            if (not actual_pokemon in dictionary): dictionary[actual_pokemon] = {}
            separated = cleaned_splitted[i].split(":")
            dictionary[actual_pokemon]["raw_count"] = separated[1].split(" ")[1].strip()
            dictionary[actual_pokemon]["avg_weight"] = separated[1].split(" ")[1].strip()
            dictionary[actual_pokemon]["viability_ceiling"] = separated[3].split(" ")[1].strip()
        elif (index_range == 2):
            ## abilities
            separated: list[str] = cleaned_splitted[i].split("    ") # ['Abilities', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' Magic Guard 89.111%', '', '', '', '', '', '', '', '', '', '', ' Unaware 10.888%', '', '', '', '', '', '', '', '', '', '', '', '', ' Cute Charm', '0.000%']
            abilities = {}
            for j in range(1, len(separated)):
                if (separated[j] == ""): continue
                abilities_list = separated[j].split(" ")
                ability_name = " ".join(abilities_list[0:(abilities_list.__len__() - 1)]).strip()
                abilities[ability_name] = abilities_list[abilities_list.__len__() - 1]
            dictionary[actual_pokemon]["abilities"] = abilities        
            pass
        elif (index_range == 3):
            ## items
            separated: list[str] = cleaned_splitted[i].split("    ")
            items = {}
            for j in range(1, len(separated)):
                if (separated[j] == ""): continue
                items_list = separated[j].split(" ")
                item_name = " ".join(items_list[0:(items_list.__len__() - 1)]).strip()
                items[item_name] = items_list[items_list.__len__() - 1]
            dictionary[actual_pokemon]["items"] = items            
            pass
        elif (index_range == 4):
            ## spreads
            separated: list[str] = cleaned_splitted[i].split("    ")
            spreads = {}
            for j in range(1, len(separated)):
                if (separated[j] == ""): continue
                spread_list = separated[j].split(" ")
                cleaned: list[str] = []
                for k in range(0, len(spread_list)):
                    if (spread_list[k] != ""):
                        cleaned.append(spread_list[k])
                if (cleaned[0] == "Other"):
                    # spreads["other"] = cleaned[1]
                    continue
                splitted = cleaned[0].split(":")
                nature = splitted[0].strip()
                evs = splitted[1].strip()
                percentage = cleaned[1].strip()
                if (nature in spreads):
                    spreads[nature].append({"evs": evs, "percentage": percentage})
                else:
                    spreads[nature] = [{"evs": evs, "percentage": percentage}]
                # first_index = spread_list.index(":")
                # nature = spread_list[0].strip()
            dictionary[actual_pokemon]["spreads"] = spreads
            pass
        elif (index_range == 5):
            # same impl as items
            separated: list[str] = cleaned_splitted[i].split("    ")
            moves = {}
            for j in range(1, len(separated)):
                if (separated[j] == ""): continue
                moves_list = separated[j].split(" ")
                move_name = " ".join(moves_list[0:(moves_list.__len__() - 1)]).strip()
                moves[move_name] = moves_list[moves_list.__len__() - 1]
            dictionary[actual_pokemon]["moves"] = moves
            ## moves
            pass            
        elif (index_range == 6):
            # same impl as ability
            separated: list[str] = cleaned_splitted[i].split("    ")
            teammates = {}
            for j in range(1, len(separated)):
                if (separated[j] == ""): continue
                teammates_list = separated[j].split(" ")
                teammate_name = " ".join(teammates_list[0:(teammates_list.__len__() - 1)]).strip()
                teammates[teammate_name] = teammates_list[teammates_list.__len__() - 1]
            dictionary[actual_pokemon]["teammates"] = teammates
            ## teammates
            pass
        elif (index_range == 7):
            # same impl as ability
            separated: list[str] = cleaned_splitted[i].split("    ")
            checks_and_counters = {}
            for j in range(1, len(separated)):
                if (separated[j] == ""): continue
                splitted = separated[j].split(" ")
                for k in range(0, len(splitted)):
                    # print(splitted[k], is_float(splitted[k]))
                    if (is_float(splitted[k])):
                        checks_and_counters[splitted[k-1].strip()] = splitted[k].strip()
            dictionary[actual_pokemon]["checks_and_counters"] = checks_and_counters
    return json.dumps(dictionary)



input_text = """
 +----------------------------------------+ 
 | Landorus-Therian                       | 
 +----------------------------------------+ 
 | Raw count: 10332                       | 
 | Avg. weight: 0.0924672812432           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Intimidate 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 83.833%                      | 
 | Rocky Helmet  3.664%                   | 
 | Choice Scarf  2.947%                   | 
 | Normal Gem  2.266%                     | 
 | Focus Sash  1.488%                     | 
 | Soft Sand  1.464%                      | 
 | Other  4.337%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:252/0/4/0/252/0 15.100%        | 
 | Careful:252/0/0/0/240/16  6.641%       | 
 | Careful:248/0/8/0/252/0  5.445%        | 
 | Sassy:248/0/8/0/252/0  5.142%          | 
 | Jolly:0/252/0/0/4/252  5.010%          | 
 | Jolly:48/0/0/0/252/208  3.852%         | 
 | Other 58.810%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 96.789%                     | 
 | U-turn 86.899%                         | 
 | Toxic 50.841%                          | 
 | Defog 49.250%                          | 
 | Stealth Rock 47.152%                   | 
 | Knock Off 32.911%                      | 
 | Swords Dance 10.349%                   | 
 | Stone Edge  9.183%                     | 
 | Other 16.626%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Weavile 30.901%                        | 
 | Melmetal 29.096%                       | 
 | Dragapult 27.297%                      | 
 | Heatran 26.839%                        | 
 | Ferrothorn 23.470%                     | 
 | Tapu Lele 21.286%                      | 
 | Kartana 21.273%                        | 
 | Zapdos 19.945%                         | 
 | Blacephalon 19.102%                    | 
 | Urshifu-Rapid-Strike 17.762%           | 
 | Clefable 13.255%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Weavile 76.664 (94.42±4.44)            |
 |	 (27.5% KOed / 66.9% switched out)| 
 | Skarmory 61.562 (83.83±5.57)           |
 |	 (0.0% KOed / 83.8% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Clefable                               | 
 +----------------------------------------+ 
 | Raw count: 5669                        | 
 | Avg. weight: 0.14732289684             | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magic Guard 89.111%                    | 
 | Unaware 10.888%                        | 
 | Cute Charm  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 58.400%                      | 
 | Rocky Helmet 20.880%                   | 
 | Life Orb 11.617%                       | 
 | Sticky Barb  5.392%                    | 
 | Other  3.712%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 21.809%           | 
 | Calm:252/0/188/0/68/0  8.856%          | 
 | Sassy:252/0/188/0/68/0  7.728%         | 
 | Calm:252/0/200/0/56/0  7.078%          | 
 | Modest:248/0/0/252/0/8  6.696%         | 
 | Bold:252/0/252/0/0/4  4.698%           | 
 | Other 43.136%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Moonblast 98.594%                      | 
 | Soft-Boiled 97.021%                    | 
 | Knock Off 51.056%                      | 
 | Stealth Rock 47.047%                   | 
 | Calm Mind 29.614%                      | 
 | Thunder Wave 26.621%                   | 
 | Aromatherapy 10.769%                   | 
 | Thunder  9.309%                        | 
 | Flamethrower  6.302%                   | 
 | Wish  4.711%                           | 
 | Other 18.955%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tornadus-Therian 42.083%               | 
 | Heatran 40.225%                        | 
 | Gastrodon 39.534%                      | 
 | Skarmory 31.795%                       | 
 | Tapu Koko 28.831%                      | 
 | Dragonite 20.583%                      | 
 | Slowbro 17.319%                        | 
 | Dragapult 16.665%                      | 
 | Scizor 16.367%                         | 
 | Toxapex 16.018%                        | 
 | Zapdos 15.743%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Heatran 65.522 (81.86±4.09)            |
 |	 (11.8% KOed / 70.1% switched out)| 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Heatran                                | 
 +----------------------------------------+ 
 | Raw count: 5580                        | 
 | Avg. weight: 0.142283564775            | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Flash Fire 80.590%                     | 
 | Flame Body 19.410%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 72.563%                      | 
 | Air Balloon 24.271%                    | 
 | Other  3.167%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Sassy:248/0/0/0/232/28 17.198%         | 
 | Timid:0/0/0/252/4/252  9.246%          | 
 | Calm:252/0/0/0/128/128  8.207%         | 
 | Calm:252/0/0/0/252/4  7.406%           | 
 | Timid:184/0/0/96/4/224  5.136%         | 
 | Modest:4/0/0/252/0/252  3.929%         | 
 | Other 48.877%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earth Power 89.920%                    | 
 | Magma Storm 86.596%                    | 
 | Taunt 45.128%                          | 
 | Stealth Rock 44.133%                   | 
 | Protect 37.398%                        | 
 | Toxic 30.499%                          | 
 | Heavy Slam 24.347%                     | 
 | Eruption 11.504%                       | 
 | Will-O-Wisp  6.891%                    | 
 | Flash Cannon  6.818%                   | 
 | Other 16.767%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 42.315%                       | 
 | Tornadus-Therian 33.138%               | 
 | Landorus-Therian 32.289%               | 
 | Gastrodon 31.029%                      | 
 | Kartana 26.971%                        | 
 | Tapu Koko 24.648%                      | 
 | Dragapult 23.674%                      | 
 | Skarmory 23.352%                       | 
 | Rillaboom 22.637%                      | 
 | Zapdos 17.096%                         | 
 | Garchomp 16.024%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Garchomp 62.930 (86.08±5.79)           |
 |	 (15.1% KOed / 71.0% switched out)| 
 | Dragonite 60.305 (83.19±5.72)          |
 |	 (18.4% KOed / 64.8% switched out)| 
 | Urshifu-Rapid-Strike 50.945 (80.12±7.29) |
 |	 (15.5% KOed / 64.6% switched out)| 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tornadus-Therian                       | 
 +----------------------------------------+ 
 | Raw count: 3485                        | 
 | Avg. weight: 0.18159360589             | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 81.936%               | 
 | Assault Vest 14.613%                   | 
 | Other  3.452%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:252/0/56/0/32/168 22.827%        | 
 | Timid:252/0/88/0/0/168  6.952%         | 
 | Timid:80/0/0/252/0/176  5.662%         | 
 | Timid:248/0/92/0/0/168  5.654%         | 
 | Timid:248/0/96/0/0/164  5.478%         | 
 | Timid:88/0/0/244/0/176  3.598%         | 
 | Other 49.829%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Hurricane 79.301%                      | 
 | U-turn 76.216%                         | 
 | Knock Off 74.818%                      | 
 | Defog 62.593%                          | 
 | Heat Wave 28.498%                      | 
 | Nasty Plot 20.414%                     | 
 | Focus Blast 18.799%                    | 
 | Sludge Bomb 12.868%                    | 
 | Toxic 11.252%                          | 
 | Other 15.241%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 55.526%                       | 
 | Heatran 41.566%                        | 
 | Gastrodon 30.668%                      | 
 | Skarmory 29.185%                       | 
 | Melmetal 24.514%                       | 
 | Tapu Koko 23.353%                      | 
 | Garchomp 23.054%                       | 
 | Toxapex 20.182%                        | 
 | Hippowdon 17.508%                      | 
 | Landorus-Therian 17.426%               | 
 | Corviknight 15.665%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Clefable 59.667 (79.64±4.99)           |
 |	 (2.9% KOed / 76.8% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Dragapult                              | 
 +----------------------------------------+ 
 | Raw count: 9725                        | 
 | Avg. weight: 0.058872403271            | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Infiltrator 77.023%                    | 
 | Clear Body 22.698%                     | 
 | Cursed Body  0.279%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 65.848%                   | 
 | Choice Band 10.612%                    | 
 | Life Orb  6.605%                       | 
 | Heavy-Duty Boots  5.768%               | 
 | Dragon Fang  5.535%                    | 
 | Spell Tag  2.540%                      | 
 | Other  3.091%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 38.072%         | 
 | Timid:0/0/0/252/4/252 24.975%          | 
 | Adamant:0/252/0/0/4/252  8.715%        | 
 | Lonely:0/252/0/4/0/252  4.541%         | 
 | Timid:0/4/0/252/0/252  3.649%          | 
 | Hasty:0/100/0/248/0/160  3.303%        | 
 | Other 16.744%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | U-turn 78.567%                         | 
 | Draco Meteor 70.098%                   | 
 | Shadow Ball 66.624%                    | 
 | Flamethrower 53.013%                   | 
 | Dragon Darts 28.224%                   | 
 | Hex 26.557%                            | 
 | Phantom Force 22.071%                  | 
 | Dragon Dance 14.376%                   | 
 | Sucker Punch 12.758%                   | 
 | Fire Blast  6.958%                     | 
 | Thunder Wave  4.292%                   | 
 | Other 16.460%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 45.537%               | 
 | Heatran 32.826%                        | 
 | Melmetal 26.883%                       | 
 | Clefable 24.308%                       | 
 | Zapdos 22.685%                         | 
 | Tapu Lele 19.771%                      | 
 | Ferrothorn 19.250%                     | 
 | Garchomp 18.221%                       | 
 | Kartana 17.154%                        | 
 | Weavile 14.513%                        | 
 | Blacephalon 14.496%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Garchomp                               | 
 +----------------------------------------+ 
 | Raw count: 6246                        | 
 | Avg. weight: 0.0900703977225           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Rough Skin 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 70.868%                      | 
 | Life Orb 10.734%                       | 
 | Rocky Helmet  5.334%                   | 
 | Lum Berry  4.251%                      | 
 | Focus Sash  2.788%                     | 
 | Heavy-Duty Boots  2.075%               | 
 | Other  3.950%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 52.038%          | 
 | Careful:240/0/0/0/252/16  9.786%       | 
 | Jolly:116/152/0/0/0/240  4.220%        | 
 | Jolly:4/252/0/0/0/252  3.450%          | 
 | Jolly:112/144/0/0/0/252  3.372%        | 
 | Jolly:252/0/136/0/0/120  2.819%        | 
 | Other 24.315%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 99.596%                     | 
 | Swords Dance 71.043%                   | 
 | Scale Shot 67.371%                     | 
 | Fire Fang 40.020%                      | 
 | Stealth Rock 37.790%                   | 
 | Toxic 25.234%                          | 
 | Protect 14.559%                        | 
 | Stone Edge 14.236%                     | 
 | Aqua Tail  9.721%                      | 
 | Flamethrower  6.340%                   | 
 | Other 14.091%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tornadus-Therian 25.938%               | 
 | Ferrothorn 24.185%                     | 
 | Heatran 22.613%                        | 
 | Blacephalon 20.953%                    | 
 | Tapu Lele 18.659%                      | 
 | Dragapult 18.544%                      | 
 | Weavile 17.450%                        | 
 | Clefable 17.420%                       | 
 | Slowbro 16.011%                        | 
 | Melmetal 15.526%                       | 
 | Kartana 14.286%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Ferrothorn                             | 
 +----------------------------------------+ 
 | Raw count: 8564                        | 
 | Avg. weight: 0.0634539037817           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Iron Barbs 100.000%                    | 
 | Anticipation  0.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 74.206%                      | 
 | Rocky Helmet 20.663%                   | 
 | Eject Button  3.718%                   | 
 | Other  1.414%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/0/252/0/4/0 18.939%         | 
 | Sassy:252/0/4/0/252/0  9.746%          | 
 | Impish:248/0/252/0/8/0  7.981%         | 
 | Relaxed:252/0/252/0/4/0  6.529%        | 
 | Careful:248/0/136/0/124/0  3.941%      | 
 | Relaxed:248/0/252/0/8/0  3.319%        | 
 | Other 49.544%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Leech Seed 96.813%                     | 
 | Knock Off 62.880%                      | 
 | Stealth Rock 51.992%                   | 
 | Body Press 47.687%                     | 
 | Spikes 45.408%                         | 
 | Gyro Ball 33.740%                      | 
 | Power Whip 32.130%                     | 
 | Thunder Wave 10.519%                   | 
 | Other 18.832%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 41.251%               | 
 | Zapdos 28.236%                         | 
 | Tapu Lele 26.319%                      | 
 | Garchomp 25.037%                       | 
 | Tyranitar 23.672%                      | 
 | Clefable 20.478%                       | 
 | Dragapult 20.282%                      | 
 | Slowbro 19.763%                        | 
 | Excadrill 19.366%                      | 
 | Weavile 18.419%                        | 
 | Tornadus-Therian 16.350%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Heatran 58.080 (82.95±6.22)            |
 |	 (18.0% KOed / 64.9% switched out)| 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Weavile                                | 
 +----------------------------------------+ 
 | Raw count: 5195                        | 
 | Avg. weight: 0.096929725578            | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Pressure 86.148%                       | 
 | Pickpocket 13.852%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 38.701%               | 
 | Choice Band 37.401%                    | 
 | Life Orb 19.852%                       | 
 | Other  4.046%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 52.272%          | 
 | Adamant:0/252/0/0/4/252 39.103%        | 
 | Adamant:4/252/0/0/0/252  5.278%        | 
 | Other  3.346%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 99.138%                      | 
 | Ice Shard 96.806%                      | 
 | Triple Axel 90.492%                    | 
 | Swords Dance 55.802%                   | 
 | Beat Up 20.552%                        | 
 | Low Kick 17.064%                       | 
 | Icicle Crash 13.562%                   | 
 | Other  6.583%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 58.604%               | 
 | Zapdos 22.353%                         | 
 | Kartana 22.308%                        | 
 | Heatran 20.326%                        | 
 | Ferrothorn 19.875%                     | 
 | Garchomp 19.493%                       | 
 | Melmetal 18.987%                       | 
 | Mew 16.750%                            | 
 | Dragapult 16.500%                      | 
 | Corviknight 16.291%                    | 
 | Blacephalon 16.198%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Zapdos                                 | 
 +----------------------------------------+ 
 | Raw count: 5178                        | 
 | Avg. weight: 0.0969825964186           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Static 93.931%                         | 
 | Pressure  6.069%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 92.404%               | 
 | Choice Specs  6.725%                   | 
 | Other  0.871%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:248/0/228/0/0/32 12.159%          | 
 | Timid:248/0/220/0/0/40  8.669%         | 
 | Bold:248/0/244/0/0/16  8.146%          | 
 | Timid:0/0/0/252/4/252  7.574%          | 
 | Timid:4/0/0/252/0/252  6.263%          | 
 | Timid:0/0/120/136/0/252  5.124%        | 
 | Other 52.065%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 88.153%                          | 
 | Volt Switch 80.332%                    | 
 | Hurricane 72.829%                      | 
 | Defog 57.269%                          | 
 | Heat Wave 41.477%                      | 
 | Toxic 15.537%                          | 
 | Thunderbolt 13.194%                    | 
 | Discharge 10.619%                      | 
 | Weather Ball  5.795%                   | 
 | Other 14.795%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 37.938%               | 
 | Ferrothorn 30.557%                     | 
 | Melmetal 28.229%                       | 
 | Heatran 27.030%                        | 
 | Clefable 26.182%                       | 
 | Dragapult 25.865%                      | 
 | Urshifu-Rapid-Strike 23.816%           | 
 | Weavile 22.419%                        | 
 | Tapu Lele 21.489%                      | 
 | Kartana 17.915%                        | 
 | Toxapex 14.622%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Kartana                                | 
 +----------------------------------------+ 
 | Raw count: 5088                        | 
 | Avg. weight: 0.0956490258214           | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 55.209%                   | 
 | Protective Pads 23.515%                | 
 | Choice Band  9.195%                    | 
 | Life Orb  4.040%                       | 
 | Adrenaline Orb  3.912%                 | 
 | Other  4.130%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 71.326%          | 
 | Jolly:0/252/4/0/0/252 15.707%          | 
 | Timid:248/0/0/0/8/252  3.845%          | 
 | Jolly:4/252/0/0/0/252  2.937%          | 
 | Timid:252/0/0/0/0/252  2.378%          | 
 | Other  3.807%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Leaf Blade 99.736%                     | 
 | Knock Off 98.128%                      | 
 | Sacred Sword 95.623%                   | 
 | Smart Strike 59.584%                   | 
 | Swords Dance 35.333%                   | 
 | Other 11.596%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Heatran 43.993%                        | 
 | Landorus-Therian 41.746%               | 
 | Dragonite 24.177%                      | 
 | Weavile 23.082%                        | 
 | Rillaboom 22.686%                      | 
 | Dragapult 20.179%                      | 
 | Clefable 19.370%                       | 
 | Tapu Fini 18.759%                      | 
 | Zapdos 18.482%                         | 
 | Magnezone 17.684%                      | 
 | Garchomp 16.512%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Melmetal                               | 
 +----------------------------------------+ 
 | Raw count: 5471                        | 
 | Avg. weight: 0.0833263331883           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Iron Fist 100.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 56.604%                      | 
 | Choice Band 15.447%                    | 
 | Protective Pads 13.511%                | 
 | Assault Vest 12.366%                   | 
 | Other  2.072%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:40/252/0/0/104/112  7.693%     | 
 | Adamant:0/252/0/0/244/12  5.831%       | 
 | Adamant:32/252/0/0/0/224  5.088%       | 
 | Adamant:20/232/0/0/196/60  4.984%      | 
 | Careful:84/152/0/0/252/20  4.523%      | 
 | Adamant:252/252/0/0/4/0  4.521%        | 
 | Other 67.360%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Double Iron Bash 100.000%              | 
 | Earthquake 73.510%                     | 
 | Thunder Punch 46.871%                  | 
 | Toxic 46.041%                          | 
 | Protect 45.587%                        | 
 | Ice Punch 28.630%                      | 
 | Superpower 27.313%                     | 
 | Thunder Wave 13.975%                   | 
 | Other 18.072%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 60.997%               | 
 | Tornadus-Therian 34.055%               | 
 | Dragapult 33.784%                      | 
 | Zapdos 31.112%                         | 
 | Tapu Lele 22.036%                      | 
 | Weavile 20.988%                        | 
 | Urshifu-Rapid-Strike 19.386%           | 
 | Garchomp 19.171%                       | 
 | Clefable 16.609%                       | 
 | Rotom-Wash 13.187%                     | 
 | Kartana 12.499%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tapu Lele                              | 
 +----------------------------------------+ 
 | Raw count: 3785                        | 
 | Avg. weight: 0.109524005924            | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Psychic Surge 100.000%                 | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 54.300%                   | 
 | Choice Specs 29.023%                   | 
 | Life Orb  4.710%                       | 
 | Twisted Spoon  4.442%                  | 
 | Assault Vest  2.992%                   | 
 | Other  4.533%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 50.876%         | 
 | Timid:0/0/0/252/4/252 27.363%          | 
 | Modest:0/0/4/252/0/252  8.311%         | 
 | Modest:24/0/16/252/0/216  3.071%       | 
 | Modest:44/0/0/252/0/212  2.855%        | 
 | Modest:252/0/0/40/0/216  1.992%        | 
 | Other  5.533%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Moonblast 94.609%                      | 
 | Psyshock 92.172%                       | 
 | Focus Blast 60.457%                    | 
 | Psychic 43.055%                        | 
 | Thunderbolt 40.355%                    | 
 | Future Sight 39.407%                   | 
 | Thunder  7.050%                        | 
 | Calm Mind  6.284%                      | 
 | Other 16.612%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 49.050%               | 
 | Ferrothorn 34.506%                     | 
 | Dragapult 27.311%                      | 
 | Zapdos 26.034%                         | 
 | Garchomp 25.324%                       | 
 | Urshifu-Rapid-Strike 24.686%           | 
 | Melmetal 24.221%                       | 
 | Tornadus-Therian 18.296%               | 
 | Magnezone 16.741%                      | 
 | Rotom-Wash 15.022%                     | 
 | Kartana 14.276%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Dragonite                              | 
 +----------------------------------------+ 
 | Raw count: 3175                        | 
 | Avg. weight: 0.12161762087             | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Multiscale 93.162%                     | 
 | Inner Focus  6.838%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 84.983%               | 
 | Life Orb  6.523%                       | 
 | Leftovers  3.347%                      | 
 | Weakness Policy  3.116%                | 
 | Other  2.031%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:248/60/52/0/0/148 21.354%      | 
 | Relaxed:248/0/252/0/8/0 13.575%        | 
 | Adamant:0/252/0/0/4/252  9.210%        | 
 | Jolly:0/252/0/0/4/252  6.155%          | 
 | Sassy:248/0/124/0/136/0  5.936%        | 
 | Impish:248/0/252/0/8/0  4.471%         | 
 | Other 39.299%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 91.016%                     | 
 | Roost 80.603%                          | 
 | Dragon Dance 54.334%                   | 
 | Ice Punch 41.423%                      | 
 | Ice Beam 31.168%                       | 
 | Defog 21.329%                          | 
 | Heal Bell 19.326%                      | 
 | Dual Wingbeat 16.644%                  | 
 | Extreme Speed 15.787%                  | 
 | Thunder Wave  7.127%                   | 
 | Toxic  5.795%                          | 
 | Other 15.448%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 44.511%                       | 
 | Scizor 32.432%                         | 
 | Kartana 30.472%                        | 
 | Landorus-Therian 22.358%               | 
 | Heatran 21.544%                        | 
 | Nidoking 21.038%                       | 
 | Tapu Koko 20.472%                      | 
 | Umbreon 19.319%                        | 
 | Slowbro 18.216%                        | 
 | Magnezone 17.571%                      | 
 | Gastrodon 16.938%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Clefable 52.606 (81.87±7.32)           |
 |	 (6.0% KOed / 75.9% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Toxapex                                | 
 +----------------------------------------+ 
 | Raw count: 5249                        | 
 | Avg. weight: 0.0723408353773           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 99.827%                    | 
 | Merciless  0.173%                      | 
 | Limber  0.000%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Shed Shell 40.641%                     | 
 | Rocky Helmet 18.718%                   | 
 | Eject Button 17.341%                   | 
 | Black Sludge 16.883%                   | 
 | Payapa Berry  3.108%                   | 
 | Other  3.309%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 17.886%           | 
 | Calm:248/0/48/0/212/0  7.587%          | 
 | Impish:248/0/200/0/60/0  7.024%        | 
 | Relaxed:248/0/160/0/100/0  5.427%      | 
 | Impish:248/0/200/0/52/8  4.579%        | 
 | Impish:252/0/252/0/4/0  4.426%         | 
 | Other 53.070%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Recover 99.551%                        | 
 | Knock Off 68.414%                      | 
 | Haze 58.741%                           | 
 | Scald 51.757%                          | 
 | Toxic Spikes 49.862%                   | 
 | Toxic 43.276%                          | 
 | Light Screen 12.852%                   | 
 | Other 15.548%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 45.129%                    | 
 | Clefable 35.224%                       | 
 | Tornadus-Therian 33.637%               | 
 | Hippowdon 33.041%                      | 
 | Landorus-Therian 31.354%               | 
 | Zapdos 19.334%                         | 
 | Weavile 18.723%                        | 
 | Blissey 18.698%                        | 
 | Blacephalon 14.788%                    | 
 | Slowking-Galar 14.666%                 | 
 | Melmetal 13.742%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Melmetal 51.344 (81.38±7.51)           |
 |	 (9.0% KOed / 72.4% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tapu Koko                              | 
 +----------------------------------------+ 
 | Raw count: 3797                        | 
 | Avg. weight: 0.100391804961            | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Electric Surge 100.000%                | 
 | Telepathy  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 82.010%               | 
 | Choice Specs  8.269%                   | 
 | Terrain Extender  4.677%               | 
 | Leftovers  1.986%                      | 
 | Other  3.059%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 44.242%          | 
 | Timid:120/0/0/132/4/252 18.373%        | 
 | Timid:40/0/0/252/0/216 12.464%         | 
 | Timid:16/0/4/252/20/216 10.982%        | 
 | Timid:0/0/4/252/0/252  5.096%          | 
 | Timid:108/0/0/148/0/252  2.010%        | 
 | Other  6.832%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 87.038%                          | 
 | Dazzling Gleam 76.782%                 | 
 | Thunderbolt 69.582%                    | 
 | Toxic 46.440%                          | 
 | U-turn 44.463%                         | 
 | Volt Switch 42.999%                    | 
 | Calm Mind 16.232%                      | 
 | Other 16.464%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 63.190%                       | 
 | Skarmory 54.026%                       | 
 | Heatran 51.355%                        | 
 | Gastrodon 51.352%                      | 
 | Tornadus-Therian 38.791%               | 
 | Landorus-Therian 25.036%               | 
 | Dragonite 20.749%                      | 
 | Ferrothorn 13.814%                     | 
 | Scizor 13.131%                         | 
 | Dragapult 10.355%                      | 
 | Buzzwole 10.295%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Slowbro                                | 
 +----------------------------------------+ 
 | Raw count: 3497                        | 
 | Avg. weight: 0.104926604281            | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 99.998%                    | 
 | Oblivious  0.002%                      | 
 | Own Tempo  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Rocky Helmet 37.624%                   | 
 | Colbur Berry 26.959%                   | 
 | Heavy-Duty Boots 21.208%               | 
 | Leftovers  7.469%                      | 
 | Eject Button  3.157%                   | 
 | Other  3.583%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Relaxed:252/0/252/0/4/0 33.414%        | 
 | Sassy:248/0/8/0/252/0 16.618%          | 
 | Relaxed:248/0/252/0/8/0  8.794%        | 
 | Relaxed:252/0/96/0/160/0  6.863%       | 
 | Relaxed:252/0/252/4/0/0  3.574%        | 
 | Relaxed:248/0/252/8/0/0  3.154%        | 
 | Other 27.584%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Teleport 85.424%                       | 
 | Scald 78.375%                          | 
 | Future Sight 74.712%                   | 
 | Slack Off 67.884%                      | 
 | Body Press 28.173%                     | 
 | Flamethrower 24.058%                   | 
 | Trick Room 17.744%                     | 
 | Toxic 10.381%                          | 
 | Other 13.248%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 39.414%                       | 
 | Ferrothorn 29.266%                     | 
 | Landorus-Therian 25.921%               | 
 | Garchomp 24.544%                       | 
 | Nidoking 21.648%                       | 
 | Tornadus-Therian 21.325%               | 
 | Umbreon 21.187%                        | 
 | Scizor 19.170%                         | 
 | Dragonite 19.170%                      | 
 | Heatran 15.784%                        | 
 | Melmetal 15.100%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Corviknight                            | 
 +----------------------------------------+ 
 | Raw count: 4956                        | 
 | Avg. weight: 0.0736803177644           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Pressure 95.736%                       | 
 | Mirror Armor  4.256%                   | 
 | Unnerve  0.008%                        | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 49.627%                      | 
 | Rocky Helmet 41.087%                   | 
 | Shed Shell  7.261%                     | 
 | Other  2.024%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/0/168/0/88/0 17.281%        | 
 | Relaxed:248/0/252/0/8/0 13.422%        | 
 | Relaxed:252/0/252/0/4/0 10.609%        | 
 | Impish:252/0/252/0/4/0  7.225%         | 
 | Bold:248/0/252/0/8/0  6.236%           | 
 | Careful:252/0/4/0/252/0  4.865%        | 
 | Other 40.362%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 99.921%                          | 
 | Defog 91.309%                          | 
 | U-turn 71.912%                         | 
 | Body Press 68.485%                     | 
 | Brave Bird 30.407%                     | 
 | Iron Defense 12.141%                   | 
 | Bulk Up  9.180%                        | 
 | Other 16.645%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 46.928%                        | 
 | Clefable 33.614%                       | 
 | Tornadus-Therian 27.149%               | 
 | Landorus-Therian 25.007%               | 
 | Hippowdon 24.953%                      | 
 | Weavile 22.465%                        | 
 | Slowking-Galar 21.750%                 | 
 | Blacephalon 17.876%                    | 
 | Blissey 15.788%                        | 
 | Dragapult 15.744%                      | 
 | Garchomp 15.722%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Heatran 71.077 (92.14±5.27)            |
 |	 (8.0% KOed / 84.2% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Gastrodon                              | 
 +----------------------------------------+ 
 | Raw count: 1364                        | 
 | Avg. weight: 0.255980249444            | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Storm Drain 96.403%                    | 
 | Sticky Hold  3.597%                    | 
 | Sand Force  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 75.017%                      | 
 | Heavy-Duty Boots 24.795%               | 
 | Other  0.188%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:248/0/32/0/200/28 38.529%         | 
 | Calm:252/0/64/0/192/0 12.309%          | 
 | Calm:252/0/4/0/252/0 11.464%           | 
 | Calm:248/0/68/0/192/0  7.118%          | 
 | Calm:248/0/64/0/196/0  7.001%          | 
 | Careful:252/0/52/0/192/12  5.128%      | 
 | Other 18.451%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Recover 100.000%                       | 
 | Scald 99.647%                          | 
 | Toxic 81.670%                          | 
 | Clear Smog 62.903%                     | 
 | Earth Power 25.696%                    | 
 | Protect 16.169%                        | 
 | Other 13.915%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 94.548%                       | 
 | Heatran 70.544%                        | 
 | Skarmory 67.951%                       | 
 | Tapu Koko 56.033%                      | 
 | Tornadus-Therian 55.587%               | 
 | Dragonite 18.732%                      | 
 | Zapdos 14.964%                         | 
 | Rillaboom 14.857%                      | 
 | Scizor 14.565%                         | 
 | Corviknight 12.606%                    | 
 | Kartana 12.170%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Suicune 66.726 (90.85±6.03)            |
 |	 (0.0% KOed / 90.8% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Blacephalon                            | 
 +----------------------------------------+ 
 | Raw count: 2940                        | 
 | Avg. weight: 0.1084812477              | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 63.859%                   | 
 | Choice Specs 29.348%                   | 
 | Focus Sash  5.270%                     | 
 | Other  1.523%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 68.712%          | 
 | Modest:0/0/0/252/4/252 23.729%         | 
 | Hasty:0/4/0/252/0/252  3.172%          | 
 | Other  4.387%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shadow Ball 99.988%                    | 
 | Flamethrower 99.555%                   | 
 | Trick 90.191%                          | 
 | Overheat 40.216%                       | 
 | Taunt 30.523%                          | 
 | Mind Blown 15.658%                     | 
 | Psychic  9.830%                        | 
 | Other 14.038%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 57.217%               | 
 | Garchomp 36.967%                       | 
 | Dragapult 26.029%                      | 
 | Weavile 25.583%                        | 
 | Heatran 20.873%                        | 
 | Corviknight 20.474%                    | 
 | Zapdos 19.034%                         | 
 | Toxapex 17.612%                        | 
 | Urshifu-Rapid-Strike 16.224%           | 
 | Celesteela 13.228%                     | 
 | Mew 13.129%                            | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Rillaboom                              | 
 +----------------------------------------+ 
 | Raw count: 5057                        | 
 | Avg. weight: 0.0582108719601           | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Grassy Surge 99.994%                   | 
 | Overgrow  0.006%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 29.421%                       | 
 | Choice Band 23.181%                    | 
 | Leftovers 19.339%                      | 
 | Terrain Extender 18.385%               | 
 | Coba Berry  5.293%                     | 
 | Other  4.381%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 21.398%        | 
 | Adamant:252/252/4/0/0/0 14.365%        | 
 | Adamant:0/252/0/0/4/252 14.268%        | 
 | Adamant:240/252/0/0/0/16 10.755%       | 
 | Jolly:0/252/0/0/4/252  7.725%          | 
 | Adamant:64/252/0/0/0/192  5.572%       | 
 | Other 25.918%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Grassy Glide 99.905%                   | 
 | Knock Off 85.828%                      | 
 | Swords Dance 71.840%                   | 
 | Superpower 70.482%                     | 
 | Wood Hammer 28.149%                    | 
 | U-turn 24.505%                         | 
 | Other 19.291%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Heatran 61.041%                        | 
 | Kartana 37.505%                        | 
 | Clefable 28.995%                       | 
 | Landorus-Therian 24.400%               | 
 | Zapdos 24.030%                         | 
 | Garchomp 21.071%                       | 
 | Tornadus-Therian 20.680%               | 
 | Dragapult 18.716%                      | 
 | Gastrodon 17.622%                      | 
 | Slowbro 17.335%                        | 
 | Melmetal 16.387%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Skarmory                               | 
 +----------------------------------------+ 
 | Raw count: 1847                        | 
 | Avg. weight: 0.156017168143            | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sturdy 96.222%                         | 
 | Keen Eye  3.751%                       | 
 | Weak Armor  0.028%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Rocky Helmet 95.991%                   | 
 | Other  4.009%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 63.419%           | 
 | Bold:248/0/252/0/0/8 13.858%           | 
 | Impish:248/0/252/0/8/0  6.943%         | 
 | Bold:252/0/252/0/0/4  4.803%           | 
 | Impish:248/0/248/0/0/12  3.049%        | 
 | Impish:252/0/252/0/4/0  2.734%         | 
 | Other  5.195%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 99.206%                          | 
 | Spikes 99.180%                         | 
 | Body Press 98.898%                     | 
 | Iron Defense 72.555%                   | 
 | Toxic 24.692%                          | 
 | Other  5.469%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 92.133%                       | 
 | Gastrodon 82.334%                      | 
 | Tapu Koko 71.429%                      | 
 | Heatran 64.326%                        | 
 | Tornadus-Therian 64.094%               | 
 | Dragonite 21.646%                      | 
 | Scizor 18.203%                         | 
 | Dragapult 13.832%                      | 
 | Hippowdon  8.881%                      | 
 | Toxapex  8.383%                        | 
 | Rotom-Wash  3.663%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Urshifu-Rapid-Strike                   | 
 +----------------------------------------+ 
 | Raw count: 4770                        | 
 | Avg. weight: 0.0583682071492           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Unseen Fist 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 53.015%                    | 
 | Protective Pads 29.902%                | 
 | Choice Scarf 11.004%                   | 
 | Lum Berry  4.584%                      | 
 | Other  1.494%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 49.232%          | 
 | Jolly:0/252/4/0/0/252 31.222%          | 
 | Adamant:0/252/0/0/4/252  6.405%        | 
 | Jolly:4/252/0/0/0/252  4.970%          | 
 | Jolly:16/252/0/0/0/240  4.584%         | 
 | Other  3.588%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Surging Strikes 99.997%                | 
 | Close Combat 95.113%                   | 
 | U-turn 86.646%                         | 
 | Aqua Jet 73.873%                       | 
 | Ice Punch 19.676%                      | 
 | Taunt  6.662%                          | 
 | Other 18.033%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 60.937%               | 
 | Zapdos 42.958%                         | 
 | Tapu Lele 36.755%                      | 
 | Melmetal 31.726%                       | 
 | Dragapult 26.139%                      | 
 | Ferrothorn 25.412%                     | 
 | Heatran 23.169%                        | 
 | Blacephalon 18.583%                    | 
 | Weavile 14.976%                        | 
 | Kartana 14.764%                        | 
 | Garchomp 13.342%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tapu Fini                              | 
 +----------------------------------------+ 
 | Raw count: 2521                        | 
 | Avg. weight: 0.0944859086104           | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Misty Surge 100.000%                   | 
 | Telepathy  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 57.627%                      | 
 | Expert Belt 27.262%                    | 
 | Choice Scarf 12.051%                   | 
 | Other  3.060%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/4/252/0/252 27.262%         | 
 | Bold:252/0/116/0/0/140 17.134%         | 
 | Calm:248/0/40/0/156/64  4.085%         | 
 | Calm:252/0/216/0/40/0  3.805%          | 
 | Calm:248/0/120/0/72/68  3.757%         | 
 | Timid:0/0/0/252/4/252  3.602%          | 
 | Other 40.355%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Moonblast 63.794%                      | 
 | Taunt 49.620%                          | 
 | Scald 36.489%                          | 
 | Calm Mind 33.212%                      | 
 | Draining Kiss 32.943%                  | 
 | Hydro Pump 30.069%                     | 
 | Knock Off 29.813%                      | 
 | Ice Beam 29.019%                       | 
 | Nature's Madness 22.873%               | 
 | Surf 19.724%                           | 
 | Defog 13.875%                          | 
 | Trick 12.063%                          | 
 | Whirlpool 11.671%                      | 
 | Other 14.835%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 49.386%               | 
 | Heatran 47.595%                        | 
 | Kartana 38.326%                        | 
 | Magnezone 37.001%                      | 
 | Dragonite 26.832%                      | 
 | Mamoswine 25.656%                      | 
 | Garchomp 21.380%                       | 
 | Melmetal 20.674%                       | 
 | Zapdos 20.249%                         | 
 | Weavile 18.132%                        | 
 | Zeraora 17.996%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Magnezone                              | 
 +----------------------------------------+ 
 | Raw count: 1658                        | 
 | Avg. weight: 0.123656437206            | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magnet Pull 96.830%                    | 
 | Sturdy  3.168%                         | 
 | Analytic  0.002%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Air Balloon 50.409%                    | 
 | Leftovers 26.263%                      | 
 | Rocky Helmet 13.237%                   | 
 | Choice Specs  4.483%                   | 
 | Chople Berry  3.789%                   | 
 | Other  1.818%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:0/0/252/116/0/140 31.673%         | 
 | Modest:160/0/252/0/0/96  8.418%        | 
 | Timid:4/0/252/0/0/252  6.949%          | 
 | Bold:0/0/252/80/0/176  6.585%          | 
 | Bold:152/0/252/0/0/104  6.423%         | 
 | Timid:0/0/252/72/0/184  5.845%         | 
 | Other 34.108%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Body Press 93.725%                     | 
 | Iron Defense 93.450%                   | 
 | Thunderbolt 84.028%                    | 
 | Flash Cannon 38.340%                   | 
 | Magnet Rise 33.166%                    | 
 | Discharge 15.543%                      | 
 | Substitute 12.792%                     | 
 | Toxic  8.784%                          | 
 | Volt Switch  7.230%                    | 
 | Other 12.942%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Fini 42.988%                      | 
 | Kartana 41.977%                        | 
 | Tapu Lele 33.840%                      | 
 | Dragonite 33.093%                      | 
 | Mamoswine 31.394%                      | 
 | Heatran 30.921%                        | 
 | Landorus-Therian 29.615%               | 
 | Melmetal 19.610%                       | 
 | Tornadus-Therian 16.562%               | 
 | Garchomp 13.161%                       | 
 | Shuckle 11.601%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mew                                    | 
 +----------------------------------------+ 
 | Raw count: 2550                        | 
 | Avg. weight: 0.0774122917922           | 
 | Viability Ceiling: 90                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Synchronize 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 22.514%                     | 
 | Colbur Berry 18.839%                   | 
 | Leftovers 16.493%                      | 
 | Weakness Policy 14.147%                | 
 | Kasib Berry  8.305%                    | 
 | Expert Belt  5.867%                    | 
 | Rocky Helmet  3.224%                   | 
 | Lum Berry  3.193%                      | 
 | Mental Herb  3.110%                    | 
 | Other  4.308%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:252/4/0/0/0/252 14.672%          | 
 | Jolly:252/0/4/0/0/252 13.056%          | 
 | Timid:252/0/0/0/4/252 12.391%          | 
 | Timid:252/0/0/4/0/252  9.892%          | 
 | Timid:252/0/4/0/0/252  9.401%          | 
 | Timid:0/0/0/252/4/252  9.064%          | 
 | Other 31.523%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Taunt 63.493%                          | 
 | Spikes 49.155%                         | 
 | Stealth Rock 46.051%                   | 
 | Thunder Wave 32.769%                   | 
 | Stored Power 21.657%                   | 
 | Cosmic Power 21.657%                   | 
 | Roost 21.232%                          | 
 | Volt Switch 12.115%                    | 
 | Close Combat 11.868%                   | 
 | Psychic Fangs 11.824%                  | 
 | Dragon Dance 10.654%                   | 
 | Triple Axel  9.657%                    | 
 | Body Press  7.684%                     | 
 | Nasty Plot  6.670%                     | 
 | Rest  6.665%                           | 
 | Psyshock  6.587%                       | 
 | Shadow Ball  6.464%                    | 
 | Vacuum Wave  6.464%                    | 
 | Knock Off  5.889%                      | 
 | Soft-Boiled  4.873%                    | 
 | Will-O-Wisp  4.498%                    | 
 | Heal Bell  4.090%                      | 
 | Explosion  2.997%                      | 
 | Aura Sphere  2.826%                    | 
 | Trick  2.810%                          | 
 | Other 19.350%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Weavile 42.728%                        | 
 | Garchomp 38.340%                       | 
 | Volcarona 34.592%                      | 
 | Celesteela 22.773%                     | 
 | Kartana 21.824%                        | 
 | Blacephalon 21.205%                    | 
 | Dragonite 20.509%                      | 
 | Bisharp 17.661%                        | 
 | Landorus-Therian 15.572%               | 
 | Polteageist 12.375%                    | 
 | Zapdos-Galar 11.574%                   | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Hippowdon                              | 
 +----------------------------------------+ 
 | Raw count: 1587                        | 
 | Avg. weight: 0.12443222081             | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sand Stream 96.454%                    | 
 | Sand Force  3.546%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 84.574%                      | 
 | Smooth Rock  6.452%                    | 
 | Rocky Helmet  4.570%                   | 
 | Other  4.404%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:252/8/0/0/248/0 31.139%        | 
 | Careful:248/0/8/0/252/0 24.087%        | 
 | Careful:248/0/0/0/252/8  8.976%        | 
 | Careful:252/0/4/0/252/0  7.456%        | 
 | Careful:252/4/0/0/252/0  6.879%        | 
 | Careful:252/0/0/0/252/4  5.495%        | 
 | Other 15.968%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Slack Off 100.000%                     | 
 | Earthquake 99.599%                     | 
 | Stealth Rock 99.423%                   | 
 | Toxic 92.625%                          | 
 | Other  8.353%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 63.533%                        | 
 | Clefable 59.858%                       | 
 | Tornadus-Therian 56.107%               | 
 | Corviknight 46.143%                    | 
 | Slowbro 21.555%                        | 
 | Zapdos 21.164%                         | 
 | Kartana 16.917%                        | 
 | Melmetal 14.078%                       | 
 | Slowking 13.377%                       | 
 | Skarmory 12.960%                       | 
 | Heatran 12.806%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Scizor                                 | 
 +----------------------------------------+ 
 | Raw count: 1851                        | 
 | Avg. weight: 0.100012221788            | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Technician 99.997%                     | 
 | Swarm  0.003%                          | 
 | Light Metal  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 41.207%               | 
 | Protective Pads 38.742%                | 
 | Leftovers 13.096%                      | 
 | Rocky Helmet  2.566%                   | 
 | Other  4.388%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:248/0/8/0/252/0 50.232%        | 
 | Careful:248/8/0/0/252/0 21.572%        | 
 | Adamant:88/252/4/0/0/164  8.467%       | 
 | Impish:248/0/172/0/88/0  5.274%        | 
 | Careful:248/12/100/0/148/0  4.861%     | 
 | Adamant:100/252/4/0/0/152  1.801%      | 
 | Other  7.793%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Bullet Punch 99.963%                   | 
 | Roost 96.683%                          | 
 | Swords Dance 89.161%                   | 
 | Knock Off 64.607%                      | 
 | U-turn 39.887%                         | 
 | Other  9.700%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 73.827%                       | 
 | Dragonite 67.648%                      | 
 | Nidoking 40.390%                       | 
 | Umbreon 40.296%                        | 
 | Slowbro 37.997%                        | 
 | Skarmory 28.335%                       | 
 | Gastrodon 27.470%                      | 
 | Tapu Koko 27.025%                      | 
 | Garchomp 18.401%                       | 
 | Tornadus-Therian 13.671%               | 
 | Dragapult 12.147%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Rotom-Wash                             | 
 +----------------------------------------+ 
 | Raw count: 2327                        | 
 | Avg. weight: 0.0761030369975           | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 89.553%                      | 
 | Choice Scarf  6.285%                   | 
 | Other  4.162%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:248/0/8/0/252/0 19.292%           | 
 | Calm:252/0/0/0/128/128 10.083%         | 
 | Calm:252/0/0/0/168/88  9.194%          | 
 | Timid:248/0/0/12/0/248  8.758%         | 
 | Bold:252/0/252/0/4/0  8.588%           | 
 | Modest:136/0/0/124/0/248  7.848%       | 
 | Other 36.238%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Hydro Pump 99.952%                     | 
 | Pain Split 97.422%                     | 
 | Volt Switch 91.360%                    | 
 | Will-O-Wisp 27.462%                    | 
 | Toxic 26.077%                          | 
 | Defog 18.508%                          | 
 | Thunder Wave 15.372%                   | 
 | Nasty Plot  8.651%                     | 
 | Other 15.195%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 57.693%               | 
 | Clefable 45.363%                       | 
 | Ferrothorn 43.058%                     | 
 | Dragapult 42.067%                      | 
 | Tornadus-Therian 37.017%               | 
 | Tapu Lele 35.185%                      | 
 | Melmetal 33.952%                       | 
 | Tyranitar 18.811%                      | 
 | Weavile 18.152%                        | 
 | Kartana 16.880%                        | 
 | Garchomp 14.385%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tyranitar                              | 
 +----------------------------------------+ 
 | Raw count: 3264                        | 
 | Avg. weight: 0.0517978244011           | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sand Stream 99.985%                    | 
 | Unnerve  0.015%                        | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 52.600%                    | 
 | Leftovers 32.448%                      | 
 | Smooth Rock 10.752%                    | 
 | Other  4.200%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 31.930%        | 
 | Careful:252/0/4/0/252/0 12.399%        | 
 | Sassy:252/0/80/0/176/0 12.206%         | 
 | Adamant:0/252/4/0/0/252  9.859%        | 
 | Adamant:252/252/0/0/4/0  9.436%        | 
 | Adamant:168/252/0/0/0/88  7.218%       | 
 | Other 16.951%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Stone Edge 77.823%                     | 
 | Crunch 48.776%                         | 
 | Stealth Rock 40.464%                   | 
 | Ice Punch 32.432%                      | 
 | Earthquake 31.988%                     | 
 | Superpower 29.844%                     | 
 | Fire Punch 23.273%                     | 
 | Thunder Wave 23.111%                   | 
 | Rock Blast 19.887%                     | 
 | Heavy Slam 19.212%                     | 
 | Ice Beam 15.722%                       | 
 | Dragon Dance  9.860%                   | 
 | Aerial Ace  8.310%                     | 
 | Other 19.298%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 76.100%                     | 
 | Excadrill 71.405%                      | 
 | Zapdos 36.047%                         | 
 | Tapu Lele 32.038%                      | 
 | Slowbro 22.960%                        | 
 | Urshifu-Rapid-Strike 21.893%           | 
 | Rotom-Wash 19.692%                     | 
 | Clefable 18.152%                       | 
 | Dragapult 18.094%                      | 
 | Toxapex 17.117%                        | 
 | Dracozolt 15.642%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Volcarona                              | 
 +----------------------------------------+ 
 | Raw count: 3601                        | 
 | Avg. weight: 0.0471079292347           | 
 | Viability Ceiling: 95                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Flame Body 81.459%                     | 
 | Swarm 18.541%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 61.279%               | 
 | Leftovers 33.118%                      | 
 | Lum Berry  5.097%                      | 
 | Other  0.506%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 18.284%          | 
 | Bold:248/0/252/0/8/0 14.546%           | 
 | Modest:0/0/68/252/0/188 13.687%        | 
 | Modest:96/0/0/252/4/156  7.677%        | 
 | Bold:248/0/208/0/0/52  7.117%          | 
 | Modest:0/0/0/252/4/252  4.635%         | 
 | Other 34.053%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Quiver Dance 99.535%                   | 
 | Flamethrower 55.657%                   | 
 | Bug Buzz 43.749%                       | 
 | Roost 41.539%                          | 
 | Psychic 39.053%                        | 
 | Giga Drain 34.124%                     | 
 | Fiery Dance 32.525%                    | 
 | Safeguard 22.243%                      | 
 | Substitute 21.201%                     | 
 | Other 10.373%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mew 40.254%                            | 
 | Weavile 35.782%                        | 
 | Dragonite 25.427%                      | 
 | Garchomp 22.859%                       | 
 | Landorus-Therian 19.591%               | 
 | Kartana 18.773%                        | 
 | Suicune 18.353%                        | 
 | Cresselia 18.242%                      | 
 | Cloyster 17.791%                       | 
 | Registeel 17.754%                      | 
 | Victini 17.700%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Blissey                                | 
 +----------------------------------------+ 
 | Raw count: 3392                        | 
 | Avg. weight: 0.0500566440503           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Natural Cure 99.862%                   | 
 | Serene Grace  0.130%                   | 
 | Healer  0.009%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 69.828%               | 
 | Leftovers 29.044%                      | 
 | Other  1.128%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 81.804%           | 
 | Bold:252/0/252/0/0/4  8.430%           | 
 | Bold:216/0/252/0/40/0  3.169%          | 
 | Bold:252/0/224/0/32/0  1.861%          | 
 | Other  4.736%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Soft-Boiled 98.698%                    | 
 | Seismic Toss 96.647%                   | 
 | Toxic 47.615%                          | 
 | Teleport 46.420%                       | 
 | Stealth Rock 41.853%                   | 
 | Aromatherapy 32.559%                   | 
 | Thunder Wave 21.699%                   | 
 | Other 14.509%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 41.829%                        | 
 | Corviknight 33.964%                    | 
 | Landorus-Therian 32.673%               | 
 | Ferrothorn 29.592%                     | 
 | Slowbro 23.287%                        | 
 | Clefable 21.428%                       | 
 | Zapdos 18.003%                         | 
 | Buzzwole 17.643%                       | 
 | Tornadus-Therian 16.949%               | 
 | Weavile 16.795%                        | 
 | Quagsire 14.880%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Excadrill                              | 
 +----------------------------------------+ 
 | Raw count: 2581                        | 
 | Avg. weight: 0.062232019876            | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sand Rush 74.827%                      | 
 | Mold Breaker 18.684%                   | 
 | Sand Force  6.490%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 38.005%                      | 
 | Focus Sash 20.866%                     | 
 | Choice Band 13.461%                    | 
 | Assault Vest 13.077%                   | 
 | Choice Scarf  6.491%                   | 
 | Air Balloon  5.374%                    | 
 | Other  2.726%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 44.871%        | 
 | Jolly:0/252/0/0/4/252 36.426%          | 
 | Adamant:4/252/0/0/0/252  9.250%        | 
 | Jolly:0/252/4/0/0/252  2.898%          | 
 | Jolly:32/224/0/0/0/252  1.796%         | 
 | Other  4.760%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 99.950%                     | 
 | Iron Head 96.132%                      | 
 | Rapid Spin 88.129%                     | 
 | Swords Dance 51.649%                   | 
 | Rock Slide 44.715%                     | 
 | Other 19.425%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tyranitar 75.138%                      | 
 | Ferrothorn 65.511%                     | 
 | Zapdos 37.107%                         | 
 | Slowbro 24.657%                        | 
 | Tapu Lele 23.453%                      | 
 | Clefable 23.201%                       | 
 | Urshifu-Rapid-Strike 20.793%           | 
 | Toxapex 18.764%                        | 
 | Dragapult 17.058%                      | 
 | Dracozolt 16.013%                      | 
 | Hippowdon 14.152%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Buzzwole                               | 
 +----------------------------------------+ 
 | Raw count: 2257                        | 
 | Avg. weight: 0.0719087588836           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Rocky Helmet 47.022%                   | 
 | Heavy-Duty Boots 17.933%               | 
 | Choice Band 13.368%                    | 
 | Leftovers  9.081%                      | 
 | Salac Berry  6.513%                    | 
 | Choice Scarf  3.883%                   | 
 | Other  2.200%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:248/28/120/0/0/112 24.409%     | 
 | Jolly:0/252/0/0/4/252  9.500%          | 
 | Adamant:200/68/200/0/12/28  9.056%     | 
 | Adamant:152/168/0/0/0/188  7.868%      | 
 | Jolly:16/144/108/0/0/240  4.625%       | 
 | Jolly:4/252/0/0/0/252  4.013%          | 
 | Other 40.528%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Ice Punch 91.054%                      | 
 | Close Combat 84.085%                   | 
 | Roost 74.015%                          | 
 | Earthquake 42.223%                     | 
 | Leech Life 34.076%                     | 
 | Toxic 16.184%                          | 
 | Substitute  9.062%                     | 
 | Focus Punch  9.056%                    | 
 | Drain Punch  6.855%                    | 
 | Fell Stinger  6.525%                   | 
 | Endure  6.492%                         | 
 | Dual Wingbeat  5.395%                  | 
 | Other 14.978%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 43.859%               | 
 | Melmetal 25.031%                       | 
 | Tapu Koko 24.177%                      | 
 | Dragapult 23.302%                      | 
 | Heatran 21.209%                        | 
 | Weavile 20.575%                        | 
 | Corviknight 20.492%                    | 
 | Clefable 18.663%                       | 
 | Blissey 18.461%                        | 
 | Slowbro 17.327%                        | 
 | Ferrothorn 15.510%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Nidoking                               | 
 +----------------------------------------+ 
 | Raw count: 1407                        | 
 | Avg. weight: 0.100786387359            | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sheer Force 99.999%                    | 
 | Poison Point  0.001%                   | 
 | Rivalry  0.000%                        | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 53.557%                     | 
 | Life Orb 46.269%                       | 
 | Other  0.173%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 60.588%         | 
 | Timid:0/0/0/252/4/252 25.918%          | 
 | Rash:0/4/0/252/0/252  5.341%           | 
 | Naive:0/0/0/252/0/252  4.988%          | 
 | Other  3.165%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Ice Beam 99.660%                       | 
 | Earth Power 97.333%                    | 
 | Sludge Wave 88.081%                    | 
 | Stealth Rock 55.775%                   | 
 | Flamethrower 31.999%                   | 
 | Rock Slide 11.025%                     | 
 | Other 16.127%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragonite 57.326%                      | 
 | Slowbro 56.055%                        | 
 | Clefable 54.935%                       | 
 | Scizor 52.765%                         | 
 | Umbreon 52.642%                        | 
 | Dragapult 15.605%                      | 
 | Ferrothorn 15.389%                     | 
 | Buzzwole 14.242%                       | 
 | Tyranitar 14.055%                      | 
 | Weavile 12.653%                        | 
 | Rotom-Wash 12.297%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Slowking-Galar                         | 
 +----------------------------------------+ 
 | Raw count: 1707                        | 
 | Avg. weight: 0.0735418977848           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 99.999%                    | 
 | Curious Medicine  0.001%               | 
 | Own Tempo  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 88.627%                   | 
 | Black Sludge  8.100%                   | 
 | Other  3.274%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:248/0/44/88/128/0 22.950%       | 
 | Modest:248/0/12/204/44/0 10.652%       | 
 | Calm:248/0/12/144/60/44  9.416%        | 
 | Modest:252/0/16/240/0/0  9.369%        | 
 | Calm:252/0/12/124/120/0  8.429%        | 
 | Sassy:252/0/12/124/120/0  4.681%       | 
 | Other 34.501%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Sludge Bomb 95.598%                    | 
 | Flamethrower 90.412%                   | 
 | Future Sight 88.187%                   | 
 | Scald 62.996%                          | 
 | Ice Beam 20.224%                       | 
 | Earthquake  8.791%                     | 
 | Nasty Plot  7.182%                     | 
 | Psyshock  5.394%                       | 
 | Psychic  5.265%                        | 
 | Other 15.949%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 63.268%                    | 
 | Weavile 46.112%                        | 
 | Landorus-Therian 45.391%               | 
 | Toxapex 44.362%                        | 
 | Blacephalon 31.138%                    | 
 | Clefable 30.534%                       | 
 | Garchomp 24.846%                       | 
 | Blissey 17.692%                        | 
 | Urshifu-Rapid-Strike 16.646%           | 
 | Ferrothorn 14.776%                     | 
 | Gastrodon 14.613%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 | Gastrodon 69.536 (90.13±5.15)          |
 |	 (4.6% KOed / 85.6% switched out) | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Hatterene                              | 
 +----------------------------------------+ 
 | Raw count: 1324                        | 
 | Avg. weight: 0.0932557986897           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magic Bounce 100.000%                  | 
 | Healer  0.000%                         | 
 | Anticipation  0.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Kasib Berry 41.196%                    | 
 | Leftovers 39.302%                      | 
 | Eject Button 11.733%                   | 
 | Focus Sash  6.945%                     | 
 | Other  0.825%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:252/0/92/0/164/0 41.196%          | 
 | Bold:252/0/196/0/0/60  9.976%          | 
 | Modest:252/0/248/8/0/0  8.849%         | 
 | Bold:252/0/252/0/4/0  7.080%           | 
 | Bold:252/0/204/0/0/52  5.186%          | 
 | Modest:252/0/4/252/0/0  4.812%         | 
 | Other 22.902%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Mystical Fire 80.617%                  | 
 | Draining Kiss 71.532%                  | 
 | Healing Wish 60.556%                   | 
 | Trick Room 57.005%                     | 
 | Future Sight 28.994%                   | 
 | Nuzzle 24.861%                         | 
 | Calm Mind 22.063%                      | 
 | Dazzling Gleam 13.475%                 | 
 | Psyshock 12.861%                       | 
 | Misty Explosion  9.270%                | 
 | Other 18.766%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 55.204%                     | 
 | Garchomp 49.793%                       | 
 | Marowak-Alola 45.911%                  | 
 | Slowbro 39.944%                        | 
 | Drampa 39.790%                         | 
 | Melmetal 27.021%                       | 
 | Landorus-Therian 24.925%               | 
 | Toxapex 22.573%                        | 
 | Chansey 12.633%                        | 
 | Buzzwole 11.446%                       | 
 | Hydreigon 10.462%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Ninetales-Alola                        | 
 +----------------------------------------+ 
 | Raw count: 2409                        | 
 | Avg. weight: 0.0441149895776           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Snow Warning 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Icy Rock 62.129%                       | 
 | Light Clay 28.422%                     | 
 | Choice Scarf  9.084%                   | 
 | Other  0.365%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 46.624%          | 
 | Timid:248/0/8/0/0/252 20.378%          | 
 | Timid:248/0/0/0/8/252  8.316%          | 
 | Timid:252/0/56/0/0/200  8.110%         | 
 | Timid:248/0/0/8/0/252  6.518%          | 
 | Timid:252/0/0/4/0/252  3.248%          | 
 | Other  6.806%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Aurora Veil 87.918%                    | 
 | Encore 86.384%                         | 
 | Freeze-Dry 74.777%                     | 
 | Moonblast 54.351%                      | 
 | Blizzard 36.660%                       | 
 | Hypnosis 34.282%                       | 
 | Heal Bell  8.940%                      | 
 | Other 16.690%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Arctozolt 77.906%                      | 
 | Dragapult 36.050%                      | 
 | Garchomp 32.924%                       | 
 | Heatran 32.793%                        | 
 | Cloyster 26.871%                       | 
 | Landorus-Therian 24.881%               | 
 | Aurorus 19.247%                        | 
 | Eiscue 19.022%                         | 
 | Scizor 18.953%                         | 
 | Sandslash-Alola 18.334%                | 
 | Corviknight 17.737%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Celesteela                             | 
 +----------------------------------------+ 
 | Raw count: 1145                        | 
 | Avg. weight: 0.0910985494387           | 
 | Viability Ceiling: 90                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Power Herb 81.826%                     | 
 | Occa Berry 10.149%                     | 
 | Leftovers  6.691%                      | 
 | Other  1.335%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 41.532%         | 
 | Modest:0/0/4/252/0/252 13.960%         | 
 | Modest:40/0/0/252/0/216 13.611%        | 
 | Timid:0/0/0/252/4/252 12.935%          | 
 | Adamant:0/252/0/0/4/252 10.149%        | 
 | Modest:4/0/0/252/0/252  3.199%         | 
 | Other  4.615%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Autotomize 92.536%                     | 
 | Flamethrower 86.593%                   | 
 | Air Slash 85.555%                      | 
 | Meteor Beam 81.826%                    | 
 | Heavy Slam 12.928%                     | 
 | Earthquake 11.311%                     | 
 | Acrobatics 10.149%                     | 
 | Other 19.102%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Garchomp 70.349%                       | 
 | Mew 43.098%                            | 
 | Blacephalon 40.434%                    | 
 | Weavile 30.861%                        | 
 | Azumarill 17.363%                      | 
 | Rillaboom 16.764%                      | 
 | Heatran 16.213%                        | 
 | Tapu Koko 16.172%                      | 
 | Dragapult 14.651%                      | 
 | Urshifu-Rapid-Strike 13.221%           | 
 | Xurkitree 12.416%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Bisharp                                | 
 +----------------------------------------+ 
 | Raw count: 1829                        | 
 | Avg. weight: 0.0573312579065           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Defiant 98.979%                        | 
 | Pressure  1.019%                       | 
 | Inner Focus  0.002%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Black Glasses 32.898%                  | 
 | Choice Band 30.752%                    | 
 | Focus Sash 20.320%                     | 
 | Leftovers  9.053%                      | 
 | Life Orb  6.457%                       | 
 | Other  0.520%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 48.802%        | 
 | Adamant:4/252/0/0/0/252 27.771%        | 
 | Jolly:0/252/4/0/0/252  8.968%          | 
 | Adamant:248/252/0/0/8/0  5.398%        | 
 | Jolly:0/252/0/0/4/252  4.277%          | 
 | Other  4.785%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 99.623%                      | 
 | Iron Head 98.889%                      | 
 | Sucker Punch 85.511%                   | 
 | Swords Dance 48.506%                   | 
 | Beat Up 26.595%                        | 
 | Stealth Rock 20.478%                   | 
 | Thunder Wave 11.355%                   | 
 | Other  9.043%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 40.086%                      | 
 | Zapdos-Galar 37.287%                   | 
 | Mew 33.266%                            | 
 | Landorus-Therian 27.948%               | 
 | Zapdos 27.583%                         | 
 | Volcarona 26.024%                      | 
 | Garchomp 25.681%                       | 
 | Blacephalon 25.567%                    | 
 | Weavile 24.622%                        | 
 | Polteageist 23.270%                    | 
 | Dragonite 22.703%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Zeraora                                | 
 +----------------------------------------+ 
 | Raw count: 2460                        | 
 | Avg. weight: 0.0399692655075           | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Volt Absorb 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 71.970%               | 
 | Leftovers 18.487%                      | 
 | Life Orb  5.499%                       | 
 | Other  4.044%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 73.669%          | 
 | Jolly:0/252/4/0/0/252 21.756%          | 
 | Other  4.575%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Plasma Fists 99.901%                   | 
 | Knock Off 89.462%                      | 
 | Close Combat 76.909%                   | 
 | Bulk Up 59.562%                        | 
 | Toxic 22.266%                          | 
 | Volt Switch 15.326%                    | 
 | Blaze Kick 10.996%                     | 
 | Drain Punch 10.192%                    | 
 | Other 15.387%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 55.364%               | 
 | Heatran 45.999%                        | 
 | Tapu Fini 43.598%                      | 
 | Garchomp 26.876%                       | 
 | Kartana 20.989%                        | 
 | Melmetal 19.555%                       | 
 | Rillaboom 18.446%                      | 
 | Dragapult 16.249%                      | 
 | Corviknight 15.869%                    | 
 | Porygon2 13.457%                       | 
 | Tornadus-Therian 13.248%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Blaziken                               | 
 +----------------------------------------+ 
 | Raw count: 2383                        | 
 | Avg. weight: 0.0421181767716           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Speed Boost 99.038%                    | 
 | Blaze  0.962%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 60.097%                      | 
 | Life Orb 14.742%                       | 
 | Air Balloon 12.971%                    | 
 | Protective Pads  9.477%                | 
 | Other  2.713%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:144/252/0/0/0/112 24.867%      | 
 | Adamant:4/252/0/0/0/252 22.486%        | 
 | Adamant:0/252/0/0/4/252 20.217%        | 
 | Jolly:0/252/0/0/4/252 12.798%          | 
 | Adamant:0/252/4/0/0/252  9.732%        | 
 | Adamant:72/252/0/0/0/184  2.768%       | 
 | Other  7.132%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Flare Blitz 98.371%                    | 
 | Swords Dance 95.340%                   | 
 | Close Combat 86.474%                   | 
 | Protect 66.146%                        | 
 | Thunder Punch 19.550%                  | 
 | High Jump Kick 13.439%                 | 
 | Earthquake 13.006%                     | 
 | Other  7.674%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 42.823%                      | 
 | Garchomp 32.519%                       | 
 | Aegislash 29.789%                      | 
 | Dragapult 25.954%                      | 
 | Melmetal 22.890%                       | 
 | Slowbro 20.736%                        | 
 | Tornadus-Therian 20.361%               | 
 | Mew 17.349%                            | 
 | Kartana 16.195%                        | 
 | Tapu Lele 15.731%                      | 
 | Landorus-Therian 14.432%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Slowking                               | 
 +----------------------------------------+ 
 | Raw count: 800                         | 
 | Avg. weight: 0.119036655866            | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 100.000%                   | 
 | Oblivious  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 45.871%               | 
 | Assault Vest 43.989%                   | 
 | Eject Button  4.738%                   | 
 | Shed Shell  3.688%                     | 
 | Other  1.714%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Sassy:252/0/4/0/252/0 26.616%          | 
 | Modest:252/0/4/252/0/0 23.908%         | 
 | Sassy:252/0/0/0/252/0 11.451%          | 
 | Sassy:252/0/160/0/96/0 10.282%         | 
 | Sassy:248/0/160/0/100/0  7.746%        | 
 | Modest:248/0/0/252/8/0  4.099%         | 
 | Other 15.898%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 95.700%                          | 
 | Future Sight 94.823%                   | 
 | Slack Off 54.990%                      | 
 | Teleport 52.914%                       | 
 | Flamethrower 43.615%                   | 
 | Dragon Tail 35.410%                    | 
 | Earthquake 12.832%                     | 
 | Other  9.716%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 54.491%                    | 
 | Tornadus-Therian 54.464%               | 
 | Toxapex 43.990%                        | 
 | Clefable 36.465%                       | 
 | Hippowdon 27.739%                      | 
 | Buzzwole 23.916%                       | 
 | Landorus-Therian 21.880%               | 
 | Garchomp 16.672%                       | 
 | Melmetal 14.228%                       | 
 | Blissey 13.554%                        | 
 | Ferrothorn 12.937%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Volcanion                              | 
 +----------------------------------------+ 
 | Raw count: 1250                        | 
 | Avg. weight: 0.0762105970808           | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Water Absorb 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 57.333%                   | 
 | Heavy-Duty Boots 36.667%               | 
 | Life Orb  2.475%                       | 
 | Other  3.526%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 38.557%         | 
 | Timid:0/0/0/252/4/252 31.660%          | 
 | Modest:0/0/4/252/0/252  6.075%         | 
 | Modest:72/0/0/252/0/184  4.081%        | 
 | Modest:252/0/0/252/4/0  3.208%         | 
 | Modest:248/0/0/252/8/0  3.186%         | 
 | Other 13.232%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Steam Eruption 99.996%                 | 
 | Earth Power 99.465%                    | 
 | Flamethrower 96.750%                   | 
 | Sludge Wave 44.982%                    | 
 | Sludge Bomb 19.832%                    | 
 | Toxic 14.724%                          | 
 | Defog 12.540%                          | 
 | Other 11.712%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 76.582%               | 
 | Weavile 59.299%                        | 
 | Kartana 37.335%                        | 
 | Zapdos 37.301%                         | 
 | Melmetal 34.480%                       | 
 | Dragonite 21.595%                      | 
 | Ferrothorn 21.519%                     | 
 | Dragapult 15.682%                      | 
 | Tornadus-Therian 14.200%               | 
 | Regieleki 11.027%                      | 
 | Tapu Lele 10.719%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Umbreon                                | 
 +----------------------------------------+ 
 | Raw count: 562                         | 
 | Avg. weight: 0.165917813217            | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Synchronize 93.091%                    | 
 | Inner Focus  6.909%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 100.000%                     | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 66.983%           | 
 | Bold:248/0/252/0/8/0 15.822%           | 
 | Calm:252/0/176/0/80/0 12.942%          | 
 | Other  4.253%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Foul Play 99.994%                      | 
 | Protect 99.993%                        | 
 | Wish 99.991%                           | 
 | Heal Bell 98.324%                      | 
 | Other  1.698%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Slowbro 83.374%                        | 
 | Scizor 80.001%                         | 
 | Clefable 80.000%                       | 
 | Dragonite 80.000%                      | 
 | Nidoking 80.000%                       | 
 | Landorus-Therian 12.419%               | 
 | Nihilego 11.610%                       | 
 | Blastoise  8.128%                      | 
 | Corviknight  7.762%                    | 
 | Regieleki  7.759%                      | 
 | Toxapex  4.141%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Suicune                                | 
 +----------------------------------------+ 
 | Raw count: 675                         | 
 | Avg. weight: 0.137369875493            | 
 | Viability Ceiling: 95                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Pressure 99.997%                       | 
 | Inner Focus  0.003%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 100.000%                     | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:252/0/0/0/4/252 52.527%          | 
 | Bold:252/0/56/0/64/136 11.826%         | 
 | Timid:252/0/0/0/60/196 10.735%         | 
 | Bold:252/0/72/0/40/144  9.451%         | 
 | Timid:252/0/4/0/0/252  4.994%          | 
 | Timid:252/0/80/0/0/176  3.863%         | 
 | Other  6.604%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 100.000%                         | 
 | Calm Mind 99.998%                      | 
 | Substitute 99.255%                     | 
 | Protect 99.031%                        | 
 | Other  1.717%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Cresselia 55.499%                      | 
 | Volcarona 33.626%                      | 
 | Registeel 33.155%                      | 
 | Victini 32.963%                        | 
 | Cloyster 32.426%                       | 
 | Tornadus-Therian 23.788%               | 
 | Dragonite 23.626%                      | 
 | Garchomp 22.816%                       | 
 | Zapdos 20.265%                         | 
 | Toxapex 18.805%                        | 
 | Tapu Fini 14.973%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Cloyster                               | 
 +----------------------------------------+ 
 | Raw count: 1435                        | 
 | Avg. weight: 0.0635526682553           | 
 | Viability Ceiling: 90                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Skill Link 95.220%                     | 
 | Shell Armor  4.744%                    | 
 | Overcoat  0.036%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 64.238%                     | 
 | Heavy-Duty Boots 19.936%               | 
 | Life Orb  9.907%                       | 
 | Never-Melt Ice  5.046%                 | 
 | Other  0.873%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 46.345%        | 
 | Naughty:0/252/0/4/0/252 29.681%        | 
 | Adamant:0/252/0/0/4/252 14.878%        | 
 | Naive:0/252/0/4/0/252  3.858%          | 
 | Adamant:4/252/0/0/0/252  2.659%        | 
 | Other  2.579%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shell Smash 100.000%                   | 
 | Icicle Spear 99.964%                   | 
 | Rock Blast 64.726%                     | 
 | Rapid Spin 31.557%                     | 
 | Hydro Pump 30.269%                     | 
 | Liquidation 24.682%                    | 
 | Toxic Spikes 23.013%                   | 
 | Ice Shard 12.051%                      | 
 | Other 13.738%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Volcarona 33.116%                      | 
 | Suicune 32.943%                        | 
 | Ninetales-Alola 31.321%                | 
 | Garchomp 27.241%                       | 
 | Cresselia 25.730%                      | 
 | Victini 22.504%                        | 
 | Registeel 22.501%                      | 
 | Arctozolt 22.435%                      | 
 | Aurorus 22.435%                        | 
 | Eiscue 22.168%                         | 
 | Sandslash-Alola 21.350%                | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Aegislash                              | 
 +----------------------------------------+ 
 | Raw count: 1408                        | 
 | Avg. weight: 0.0635605999531           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Stance Change 100.000%                 | 
 +----------------------------------------+ 
 | Items                                  | 
 | Weakness Policy 73.857%                | 
 | Leftovers 11.500%                      | 
 | Choice Specs  8.926%                   | 
 | Spell Tag  5.085%                      | 
 | Other  0.632%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:240/252/0/0/0/16 28.873%       | 
 | Adamant:168/252/0/0/0/88 27.120%       | 
 | Adamant:236/252/0/0/0/20 13.220%       | 
 | Quiet:252/4/0/252/0/0  7.508%          | 
 | Modest:252/0/0/184/56/16  5.167%       | 
 | Adamant:160/252/0/0/0/96  2.980%       | 
 | Other 15.132%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shadow Sneak 88.920%                   | 
 | Swords Dance 77.553%                   | 
 | Iron Head 77.545%                      | 
 | Shadow Claw 45.577%                    | 
 | King's Shield 44.708%                  | 
 | Shadow Ball 21.938%                    | 
 | Flash Cannon 14.743%                   | 
 | Close Combat 14.096%                   | 
 | Other 14.919%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 34.420%               | 
 | Blaziken 33.408%                       | 
 | Rillaboom 32.721%                      | 
 | Kartana 30.793%                        | 
 | Dragapult 24.983%                      | 
 | Blacephalon 20.560%                    | 
 | Ferrothorn 19.942%                     | 
 | Rotom-Wash 19.671%                     | 
 | Hydreigon 19.374%                      | 
 | Nihilego 18.879%                       | 
 | Kommo-o 17.196%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mamoswine                              | 
 +----------------------------------------+ 
 | Raw count: 551                         | 
 | Avg. weight: 0.163316085151            | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Thick Fat 84.979%                      | 
 | Oblivious 15.021%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 81.027%                      | 
 | Focus Sash 10.935%                     | 
 | Choice Band  5.291%                    | 
 | Other  2.747%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 77.142%        | 
 | Adamant:0/252/4/0/0/252  9.808%        | 
 | Naive:16/240/0/0/0/252  4.320%         | 
 | Jolly:48/252/0/0/0/208  3.479%         | 
 | Jolly:0/252/4/0/0/252  2.704%          | 
 | Other  2.546%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Ice Shard 99.999%                      | 
 | Earthquake 99.996%                     | 
 | Icicle Crash 97.274%                   | 
 | Substitute 72.693%                     | 
 | Stealth Rock 18.399%                   | 
 | Other 11.640%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Kartana 78.535%                        | 
 | Magnezone 71.527%                      | 
 | Dragonite 71.313%                      | 
 | Heatran 68.298%                        | 
 | Tapu Fini 67.912%                      | 
 | Buzzwole  6.875%                       | 
 | Dragapult  6.765%                      | 
 | Melmetal  6.225%                       | 
 | Obstagoon  6.151%                      | 
 | Landorus-Therian  6.117%               | 
 | Volcanion  5.301%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Arctozolt                              | 
 +----------------------------------------+ 
 | Raw count: 1275                        | 
 | Avg. weight: 0.0675250695162           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Slush Rush 99.977%                     | 
 | Volt Absorb  0.023%                    | 
 | Static  0.000%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 47.535%               | 
 | Choice Band 23.669%                    | 
 | Leftovers 11.613%                      | 
 | Magnet  8.547%                         | 
 | Life Orb  8.456%                       | 
 | Other  0.180%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 24.698%        | 
 | Naive:0/224/0/48/0/236 18.206%         | 
 | Naive:0/252/4/0/0/252 15.628%          | 
 | Naive:0/200/0/76/0/232 12.550%         | 
 | Naive:0/252/0/4/0/252 10.755%          | 
 | Naive:0/252/0/32/0/224  8.579%         | 
 | Other  9.583%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Bolt Beak 100.000%                     | 
 | Blizzard 73.107%                       | 
 | Low Kick 56.945%                       | 
 | Substitute 45.897%                     | 
 | Freeze-Dry 45.317%                     | 
 | Stomping Tantrum 26.889%               | 
 | Icicle Crash 26.849%                   | 
 | Rock Slide 24.869%                     | 
 | Other  0.127%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ninetales-Alola 96.126%                | 
 | Dragapult 33.982%                      | 
 | Heatran 31.285%                        | 
 | Garchomp 29.486%                       | 
 | Landorus-Therian 26.976%               | 
 | Aurorus 23.748%                        | 
 | Cloyster 23.748%                       | 
 | Eiscue 23.471%                         | 
 | Sandslash-Alola 22.601%                | 
 | Corviknight 18.678%                    | 
 | Scizor 16.921%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Victini                                | 
 +----------------------------------------+ 
 | Raw count: 1839                        | 
 | Avg. weight: 0.0486478530034           | 
 | Viability Ceiling: 95                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Victory Star 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 51.617%               | 
 | Choice Scarf 44.225%                   | 
 | Other  4.158%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:252/4/0/0/0/252 37.014%          | 
 | Jolly:0/252/0/0/4/252 26.154%          | 
 | Timid:0/0/0/252/4/252 12.323%          | 
 | Jolly:0/252/4/0/0/252  4.998%          | 
 | Hasty:0/172/0/84/0/252  4.399%         | 
 | Hasty:0/252/0/4/0/252  3.917%          | 
 | Other 11.195%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | U-turn 84.102%                         | 
 | V-create 83.480%                       | 
 | Bolt Strike 45.369%                    | 
 | Trick 42.559%                          | 
 | Final Gambit 38.279%                   | 
 | Glaciate 23.262%                       | 
 | Blue Flare 20.230%                     | 
 | Expanding Force 17.316%                | 
 | Thunder 12.428%                        | 
 | Taunt 10.640%                          | 
 | Toxic  6.266%                          | 
 | Other 16.069%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Registeel 34.153%                      | 
 | Cresselia 34.151%                      | 
 | Suicune 34.151%                        | 
 | Volcarona 33.599%                      | 
 | Landorus-Therian 24.717%               | 
 | Ferrothorn 24.306%                     | 
 | Cloyster 22.949%                       | 
 | Weavile 20.999%                        | 
 | Tapu Lele 18.985%                      | 
 | Garchomp 18.493%                       | 
 | Clefable 18.160%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Cresselia                              | 
 +----------------------------------------+ 
 | Raw count: 764                         | 
 | Avg. weight: 0.104503368959            | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 60.711%                   | 
 | Leftovers 22.220%                      | 
 | Mental Herb 12.504%                    | 
 | Other  4.565%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:252/0/4/0/0/252 26.268%          | 
 | Timid:248/0/0/0/52/208 17.363%         | 
 | Calm:252/0/132/0/56/68 13.714%         | 
 | Timid:252/0/24/0/0/232  8.767%         | 
 | Bold:252/0/252/0/4/0  6.671%           | 
 | Relaxed:248/0/244/0/16/0  5.767%       | 
 | Other 21.450%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Lunar Dance 76.755%                    | 
 | Ice Beam 68.884%                       | 
 | Trick 60.711%                          | 
 | Thunder Wave 47.969%                   | 
 | Moonlight 40.776%                      | 
 | Calm Mind 23.239%                      | 
 | Stored Power 23.223%                   | 
 | Substitute 18.377%                     | 
 | Moonblast 16.168%                      | 
 | Trick Room 15.191%                     | 
 | Other  8.708%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Suicune 64.360%                        | 
 | Volcarona 38.758%                      | 
 | Victini 38.225%                        | 
 | Registeel 38.225%                      | 
 | Cloyster 29.370%                       | 
 | Tornadus-Therian 26.130%               | 
 | Garchomp 24.679%                       | 
 | Toxapex 20.244%                        | 
 | Tapu Fini 17.363%                      | 
 | Scizor 17.363%                         | 
 | Zapdos 16.161%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Regieleki                              | 
 +----------------------------------------+ 
 | Raw count: 1239                        | 
 | Avg. weight: 0.0636659758452           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Transistor 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 63.959%               | 
 | Magnet 27.761%                         | 
 | Choice Specs  5.448%                   | 
 | Other  2.832%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 27.547%          | 
 | Hasty:0/4/0/252/0/252 26.805%          | 
 | Naive:80/4/0/252/0/172 14.674%         | 
 | Hasty:0/0/0/252/4/252 13.420%          | 
 | Naive:4/0/0/252/0/252  9.946%          | 
 | Adamant:0/252/4/0/0/252  2.462%        | 
 | Other  5.145%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Rapid Spin 96.887%                     | 
 | Volt Switch 93.841%                    | 
 | Extreme Speed 63.272%                  | 
 | Thunderbolt 58.196%                    | 
 | Electro Ball 38.975%                   | 
 | Ancient Power 28.215%                  | 
 | Explosion  8.097%                      | 
 | Other 12.517%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Lele 54.585%                      | 
 | Garchomp 45.358%                       | 
 | Landorus-Therian 43.830%               | 
 | Ferrothorn 41.269%                     | 
 | Tornadus-Therian 28.195%               | 
 | Gengar 22.436%                         | 
 | Barraskewda 18.776%                    | 
 | Pelipper 18.763%                       | 
 | Kartana 18.219%                        | 
 | Corviknight 16.333%                    | 
 | Dragonite 16.242%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Pelipper                               | 
 +----------------------------------------+ 
 | Raw count: 2672                        | 
 | Avg. weight: 0.0289317521493           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Drizzle 100.000%                       | 
 | Keen Eye  0.000%                       | 
 | Rain Dish  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 47.537%                   | 
 | Damp Rock 37.116%                      | 
 | Heavy-Duty Boots 10.986%               | 
 | Other  4.361%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Sassy:248/0/8/0/252/0 19.080%          | 
 | Modest:4/0/0/252/0/252 17.877%         | 
 | Modest:0/0/0/252/4/252 14.846%         | 
 | Relaxed:248/0/252/0/8/0  7.342%        | 
 | Bold:248/0/252/8/0/0  6.508%           | 
 | Timid:0/0/0/252/4/252  5.884%          | 
 | Other 28.463%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | U-turn 97.729%                         | 
 | Hurricane 67.366%                      | 
 | Roost 51.412%                          | 
 | Weather Ball 50.799%                   | 
 | Defog 39.487%                          | 
 | Scald 31.118%                          | 
 | Hydro Pump 24.587%                     | 
 | Surf 22.587%                           | 
 | Other 14.915%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 75.904%                     | 
 | Barraskewda 68.955%                    | 
 | Zapdos 43.837%                         | 
 | Tapu Lele 42.381%                      | 
 | Seismitoad 34.998%                     | 
 | Landorus-Therian 28.409%               | 
 | Regieleki 19.146%                      | 
 | Urshifu-Rapid-Strike 18.521%           | 
 | Melmetal 16.777%                       | 
 | Garchomp 12.828%                       | 
 | Hatterene 11.780%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Zapdos-Galar                           | 
 +----------------------------------------+ 
 | Raw count: 785                         | 
 | Avg. weight: 0.0792475673045           | 
 | Viability Ceiling: 96                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Defiant 100.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 39.617%                   | 
 | Choice Band 33.108%                    | 
 | Leftovers 26.163%                      | 
 | Other  1.112%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:4/252/0/0/0/252 49.117%          | 
 | Jolly:0/252/0/0/4/252 33.001%          | 
 | Adamant:0/252/0/0/4/252 13.271%        | 
 | Other  4.611%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Brave Bird 97.900%                     | 
 | Thunderous Kick 81.500%                | 
 | Close Combat 72.711%                   | 
 | U-turn 72.526%                         | 
 | Bulk Up 27.272%                        | 
 | Substitute 19.119%                     | 
 | Stomping Tantrum  9.387%               | 
 | Other 19.585%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Bisharp 62.815%                        | 
 | Weavile 59.698%                        | 
 | Landorus-Therian 43.926%               | 
 | Mew 36.726%                            | 
 | Polteageist 36.538%                    | 
 | Volcarona 36.271%                      | 
 | Kartana 26.292%                        | 
 | Dragonite 26.140%                      | 
 | Urshifu-Rapid-Strike 19.646%           | 
 | Gardevoir 19.119%                      | 
 | Dragapult 15.780%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Crawdaunt                              | 
 +----------------------------------------+ 
 | Raw count: 1523                        | 
 | Avg. weight: 0.0408489671204           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Adaptability 100.000%                  | 
 | Hyper Cutter  0.000%                   | 
 | Shell Armor  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 50.426%                       | 
 | Choice Band 37.147%                    | 
 | Focus Sash  8.907%                     | 
 | Other  3.520%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 36.684%        | 
 | Adamant:0/252/0/0/4/252 33.931%        | 
 | Adamant:252/252/0/0/4/0 13.341%        | 
 | Brave:248/252/0/0/8/0  7.401%          | 
 | Jolly:0/252/0/0/4/252  1.968%          | 
 | Adamant:0/252/0/0/0/252  1.593%        | 
 | Other  5.082%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 99.902%                      | 
 | Aqua Jet 99.873%                       | 
 | Crabhammer 91.514%                     | 
 | Swords Dance 59.258%                   | 
 | Close Combat 34.349%                   | 
 | Other 15.104%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 39.247%               | 
 | Blacephalon 38.254%                    | 
 | Heatran 33.505%                        | 
 | Dragapult 30.664%                      | 
 | Kartana 23.828%                        | 
 | Garchomp 23.678%                       | 
 | Weavile 16.919%                        | 
 | Rillaboom 16.865%                      | 
 | Melmetal 16.545%                       | 
 | Ferrothorn 15.548%                     | 
 | Tapu Fini 14.713%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Nihilego                               | 
 +----------------------------------------+ 
 | Raw count: 857                         | 
 | Avg. weight: 0.0725228873936           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Power Herb 82.307%                     | 
 | Choice Specs 10.028%                   | 
 | Choice Scarf  4.034%                   | 
 | Other  3.632%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:80/0/0/176/0/252 55.789%         | 
 | Modest:4/0/0/252/0/252 18.424%         | 
 | Timid:0/0/0/252/4/252 10.034%          | 
 | Timid:0/0/80/176/0/252  6.711%         | 
 | Modest:0/0/0/252/4/252  3.139%         | 
 | Jolly:252/0/156/0/28/72  3.051%        | 
 | Other  2.853%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Grass Knot 92.374%                     | 
 | Sludge Wave 91.067%                    | 
 | Power Gem 82.961%                      | 
 | Meteor Beam 82.307%                    | 
 | Pain Split 14.431%                     | 
 | Dazzling Gleam  9.324%                 | 
 | Stealth Rock  8.347%                   | 
 | Other 19.190%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Kartana 48.501%                        | 
 | Landorus-Therian 43.136%               | 
 | Rillaboom 27.990%                      | 
 | Aegislash 27.216%                      | 
 | Kommo-o 24.996%                        | 
 | Necrozma 24.234%                       | 
 | Slowbro 21.357%                        | 
 | Celesteela 18.719%                     | 
 | Umbreon 17.439%                        | 
 | Tapu Lele 17.311%                      | 
 | Dragonite 17.191%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mandibuzz                              | 
 +----------------------------------------+ 
 | Raw count: 738                         | 
 | Avg. weight: 0.0847645620867           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Overcoat 100.000%                      | 
 | Big Pecks  0.000%                      | 
 | Weak Armor  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 99.672%               | 
 | Other  0.328%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:248/0/164/0/0/96 21.588%        | 
 | Impish:252/0/152/0/104/0 17.432%       | 
 | Relaxed:248/0/252/0/8/0 14.162%        | 
 | Bold:248/0/244/0/0/16 11.332%          | 
 | Impish:248/0/64/0/176/20 10.235%       | 
 | Impish:248/0/92/0/152/16  9.199%       | 
 | Other 16.054%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 99.991%                          | 
 | Defog 98.487%                          | 
 | Foul Play 92.154%                      | 
 | U-turn 62.356%                         | 
 | Knock Off 30.881%                      | 
 | Other 16.130%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 32.897%                        | 
 | Magnezone 31.574%                      | 
 | Dragapult 26.350%                      | 
 | Swampert 24.330%                       | 
 | Ninetales-Alola 22.559%                | 
 | Arctozolt 22.539%                      | 
 | Blacephalon 21.722%                    | 
 | Slowking 16.041%                       | 
 | Blissey 15.995%                        | 
 | Quagsire 15.995%                       | 
 | Corviknight 15.994%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Marowak-Alola                          | 
 +----------------------------------------+ 
 | Raw count: 1053                        | 
 | Avg. weight: 0.0566519724336           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Rock Head 99.982%                      | 
 | Lightning Rod  0.018%                  | 
 | Cursed Body  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Thick Club 99.998%                     | 
 | Other  0.002%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:88/252/0/0/0/168 85.266%       | 
 | Brave:248/252/0/0/8/0  9.852%          | 
 | Other  4.882%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Flare Blitz 99.995%                    | 
 | Swords Dance 95.219%                   | 
 | Poltergeist 92.131%                    | 
 | Substitute 85.945%                     | 
 | Bonemerang  9.141%                     | 
 | Other 17.570%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Hatterene 95.025%                      | 
 | Garchomp 82.357%                       | 
 | Ferrothorn 82.356%                     | 
 | Slowbro 82.356%                        | 
 | Drampa 82.355%                         | 
 | Cresselia 12.786%                      | 
 | Melmetal 12.669%                       | 
 | Porygon2  9.484%                       | 
 | Crawdaunt  8.162%                      | 
 | Urshifu-Rapid-Strike  3.321%           | 
 | Pelipper  3.299%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Torkoal                                | 
 +----------------------------------------+ 
 | Raw count: 1074                        | 
 | Avg. weight: 0.0548772938324           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Drought 99.503%                        | 
 | White Smoke  0.497%                    | 
 | Shell Armor  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heat Rock 98.314%                      | 
 | Other  1.686%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:248/0/252/8/0/0 63.738%           | 
 | Bold:248/0/252/0/8/0 23.003%           | 
 | Relaxed:248/0/252/0/8/0  5.142%        | 
 | Calm:252/0/84/0/172/0  5.078%          | 
 | Other  3.039%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Rapid Spin 98.702%                     | 
 | Body Press 92.578%                     | 
 | Stealth Rock 90.777%                   | 
 | Lava Plume 86.360%                     | 
 | Toxic 13.638%                          | 
 | Other 17.943%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Venusaur 80.365%                       | 
 | Heatran 75.476%                        | 
 | Landorus-Therian 70.423%               | 
 | Blacephalon 58.697%                    | 
 | Garchomp 47.959%                       | 
 | Weavile 16.209%                        | 
 | Blaziken 13.340%                       | 
 | Hatterene 11.910%                      | 
 | Mandibuzz 10.889%                      | 
 | Lilligant 10.878%                      | 
 | Magnezone 10.863%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Barraskewda                            | 
 +----------------------------------------+ 
 | Raw count: 2106                        | 
 | Avg. weight: 0.0263353849421           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Swift Swim 99.957%                     | 
 | Propeller Tail  0.043%                 | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 99.146%                    | 
 | Other  0.854%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 35.670%        | 
 | Adamant:0/252/0/0/4/252 31.489%        | 
 | Adamant:0/252/0/0/0/252 12.467%        | 
 | Jolly:0/252/4/0/0/252  6.028%          | 
 | Adamant:32/252/0/0/36/188  5.354%      | 
 | Adamant:4/252/0/0/0/252  4.664%        | 
 | Other  4.328%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Liquidation 99.188%                    | 
 | Flip Turn 96.742%                      | 
 | Close Combat 96.308%                   | 
 | Crunch 47.473%                         | 
 | Aqua Jet 36.112%                       | 
 | Ice Fang 11.478%                       | 
 | Other 12.699%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Pelipper 96.113%                       | 
 | Ferrothorn 81.792%                     | 
 | Tapu Lele 58.729%                      | 
 | Zapdos 48.441%                         | 
 | Seismitoad 37.744%                     | 
 | Landorus-Therian 28.620%               | 
 | Regieleki 26.705%                      | 
 | Hatterene 12.871%                      | 
 | Porygon-Z 12.312%                      | 
 | Garchomp 12.274%                       | 
 | Tornadus-Therian 10.991%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Hydreigon                              | 
 +----------------------------------------+ 
 | Raw count: 814                         | 
 | Avg. weight: 0.0633191984851           | 
 | Viability Ceiling: 90                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 64.070%                   | 
 | Leftovers 11.953%                      | 
 | Black Glasses 10.795%                  | 
 | Life Orb  7.556%                       | 
 | Choice Specs  4.741%                   | 
 | Other  0.885%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 90.967%          | 
 | Timid:136/0/0/140/0/232  3.869%        | 
 | Modest:0/0/0/252/104/152  1.809%       | 
 | Other  3.355%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earth Power 92.838%                    | 
 | Dark Pulse 74.497%                     | 
 | Draco Meteor 69.173%                   | 
 | Flamethrower 62.634%                   | 
 | Roost 29.451%                          | 
 | Nasty Plot 25.565%                     | 
 | Thunder Wave 15.418%                   | 
 | Defog 12.379%                          | 
 | Other 18.043%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 76.958%               | 
 | Ferrothorn 44.138%                     | 
 | Blacephalon 38.904%                    | 
 | Aegislash 33.640%                      | 
 | Melmetal 32.244%                       | 
 | Toxapex 31.939%                        | 
 | Rotom-Wash 31.937%                     | 
 | Chansey 25.061%                        | 
 | Hatterene 25.061%                      | 
 | Corviknight 14.829%                    | 
 | Clefable 13.962%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Hawlucha                               | 
 +----------------------------------------+ 
 | Raw count: 1153                        | 
 | Avg. weight: 0.0457602210558           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Unburden 99.925%                       | 
 | Mold Breaker  0.074%                   | 
 | Limber  0.002%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Grassy Seed 63.330%                    | 
 | Electric Seed 19.186%                  | 
 | Psychic Seed 14.163%                   | 
 | Other  3.320%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/128/128 29.915%      | 
 | Adamant:0/252/0/0/4/252 26.145%        | 
 | Adamant:0/252/0/0/132/124 14.382%      | 
 | Adamant:232/252/0/0/0/24  5.267%       | 
 | Adamant:0/252/0/0/124/132  5.200%      | 
 | Adamant:128/252/4/0/0/124  4.291%      | 
 | Other 14.800%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Swords Dance 99.992%                   | 
 | Acrobatics 99.989%                     | 
 | Close Combat 94.348%                   | 
 | Stone Edge 36.877%                     | 
 | Roost 33.554%                          | 
 | Taunt 15.872%                          | 
 | Other 19.367%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 60.490%                      | 
 | Heatran 47.747%                        | 
 | Kartana 44.937%                        | 
 | Landorus-Therian 41.419%               | 
 | Weavile 35.256%                        | 
 | Clefable 16.675%                       | 
 | Dragapult 16.525%                      | 
 | Tapu Koko 16.339%                      | 
 | Garchomp 15.974%                       | 
 | Volcarona 14.782%                      | 
 | Tapu Lele 14.074%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Jirachi                                | 
 +----------------------------------------+ 
 | Raw count: 747                         | 
 | Avg. weight: 0.0678315879664           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Serene Grace 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 57.068%                      | 
 | Colbur Berry 17.174%                   | 
 | Iapapa Berry  9.259%                   | 
 | Weakness Policy  9.028%                | 
 | Heavy-Duty Boots  4.550%               | 
 | Other  2.921%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:252/0/0/4/0/252 45.858%          | 
 | Timid:252/0/72/0/0/184 13.177%         | 
 | Timid:224/0/44/8/0/232  7.340%         | 
 | Careful:248/0/0/0/88/172  5.671%       | 
 | Sassy:252/12/68/0/176/0  5.260%        | 
 | Timid:252/0/20/0/52/184  3.997%        | 
 | Other 18.697%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Stored Power 60.202%                   | 
 | Cosmic Power 59.700%                   | 
 | Iron Head 38.629%                      | 
 | Calm Mind 36.121%                      | 
 | Drain Punch 36.072%                    | 
 | Wish 31.891%                           | 
 | Stealth Rock 31.662%                   | 
 | Imprison 19.276%                       | 
 | Thunder Wave 18.975%                   | 
 | Body Slam 14.631%                      | 
 | Substitute 14.031%                     | 
 | Thunder  7.243%                        | 
 | U-turn  7.039%                         | 
 | Protect  6.331%                        | 
 | Other 18.196%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Shuckle 43.364%                        | 
 | Mew 43.364%                            | 
 | Magnezone 43.364%                      | 
 | Articuno-Galar 36.121%                 | 
 | Tapu Lele 35.124%                      | 
 | Grimmsnarl 22.228%                     | 
 | Dragonite 21.102%                      | 
 | Blaziken 20.218%                       | 
 | Toxapex 18.788%                        | 
 | Aegislash 17.603%                      | 
 | Zeraora 17.187%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Drampa                                 | 
 +----------------------------------------+ 
 | Raw count: 101                         | 
 | Avg. weight: 0.503613004801            | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Berserk 100.000%                       | 
 | Cloud Nine  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Chople Berry 100.000%                  | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Quiet:248/0/8/252/0/0 100.000%         | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Hyper Voice 100.000%                   | 
 | Roost 100.000%                         | 
 | Ice Beam 100.000%                      | 
 | Focus Blast 100.000%                   | 
 | Other  0.001%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Slowbro 96.586%                        | 
 | Marowak-Alola 96.586%                  | 
 | Hatterene 96.586%                      | 
 | Ferrothorn 96.586%                     | 
 | Garchomp 96.586%                       | 
 | Garchomp 96.586%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Venusaur                               | 
 +----------------------------------------+ 
 | Raw count: 1169                        | 
 | Avg. weight: 0.0439660442652           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Chlorophyll 99.993%                    | 
 | Overgrow  0.007%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 99.897%                       | 
 | Other  0.103%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 97.665%         | 
 | Other  2.335%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Growth 99.924%                         | 
 | Weather Ball 98.300%                   | 
 | Earth Power 97.552%                    | 
 | Giga Drain 94.385%                     | 
 | Other  9.840%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Torkoal 92.157%                        | 
 | Heatran 86.156%                        | 
 | Landorus-Therian 80.740%               | 
 | Garchomp 54.994%                       | 
 | Blacephalon 54.516%                    | 
 | Weavile 18.589%                        | 
 | Blaziken 15.297%                       | 
 | Dragapult 10.929%                      | 
 | Rillaboom 10.748%                      | 
 | Volcarona  9.124%                      | 
 | Victini  4.948%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Keldeo                                 | 
 +----------------------------------------+ 
 | Raw count: 335                         | 
 | Avg. weight: 0.117135594933            | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Justified 100.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 61.637%                      | 
 | Choice Specs 37.670%                   | 
 | Other  0.693%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 69.166%          | 
 | Modest:240/0/0/116/0/152 30.808%       | 
 | Other  0.025%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 89.334%                          | 
 | Secret Sword 69.192%                   | 
 | Substitute 61.642%                     | 
 | Taunt 52.692%                          | 
 | Calm Mind 39.759%                      | 
 | Flip Turn 37.938%                      | 
 | Hydro Pump 37.367%                     | 
 | Other 12.077%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 51.940%                    | 
 | Landorus-Therian 46.195%               | 
 | Heatran 44.959%                        | 
 | Clefable 41.152%                       | 
 | Weavile 31.022%                        | 
 | Gastrodon 30.808%                      | 
 | Tornadus-Therian 29.188%               | 
 | Melmetal 28.455%                       | 
 | Buzzwole 28.072%                       | 
 | Hatterene 26.879%                      | 
 | Slowking-Galar 22.317%                 | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Moltres-Galar                          | 
 +----------------------------------------+ 
 | Raw count: 689                         | 
 | Avg. weight: 0.0569751019941           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Berserk 100.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 53.532%               | 
 | Chesto Berry 40.220%                   | 
 | Weakness Policy  5.086%                | 
 | Other  1.162%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 42.008%         | 
 | Modest:160/0/0/252/0/96 17.568%        | 
 | Modest:80/0/0/232/0/196 14.947%        | 
 | Modest:64/0/0/252/0/192  9.989%        | 
 | Modest:104/0/0/252/0/152  3.179%       | 
 | Modest:248/0/0/252/8/0  2.936%         | 
 | Other  9.373%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Fiery Wrath 99.998%                    | 
 | Nasty Plot 94.832%                     | 
 | Agility 86.012%                        | 
 | Hurricane 50.219%                      | 
 | Rest 40.220%                           | 
 | Taunt 18.622%                          | 
 | Other 10.097%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 38.528%                      | 
 | Landorus-Therian 37.473%               | 
 | Tapu Lele 37.235%                      | 
 | Kartana 36.439%                        | 
 | Aegislash 31.302%                      | 
 | Blaziken 29.315%                       | 
 | Terrakion 26.572%                      | 
 | Heatran 20.603%                        | 
 | Urshifu-Rapid-Strike 20.217%           | 
 | Tapu Fini 16.604%                      | 
 | Dragonite 15.045%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Gengar                                 | 
 +----------------------------------------+ 
 | Raw count: 1227                        | 
 | Avg. weight: 0.0289661568475           | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Cursed Body 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Ring Target 49.461%                    | 
 | Focus Sash 16.690%                     | 
 | Choice Specs 14.840%                   | 
 | Choice Scarf 13.260%                   | 
 | Life Orb  5.555%                       | 
 | Other  0.193%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 91.687%          | 
 | Timid:0/0/4/252/0/252  8.116%          | 
 | Other  0.197%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shadow Ball 99.962%                    | 
 | Focus Blast 72.328%                    | 
 | Trick 61.422%                          | 
 | Nasty Plot 59.709%                     | 
 | Taunt 25.991%                          | 
 | Sludge Bomb 24.899%                    | 
 | Sludge Wave 23.428%                    | 
 | Energy Ball 15.225%                    | 
 | Other 17.035%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Lele 77.103%                      | 
 | Ferrothorn 62.074%                     | 
 | Garchomp 56.180%                       | 
 | Tornadus-Therian 49.924%               | 
 | Regieleki 49.796%                      | 
 | Dragapult 27.661%                      | 
 | Blacephalon 19.610%                    | 
 | Excadrill 19.392%                      | 
 | Landorus-Therian 18.724%               | 
 | Polteageist 15.060%                    | 
 | Weavile 13.031%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Polteageist                            | 
 +----------------------------------------+ 
 | Raw count: 494                         | 
 | Avg. weight: 0.0716041142675           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Weak Armor 99.175%                     | 
 | Cursed Body  0.825%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 99.173%                     | 
 | Other  0.827%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:4/0/0/252/0/252 66.766%          | 
 | Modest:0/0/0/252/4/252 24.086%         | 
 | Timid:0/0/0/252/4/252  8.136%          | 
 | Other  1.011%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shell Smash 99.183%                    | 
 | Shadow Ball 99.183%                    | 
 | Stored Power 99.173%                   | 
 | Giga Drain 98.049%                     | 
 | Other  4.413%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mew 69.060%                            | 
 | Weavile 68.978%                        | 
 | Bisharp 68.946%                        | 
 | Zapdos-Galar 64.259%                   | 
 | Volcarona 62.819%                      | 
 | Tapu Lele 17.648%                      | 
 | Blacephalon 17.619%                    | 
 | Excadrill 15.704%                      | 
 | Gengar 15.132%                         | 
 | Dragapult 15.131%                      | 
 | Hawlucha  9.200%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Kommo-o                                | 
 +----------------------------------------+ 
 | Raw count: 744                         | 
 | Avg. weight: 0.0470131306369           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Bulletproof 97.861%                    | 
 | Overcoat  2.128%                       | 
 | Soundproof  0.011%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Throat Spray 54.593%                   | 
 | Leftovers 27.507%                      | 
 | Life Orb  8.428%                       | 
 | Salac Berry  3.189%                    | 
 | Aguav Berry  2.443%                    | 
 | Other  3.840%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Naive:0/4/0/252/0/252 44.544%          | 
 | Jolly:0/252/0/0/4/252 15.469%          | 
 | Adamant:0/252/4/0/0/252 11.290%        | 
 | Adamant:0/252/0/0/4/252  9.983%        | 
 | Timid:4/0/0/252/0/252  5.436%          | 
 | Jolly:4/252/0/0/0/252  4.463%          | 
 | Other  8.816%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Close Combat 67.989%                   | 
 | Clangorous Soul 66.942%                | 
 | Clanging Scales 50.826%                | 
 | Boomburst 49.592%                      | 
 | Ice Punch 29.395%                      | 
 | Dragon Dance 27.408%                   | 
 | Earthquake 23.774%                     | 
 | Drain Punch 18.525%                    | 
 | Poison Jab 16.337%                     | 
 | Dragon Claw  9.320%                    | 
 | Flamethrower  6.447%                   | 
 | Flash Cannon  5.056%                   | 
 | Dragon Pulse  4.826%                   | 
 | Aura Sphere  4.379%                    | 
 | Other 19.184%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 57.020%                      | 
 | Nihilego 44.364%                       | 
 | Aegislash 43.998%                      | 
 | Kartana 43.444%                        | 
 | Necrozma 43.012%                       | 
 | Landorus-Therian 23.284%               | 
 | Tapu Fini 17.293%                      | 
 | Weavile 17.035%                        | 
 | Heatran 13.792%                        | 
 | Garchomp 13.640%                       | 
 | Gyarados 13.153%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Seismitoad                             | 
 +----------------------------------------+ 
 | Raw count: 1148                        | 
 | Avg. weight: 0.0284862628158           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Swift Swim 82.233%                     | 
 | Water Absorb 17.767%                   | 
 | Poison Touch  0.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 80.369%                       | 
 | Leftovers 15.686%                      | 
 | Other  3.944%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 46.921%         | 
 | Calm:248/0/8/0/252/0 13.985%           | 
 | Mild:0/16/0/252/4/236  9.276%          | 
 | Naive:0/76/0/180/0/252  8.716%         | 
 | Naive:0/4/0/252/0/252  5.905%          | 
 | Rash:0/4/0/252/0/252  3.631%           | 
 | Other 11.566%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earth Power 80.010%                    | 
 | Weather Ball 70.979%                   | 
 | Stealth Rock 49.173%                   | 
 | Focus Blast 46.327%                    | 
 | Icy Wind 22.500%                       | 
 | Sludge Wave 21.693%                    | 
 | Focus Punch 18.238%                    | 
 | Toxic 16.720%                          | 
 | Scald 16.352%                          | 
 | Power Whip 16.194%                     | 
 | Knock Off 15.907%                      | 
 | Surf  9.348%                           | 
 | Other 16.558%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Pelipper 82.733%                       | 
 | Zapdos 69.036%                         | 
 | Barraskewda 64.013%                    | 
 | Ferrothorn 60.070%                     | 
 | Melmetal 30.708%                       | 
 | Tornadus-Therian 17.745%               | 
 | Thundurus-Therian 14.532%              | 
 | Crawdaunt 14.306%                      | 
 | Buzzwole 14.044%                       | 
 | Mew 13.937%                            | 
 | Heatran 13.937%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Swampert                               | 
 +----------------------------------------+ 
 | Raw count: 1241                        | 
 | Avg. weight: 0.0270152374414           | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Damp 68.251%                           | 
 | Torrent 31.749%                        | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 95.390%                      | 
 | Other  4.610%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Sassy:252/4/0/0/252/0 40.268%          | 
 | Sassy:252/0/4/0/252/0 24.409%          | 
 | Relaxed:252/0/252/0/4/0 10.141%        | 
 | Impish:252/0/252/0/4/0  5.861%         | 
 | Careful:248/0/0/0/252/8  5.427%        | 
 | Careful:252/0/4/0/252/0  4.344%        | 
 | Other  9.551%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Flip Turn 99.404%                      | 
 | Stealth Rock 95.329%                   | 
 | Earthquake 84.384%                     | 
 | Yawn 49.781%                           | 
 | Ice Beam 23.286%                       | 
 | Toxic 18.720%                          | 
 | High Horsepower 14.325%                | 
 | Other 14.771%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 64.318%                      | 
 | Mandibuzz 45.397%                      | 
 | Magnezone 40.324%                      | 
 | Ninetales-Alola 39.788%                | 
 | Arctozolt 39.733%                      | 
 | Rillaboom 34.253%                      | 
 | Heatran 26.287%                        | 
 | Hawlucha 20.748%                       | 
 | Clefable 19.533%                       | 
 | Tapu Lele 15.077%                      | 
 | Corviknight 14.548%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Quagsire                               | 
 +----------------------------------------+ 
 | Raw count: 844                         | 
 | Avg. weight: 0.0442084455973           | 
 | Viability Ceiling: 93                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Unaware 99.997%                        | 
 | Water Absorb  0.003%                   | 
 | Damp  0.000%                           | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 91.506%                      | 
 | Heavy-Duty Boots  5.253%               | 
 | Other  3.241%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/0/252/0/4/0 37.989%         | 
 | Relaxed:252/0/252/0/4/0 31.420%        | 
 | Bold:252/0/124/0/112/20 15.898%        | 
 | Impish:252/4/252/0/0/0  7.113%         | 
 | Bold:252/0/252/0/4/0  3.210%           | 
 | Other  4.370%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Recover 99.989%                        | 
 | Scald 97.767%                          | 
 | Earthquake 79.016%                     | 
 | Toxic 78.896%                          | 
 | Protect 15.907%                        | 
 | Seismic Toss 15.898%                   | 
 | Other 12.527%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 80.409%                        | 
 | Corviknight 75.139%                    | 
 | Blissey 67.695%                        | 
 | Slowking 32.069%                       | 
 | Tornadus-Therian 31.658%               | 
 | Mandibuzz 26.816%                      | 
 | Blacephalon 24.176%                    | 
 | Clefable 17.697%                       | 
 | Buzzwole 10.640%                       | 
 | Hippowdon 10.635%                      | 
 | Zapdos  6.991%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Registeel                              | 
 +----------------------------------------+ 
 | Raw count: 255                         | 
 | Avg. weight: 0.129807505198            | 
 | Viability Ceiling: 95                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Clear Body 100.000%                    | 
 | Light Metal  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.864%                      | 
 | Other  0.136%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 65.312%           | 
 | Calm:252/0/196/0/60/0 30.057%          | 
 | Other  4.631%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Body Press 99.373%                     | 
 | Iron Defense 99.149%                   | 
 | Amnesia 99.111%                        | 
 | Rest 98.608%                           | 
 | Other  3.760%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Suicune 92.738%                        | 
 | Victini 92.207%                        | 
 | Cresselia 92.200%                      | 
 | Volcarona 90.987%                      | 
 | Cloyster 61.952%                       | 
 | Zapdos 30.249%                         | 
 | Blacephalon  1.543%                    | 
 | Zeraora  0.679%                        | 
 | Slowbro  0.527%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Togekiss                               | 
 +----------------------------------------+ 
 | Raw count: 1228                        | 
 | Avg. weight: 0.0253143384832           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Serene Grace 99.817%                   | 
 | Hustle  0.168%                         | 
 | Super Luck  0.016%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 66.924%               | 
 | Leftovers 28.735%                      | 
 | Other  4.341%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:132/0/0/216/0/160 47.288%       | 
 | Timid:248/0/0/120/0/136 27.771%        | 
 | Bold:252/0/216/0/40/0 16.502%          | 
 | Modest:176/0/0/252/0/80  2.584%        | 
 | Bold:252/0/216/40/0/0  2.575%          | 
 | Other  3.280%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Air Slash 99.989%                      | 
 | Nasty Plot 96.104%                     | 
 | Roost 67.308%                          | 
 | Heal Bell 67.200%                      | 
 | Thunder Wave 31.042%                   | 
 | Substitute 28.423%                     | 
 | Other  9.935%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Slowbro 67.426%                        | 
 | Ferrothorn 67.016%                     | 
 | Excadrill 66.850%                      | 
 | Tyranitar 66.399%                      | 
 | Moltres 47.288%                        | 
 | Cloyster 24.646%                       | 
 | Dragonite 24.606%                      | 
 | Klefki 24.599%                         | 
 | Xatu 24.598%                           | 
 | Suicune 24.598%                        | 
 | Hippowdon 19.343%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Shuckle                                | 
 +----------------------------------------+ 
 | Raw count: 1101                        | 
 | Avg. weight: 0.0264043043357           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sturdy 99.949%                         | 
 | Contrary  0.050%                       | 
 | Gluttony  0.001%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Custap Berry 81.814%                   | 
 | Mental Herb 15.943%                    | 
 | Other  2.243%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 65.882%           | 
 | Impish:252/0/252/0/4/0 16.117%         | 
 | Bold:248/0/252/0/8/0 12.977%           | 
 | Sassy:248/0/136/0/124/0  2.741%        | 
 | Other  2.283%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Stealth Rock 99.970%                   | 
 | Sticky Web 99.942%                     | 
 | Encore 98.052%                         | 
 | Toxic 58.862%                          | 
 | Final Gambit 41.095%                   | 
 | Other  2.080%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Magnezone 81.814%                      | 
 | Jirachi 75.481%                        | 
 | Mew 75.480%                            | 
 | Tapu Lele 67.228%                      | 
 | Articuno-Galar 62.873%                 | 
 | Kartana 19.651%                        | 
 | Dragonite 16.599%                      | 
 | Grimmsnarl 15.617%                     | 
 | Bisharp 13.107%                        | 
 | Zapdos-Galar 13.041%                   | 
 | Nidoking 12.977%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Dracozolt                              | 
 +----------------------------------------+ 
 | Raw count: 807                         | 
 | Avg. weight: 0.0343580881697           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sand Rush 96.809%                      | 
 | Hustle  3.091%                         | 
 | Volt Absorb  0.100%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 95.395%                       | 
 | Other  4.605%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Naughty:0/168/0/132/0/208 57.457%      | 
 | Naughty:0/148/0/176/0/184 25.292%      | 
 | Rash:0/88/0/212/0/208  8.956%          | 
 | Adamant:0/252/0/4/0/252  2.519%        | 
 | Naive:0/252/0/40/0/216  1.594%         | 
 | Other  4.181%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Bolt Beak 100.000%                     | 
 | Draco Meteor 98.508%                   | 
 | Earthquake 96.564%                     | 
 | Fire Blast 94.145%                     | 
 | Other 10.783%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tyranitar 95.349%                      | 
 | Excadrill 92.761%                      | 
 | Zapdos 64.845%                         | 
 | Toxapex 59.989%                        | 
 | Ferrothorn 57.880%                     | 
 | Hippowdon 33.887%                      | 
 | Corviknight 29.085%                    | 
 | Tornadus-Therian 28.439%               | 
 | Buzzwole  7.089%                       | 
 | Landorus-Therian  3.436%               | 
 | Slowbro  3.348%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Grimmsnarl                             | 
 +----------------------------------------+ 
 | Raw count: 457                         | 
 | Avg. weight: 0.0608986972258           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Prankster 100.000%                     | 
 | Pickpocket  0.000%                     | 
 | Frisk  0.000%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Light Clay 99.922%                     | 
 | Other  0.078%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:252/0/252/0/4/0 39.962%           | 
 | Careful:252/0/252/0/4/0 26.722%        | 
 | Impish:252/0/252/0/4/0 13.914%         | 
 | Bold:252/0/252/0/4/0 10.538%           | 
 | Jolly:252/4/0/0/0/252  6.334%          | 
 | Other  2.530%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Reflect 99.995%                        | 
 | Light Screen 99.922%                   | 
 | Thunder Wave 91.971%                   | 
 | Taunt 69.794%                          | 
 | Spirit Break 37.982%                   | 
 | Other  0.336%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Jirachi 40.416%                        | 
 | Dragonite 40.116%                      | 
 | Suicune 36.481%                        | 
 | Hatterene 29.821%                      | 
 | Garchomp 26.942%                       | 
 | Mew 26.315%                            | 
 | Toxapex 24.134%                        | 
 | Landorus-Therian 23.195%               | 
 | Kartana 17.057%                        | 
 | Volcarona 16.945%                      | 
 | Bisharp 16.584%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Chansey                                | 
 +----------------------------------------+ 
 | Raw count: 666                         | 
 | Avg. weight: 0.0420660483931           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Natural Cure 99.999%                   | 
 | Serene Grace  0.001%                   | 
 | Healer  0.000%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Eviolite 100.000%                      | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:0/0/252/0/252/4 62.059%           | 
 | Impish:248/8/252/0/0/0 15.009%         | 
 | Bold:252/0/252/0/4/0  8.093%           | 
 | Calm:252/0/4/0/252/0  7.291%           | 
 | Bold:248/0/252/0/8/0  7.162%           | 
 | Other  0.386%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Soft-Boiled 100.000%                   | 
 | Toxic 96.501%                          | 
 | Wish 46.371%                           | 
 | Counter 46.105%                        | 
 | Seismic Toss 45.335%                   | 
 | Stealth Rock 35.382%                   | 
 | Aromatherapy 22.296%                   | 
 | Other  8.010%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 79.130%                        | 
 | Hatterene 55.675%                      | 
 | Landorus-Therian 51.901%               | 
 | Melmetal 46.108%                       | 
 | Hydreigon 46.105%                      | 
 | Clefable 22.795%                       | 
 | Corviknight 22.497%                    | 
 | Gastrodon 15.958%                      | 
 | Ferrothorn 12.680%                     | 
 | Buzzwole  9.577%                       | 
 | Dragapult  9.269%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Reuniclus                              | 
 +----------------------------------------+ 
 | Raw count: 698                         | 
 | Avg. weight: 0.0355044485568           | 
 | Viability Ceiling: 92                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magic Guard 84.943%                    | 
 | Regenerator 15.056%                    | 
 | Overcoat  0.001%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 28.879%                      | 
 | Life Orb 21.162%                       | 
 | Grassy Seed 16.456%                    | 
 | Kasib Berry 13.635%                    | 
 | Assault Vest 13.541%                   | 
 | Colbur Berry  4.527%                   | 
 | Other  1.801%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/212/0/0/44 21.159%          | 
 | Modest:252/0/156/0/0/100 13.635%       | 
 | Bold:88/0/252/0/0/148 10.124%          | 
 | Quiet:248/0/8/0/252/0  9.558%          | 
 | Bold:200/0/252/0/0/56  6.804%          | 
 | Bold:244/0/216/0/0/48  5.653%          | 
 | Other 33.066%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Recover 86.229%                        | 
 | Calm Mind 86.108%                      | 
 | Psyshock 62.708%                       | 
 | Knock Off 46.317%                      | 
 | Focus Blast 42.574%                    | 
 | Stored Power 24.085%                   | 
 | Thunder 16.778%                        | 
 | Future Sight 13.536%                   | 
 | Psychic 13.207%                        | 
 | Other  8.458%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 57.476%                       | 
 | Skarmory 39.476%                       | 
 | Toxapex 38.508%                        | 
 | Tapu Koko 27.158%                      | 
 | Hippowdon 27.054%                      | 
 | Heatran 25.867%                        | 
 | Zapdos 25.335%                         | 
 | Tapu Bulu 20.189%                      | 
 | Dragapult 18.779%                      | 
 | Landorus-Therian 18.168%               | 
 | Tornadus-Therian 17.224%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Moltres                                | 
 +----------------------------------------+ 
 | Raw count: 382                         | 
 | Avg. weight: 0.0644576620357           | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Flame Body 71.194%                     | 
 | Pressure 28.806%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 93.905%               | 
 | Power Herb  6.082%                     | 
 | Other  0.013%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 59.746%           | 
 | Bold:248/0/140/0/0/120 28.753%         | 
 | Timid:0/0/0/252/4/252  6.085%          | 
 | Sassy:252/0/0/4/252/0  4.431%          | 
 | Other  0.985%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 93.866%                          | 
 | Flamethrower 93.749%                   | 
 | Hurricane 65.876%                      | 
 | Toxic 59.702%                          | 
 | Defog 29.275%                          | 
 | Substitute 28.827%                     | 
 | Fire Blast  6.147%                     | 
 | Scorching Sands  6.082%                | 
 | Other 16.476%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 64.046%                     | 
 | Slowbro 60.080%                        | 
 | Excadrill 59.717%                      | 
 | Tyranitar 59.717%                      | 
 | Togekiss 59.700%                       | 
 | Tapu Koko 27.762%                      | 
 | Toxapex 27.575%                        | 
 | Mew 27.524%                            | 
 | Mandibuzz 27.504%                      | 
 | Hippowdon 27.503%                      | 
 | Landorus-Therian 10.735%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Necrozma                               | 
 +----------------------------------------+ 
 | Raw count: 306                         | 
 | Avg. weight: 0.079247180569            | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Prism Armor 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Weakness Policy 64.252%                | 
 | Lum Berry 15.591%                      | 
 | Power Herb 12.205%                     | 
 | Choice Specs  7.886%                   | 
 | Other  0.066%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:252/0/84/172/0/0 64.250%        | 
 | Naughty:0/252/0/4/0/252 13.509%        | 
 | Naughty:0/200/0/120/0/188 11.824%      | 
 | Modest:0/0/0/252/4/252  7.886%         | 
 | Other  2.531%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Heat Wave 74.361%                      | 
 | Toxic 64.304%                          | 
 | Psyshock 64.250%                       | 
 | Stealth Rock 64.250%                   | 
 | Photon Geyser 35.446%                  | 
 | Earthquake 25.333%                     | 
 | Dragon Dance 15.593%                   | 
 | X-Scissor 15.593%                      | 
 | Meteor Beam 12.205%                    | 
 | Knock Off 11.825%                      | 
 | Other 16.839%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 62.090%                      | 
 | Kommo-o 62.040%                        | 
 | Kartana 62.039%                        | 
 | Aegislash 62.038%                      | 
 | Nihilego 62.038%                       | 
 | Landorus-Therian 31.359%               | 
 | Ferrothorn 31.335%                     | 
 | Tapu Lele 19.511%                      | 
 | Rotom-Wash 13.352%                     | 
 | Weavile 13.328%                        | 
 | Buzzwole 11.827%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tapu Bulu                              | 
 +----------------------------------------+ 
 | Raw count: 608                         | 
 | Avg. weight: 0.0391388202413           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Grassy Surge 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 53.812%                      | 
 | Choice Band 31.228%                    | 
 | Life Orb  4.846%                       | 
 | Choice Scarf  4.139%                   | 
 | Assault Vest  2.492%                   | 
 | Other  3.483%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:104/252/4/0/0/148 20.822%      | 
 | Adamant:248/228/0/0/32/0 19.806%       | 
 | Adamant:108/252/0/0/0/64 16.338%       | 
 | Adamant:196/252/0/0/0/60  9.954%       | 
 | Adamant:32/252/0/0/0/224  5.063%       | 
 | Jolly:0/252/0/0/4/252  4.139%          | 
 | Other 23.879%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Horn Leech 91.072%                     | 
 | Close Combat 72.238%                   | 
 | Stone Edge 64.910%                     | 
 | Swords Dance 55.501%                   | 
 | Wood Hammer 35.464%                    | 
 | Toxic 20.447%                          | 
 | Superpower 16.395%                     | 
 | High Horsepower  6.459%                | 
 | Synthesis  4.325%                      | 
 | Stored Power  4.133%                   | 
 | Calm Mind  4.133%                      | 
 | Iron Defense  4.133%                   | 
 | Zen Headbutt  3.708%                   | 
 | Other 17.082%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Heatran 62.330%                        | 
 | Landorus-Therian 46.186%               | 
 | Dragapult 39.628%                      | 
 | Kartana 37.430%                        | 
 | Clefable 32.395%                       | 
 | Zapdos 28.310%                         | 
 | Magnezone 27.470%                      | 
 | Reuniclus 21.026%                      | 
 | Weavile 18.174%                        | 
 | Mamoswine 16.338%                      | 
 | Keldeo 16.338%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Latios                                 | 
 +----------------------------------------+ 
 | Raw count: 932                         | 
 | Avg. weight: 0.025572142397            | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 82.251%                   | 
 | Soul Dew 15.742%                       | 
 | Other  2.007%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 94.395%          | 
 | Timid:64/0/0/252/0/192  3.898%         | 
 | Other  1.707%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Psychic 86.331%                        | 
 | Draco Meteor 80.111%                   | 
 | Trick 70.635%                          | 
 | Defog 61.648%                          | 
 | Psyshock 29.153%                       | 
 | Aura Sphere 27.875%                    | 
 | Ice Beam 21.161%                       | 
 | Surf  8.125%                           | 
 | Other 14.961%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 82.713%               | 
 | Buzzwole 59.243%                       | 
 | Slowbro 58.672%                        | 
 | Blissey 58.407%                        | 
 | Blacephalon 58.308%                    | 
 | Tapu Fini 19.586%                      | 
 | Heatran 17.211%                        | 
 | Magnezone 15.698%                      | 
 | Kartana 15.580%                        | 
 | Latias 15.538%                         | 
 | Rillaboom  9.987%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Porygon2                               | 
 +----------------------------------------+ 
 | Raw count: 807                         | 
 | Avg. weight: 0.0297089727867           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Trace 77.367%                          | 
 | Download 22.602%                       | 
 | Analytic  0.031%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Eviolite 99.827%                       | 
 | Other  0.173%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:252/0/4/0/252/0 71.181%           | 
 | Bold:248/0/176/0/80/4 19.206%          | 
 | Quiet:252/0/0/252/4/0  3.196%          | 
 | Sassy:252/0/0/4/252/0  1.844%          | 
 | Other  4.572%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Teleport 99.442%                       | 
 | Recover 96.485%                        | 
 | Toxic 62.210%                          | 
 | Thunder Wave 60.457%                   | 
 | Trick Room 39.274%                     | 
 | Ice Beam 33.853%                       | 
 | Other  8.279%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Melmetal 89.624%                       | 
 | Garchomp 55.419%                       | 
 | Dragapult 55.199%                      | 
 | Corviknight 55.187%                    | 
 | Zeraora 55.187%                        | 
 | Cresselia 34.581%                      | 
 | Crawdaunt 30.865%                      | 
 | Hatterene 23.839%                      | 
 | Marowak-Alola 23.597%                  | 
 | Magnezone 10.607%                      | 
 | Rhyperior 10.606%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Azumarill                              | 
 +----------------------------------------+ 
 | Raw count: 759                         | 
 | Avg. weight: 0.0281337372358           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Huge Power 99.194%                     | 
 | Sap Sipper  0.806%                     | 
 | Thick Fat  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Sitrus Berry 99.272%                   | 
 | Other  0.728%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:4/252/0/0/0/252 85.123%        | 
 | Adamant:252/252/0/0/4/0  9.984%        | 
 | Other  4.893%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Aqua Jet 99.991%                       | 
 | Play Rough 99.939%                     | 
 | Belly Drum 99.470%                     | 
 | Knock Off 98.956%                      | 
 | Other  1.645%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mew 93.348%                            | 
 | Weavile 85.076%                        | 
 | Garchomp 85.054%                       | 
 | Blacephalon 84.851%                    | 
 | Celesteela 84.816%                     | 
 | Volcarona  8.234%                      | 
 | Blaziken  8.147%                       | 
 | Blissey  8.078%                        | 
 | Slurpuff  7.120%                       | 
 | Pelipper  3.354%                       | 
 | Barraskewda  3.338%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Aurorus                                | 
 +----------------------------------------+ 
 | Raw count: 598                         | 
 | Avg. weight: 0.0355597282029           | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Snow Warning 100.000%                  | 
 | Refrigerate  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Icy Rock 99.996%                       | 
 | Other  0.004%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:248/0/0/252/8/0 99.996%         | 
 | Other  0.004%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earth Power 100.000%                   | 
 | Blizzard 99.999%                       | 
 | Stealth Rock 99.997%                   | 
 | Encore 99.996%                         | 
 | Other  0.008%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ninetales-Alola 96.150%                | 
 | Arctozolt 96.149%                      | 
 | Cloyster 96.149%                       | 
 | Eiscue 95.006%                         | 
 | Sandslash-Alola 91.502%                | 
 | Avalugg  5.791%                        | 
 | Avalugg  5.791%                        | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Eiscue                                 | 
 +----------------------------------------+ 
 | Raw count: 583                         | 
 | Avg. weight: 0.0361078333178           | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Ice Face 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Rocky Helmet 95.431%                   | 
 | Other  4.569%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/4/0/0/252 95.163%          | 
 | Other  4.837%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Belly Drum 100.000%                    | 
 | Icicle Crash 99.980%                   | 
 | Head Smash 99.878%                     | 
 | Zen Headbutt 90.301%                   | 
 | Other  9.840%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ninetales-Alola 95.991%                | 
 | Arctozolt 95.991%                      | 
 | Cloyster 95.971%                       | 
 | Aurorus 95.971%                        | 
 | Sandslash-Alola 91.276%                | 
 | Sandslash-Alola 91.276%                | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Sandslash-Alola                        | 
 +----------------------------------------+ 
 | Raw count: 606                         | 
 | Avg. weight: 0.0335334486631           | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Slush Rush 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 99.775%                       | 
 | Other  0.225%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/4/0/0/252 99.812%          | 
 | Other  0.188%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 99.934%                     | 
 | Swords Dance 99.916%                   | 
 | Icicle Crash 99.900%                   | 
 | Rapid Spin 99.859%                     | 
 | Other  0.391%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ninetales-Alola 95.840%                | 
 | Arctozolt 95.753%                      | 
 | Aurorus 95.750%                        | 
 | Cloyster 95.749%                       | 
 | Eiscue 94.553%                         | 
 | Eiscue 94.553%                         | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Thundurus-Therian                      | 
 +----------------------------------------+ 
 | Raw count: 457                         | 
 | Avg. weight: 0.0450291136718           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Volt Absorb 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 96.531%               | 
 | Other  3.469%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 43.142%         | 
 | Timid:0/0/0/252/4/252 30.249%          | 
 | Timid:0/0/4/252/0/252 24.693%          | 
 | Other  1.916%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Weather Ball 72.999%                   | 
 | Focus Blast 69.385%                    | 
 | Agility 42.931%                        | 
 | Rising Voltage 42.931%                 | 
 | Thunder 30.431%                        | 
 | Grass Knot 29.518%                     | 
 | Nasty Plot 29.456%                     | 
 | Volt Switch 26.755%                    | 
 | Thunderbolt 26.354%                    | 
 | Knock Off 24.735%                      | 
 | Other  4.506%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 50.003%                     | 
 | Heatran 40.151%                        | 
 | Landorus-Therian 39.500%               | 
 | Tapu Koko 39.256%                      | 
 | Arctozolt 39.256%                      | 
 | Ninetales-Alola 39.256%                | 
 | Pelipper 30.130%                       | 
 | Seismitoad 23.094%                     | 
 | Clefable 22.507%                       | 
 | Excadrill 21.664%                      | 
 | Slowbro 21.635%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Articuno-Galar                         | 
 +----------------------------------------+ 
 | Raw count: 60                          | 
 | Avg. weight: 0.304633281361            | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Competitive 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Chesto Berry 74.366%                   | 
 | Iapapa Berry 25.633%                   | 
 | Other  0.001%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 74.366%          | 
 | Timid:0/0/44/252/0/212 25.633%         | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Calm Mind 99.999%                      | 
 | Freezing Glare 74.366%                 | 
 | Air Slash 74.366%                      | 
 | Rest 74.366%                           | 
 | Agility 25.634%                        | 
 | Hurricane 25.633%                      | 
 | Stored Power 25.633%                   | 
 | Other  0.002%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Shuckle 99.999%                        | 
 | Mew 99.999%                            | 
 | Jirachi 99.999%                        | 
 | Magnezone 99.999%                      | 
 | Tapu Lele 95.216%                      | 
 | Tapu Lele 95.216%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Terrakion                              | 
 +----------------------------------------+ 
 | Raw count: 288                         | 
 | Avg. weight: 0.0692626929941           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Justified 100.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 71.593%                     | 
 | Choice Band 22.692%                    | 
 | Weakness Policy  2.637%                | 
 | Other  3.078%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 90.700%          | 
 | Jolly:4/252/0/0/0/252  4.079%          | 
 | Jolly:8/252/0/0/0/248  2.636%          | 
 | Other  2.585%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Close Combat 99.999%                   | 
 | Taunt 71.593%                          | 
 | Stealth Rock 71.593%                   | 
 | Rock Tomb 71.330%                      | 
 | Stone Edge 28.646%                     | 
 | Earthquake 24.151%                     | 
 | Quick Attack 18.866%                   | 
 | Other 13.821%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 63.056%                      | 
 | Blaziken 63.013%                       | 
 | Tapu Lele 54.215%                      | 
 | Moltres-Galar 52.216%                  | 
 | Aegislash 52.087%                      | 
 | Bisharp 20.471%                        | 
 | Garchomp 12.192%                       | 
 | Cloyster 12.019%                       | 
 | Landorus-Therian  9.326%               | 
 | Blacephalon  8.827%                    | 
 | Rillaboom  8.542%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Klefki                                 | 
 +----------------------------------------+ 
 | Raw count: 323                         | 
 | Avg. weight: 0.0555718005581           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Prankster 100.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Light Clay 50.713%                     | 
 | Air Balloon 42.018%                    | 
 | Iron Ball  6.950%                      | 
 | Other  0.319%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:252/0/4/0/252/0 70.945%           | 
 | Bold:252/0/252/0/4/0 25.242%           | 
 | Other  3.814%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Thunder Wave 99.788%                   | 
 | Reflect 92.763%                        | 
 | Light Screen 87.349%                   | 
 | Toxic 80.579%                          | 
 | Spikes 19.503%                         | 
 | Switcheroo  7.121%                     | 
 | Other 12.897%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Cloyster 69.408%                       | 
 | Suicune 58.493%                        | 
 | Xatu 56.583%                           | 
 | Dragonite 53.014%                      | 
 | Togekiss 42.602%                       | 
 | Cresselia 21.874%                      | 
 | Kommo-o 19.964%                        | 
 | Garchomp 16.397%                       | 
 | Gyarados 16.395%                       | 
 | Tornadus-Therian 11.378%               | 
 | Celesteela 10.414%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Gyarados                               | 
 +----------------------------------------+ 
 | Raw count: 1049                        | 
 | Avg. weight: 0.0168490410755           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Intimidate 78.453%                     | 
 | Moxie 21.547%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 86.854%                      | 
 | Lum Berry 11.705%                      | 
 | Other  1.441%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 74.272%        | 
 | Jolly:8/252/0/0/0/248 11.104%          | 
 | Jolly:24/128/116/0/0/240  5.398%       | 
 | Jolly:0/252/0/0/4/252  4.112%          | 
 | Jolly:4/252/0/0/0/252  3.297%          | 
 | Other  1.816%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Dragon Dance 99.995%                   | 
 | Waterfall 99.964%                      | 
 | Earthquake 80.323%                     | 
 | Substitute 79.470%                     | 
 | Ice Fang 12.568%                       | 
 | Power Whip 11.518%                     | 
 | Other 16.163%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mew 58.238%                            | 
 | Cloyster 56.451%                       | 
 | Volcarona 44.463%                      | 
 | Blissey 42.374%                        | 
 | Blaziken 41.749%                       | 
 | Kommo-o 26.029%                        | 
 | Garchomp 22.869%                       | 
 | Excadrill 17.924%                      | 
 | Weavile 16.794%                        | 
 | Cresselia 16.651%                      | 
 | Klefki 16.650%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Raikou                                 | 
 +----------------------------------------+ 
 | Raw count: 109                         | 
 | Avg. weight: 0.141935430476            | 
 | Viability Ceiling: 84                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Pressure 99.994%                       | 
 | Inner Focus  0.006%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.388%                      | 
 | Other  0.612%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:104/0/0/252/0/152 82.473%        | 
 | Timid:224/0/0/76/0/208 10.012%         | 
 | Timid:248/0/8/0/0/252  6.901%          | 
 | Other  0.614%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Calm Mind 99.388%                      | 
 | Substitute 99.386%                     | 
 | Thunderbolt 93.099%                    | 
 | Scald 93.095%                          | 
 | Other 15.032%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Urshifu-Rapid-Strike 82.480%           | 
 | Mew 82.473%                            | 
 | Garchomp 82.473%                       | 
 | Celesteela 82.473%                     | 
 | Blacephalon 82.473%                    | 
 | Weavile 16.914%                        | 
 | Heatran 10.013%                        | 
 | Dragapult 10.012%                      | 
 | Toxapex 10.012%                        | 
 | Landorus-Therian 10.012%               | 
 | Suicune  6.901%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Haxorus                                | 
 +----------------------------------------+ 
 | Raw count: 580                         | 
 | Avg. weight: 0.0263462887785           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Mold Breaker 100.000%                  | 
 | Rivalry  0.000%                        | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 46.448%                     | 
 | Life Orb 31.548%                       | 
 | Lum Berry 16.863%                      | 
 | White Herb  3.181%                     | 
 | Other  1.960%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 80.650%          | 
 | Adamant:0/252/0/0/4/252 16.080%        | 
 | Other  3.270%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Poison Jab 88.982%                     | 
 | Close Combat 80.909%                   | 
 | Swords Dance 78.368%                   | 
 | Scale Shot 63.237%                     | 
 | Dragon Claw 20.748%                    | 
 | Dragon Dance 19.660%                   | 
 | Outrage 17.384%                        | 
 | Taunt 15.560%                          | 
 | Other 15.151%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Garchomp 59.647%                       | 
 | Dragapult 48.146%                      | 
 | Excadrill 46.476%                      | 
 | Blacephalon 46.448%                    | 
 | Crawdaunt 28.278%                      | 
 | Cloyster 25.074%                       | 
 | Grimmsnarl 18.884%                     | 
 | Tapu Lele 18.172%                      | 
 | Hawlucha 18.170%                       | 
 | Gyarados 15.454%                       | 
 | Melmetal 13.587%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Xurkitree                              | 
 +----------------------------------------+ 
 | Raw count: 276                         | 
 | Avg. weight: 0.0514180342193           | 
 | Viability Ceiling: 90                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 95.353%                       | 
 | Other  4.647%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 95.935%         | 
 | Other  4.065%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Energy Ball 99.895%                    | 
 | Dazzling Gleam 99.895%                 | 
 | Calm Mind 95.177%                      | 
 | Rising Voltage 95.071%                 | 
 | Other  9.963%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 92.124%                      | 
 | Dragapult 91.260%                      | 
 | Heatran 91.258%                        | 
 | Celesteela 91.258%                     | 
 | Tapu Koko 91.258%                      | 
 | Kartana  2.734%                        | 
 | Stakataka  2.593%                      | 
 | Buzzwole  2.593%                       | 
 | Nihilego  2.573%                       | 
 | Blacephalon  2.491%                    | 
 | Melmetal  2.139%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Amoonguss                              | 
 +----------------------------------------+ 
 | Raw count: 721                         | 
 | Avg. weight: 0.0205152582167           | 
 | Viability Ceiling: 83                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 99.975%                    | 
 | Effect Spore  0.025%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Black Sludge 95.247%                   | 
 | Other  4.753%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:248/0/44/0/216/0 62.186%          | 
 | Calm:248/0/136/0/124/0 32.811%         | 
 | Bold:252/0/168/0/88/0  3.609%          | 
 | Other  1.395%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Spore 99.985%                          | 
 | Giga Drain 99.779%                     | 
 | Clear Smog 96.253%                     | 
 | Foul Play 95.180%                      | 
 | Other  8.803%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Weavile 90.109%                        | 
 | Slowbro 87.577%                        | 
 | Heatran 87.236%                        | 
 | Urshifu-Rapid-Strike 58.946%           | 
 | Landorus-Therian 57.922%               | 
 | Tornadus-Therian 30.001%               | 
 | Diggersby 29.190%                      | 
 | Slowking  3.686%                       | 
 | Garchomp  3.238%                       | 
 | Corviknight  3.238%                    | 
 | Volcarona  3.002%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Starmie                                | 
 +----------------------------------------+ 
 | Raw count: 474                         | 
 | Avg. weight: 0.0282142306896           | 
 | Viability Ceiling: 81                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Analytic 99.652%                       | 
 | Natural Cure  0.348%                   | 
 | Illuminate  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Power Herb 99.590%                     | 
 | Other  0.410%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 99.590%         | 
 | Other  0.410%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Rapid Spin 99.975%                     | 
 | Hydro Pump 99.627%                     | 
 | Psyshock 99.615%                       | 
 | Meteor Beam 99.590%                    | 
 | Other  1.193%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragonite 88.421%                      | 
 | Aegislash 64.983%                      | 
 | Blaziken 64.983%                       | 
 | Zeraora 64.983%                        | 
 | Jirachi 64.983%                        | 
 | Nihilego 34.607%                       | 
 | Kartana 23.410%                        | 
 | Mamoswine 23.409%                      | 
 | Moltres-Galar 23.409%                  | 
 | Hawlucha 11.543%                       | 
 | Landorus-Therian 11.222%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Xatu                                   | 
 +----------------------------------------+ 
 | Raw count: 308                         | 
 | Avg. weight: 0.0462726713724           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magic Bounce 87.450%                   | 
 | Synchronize 12.550%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Weakness Policy 78.184%                | 
 | Rocky Helmet 12.550%                   | 
 | Leftovers  9.258%                      | 
 | Other  0.008%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:248/0/0/8/0/252 73.689%          | 
 | Bold:252/0/216/0/40/0 12.550%          | 
 | Calm:252/0/44/0/132/80  8.402%         | 
 | Bold:248/0/252/0/0/8  4.495%           | 
 | Other  0.864%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 99.992%                          | 
 | Stored Power 86.586%                   | 
 | Cosmic Power 86.586%                   | 
 | Thunder Wave 74.545%                   | 
 | Heat Wave 17.045%                      | 
 | Psychic 12.557%                        | 
 | Teleport 12.556%                       | 
 | Other 10.133%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Klefki 71.263%                         | 
 | Cloyster 66.769%                       | 
 | Dragonite 66.768%                      | 
 | Suicune 66.768%                        | 
 | Togekiss 53.653%                       | 
 | Gastrodon 17.045%                      | 
 | Chansey 13.326%                        | 
 | Toxapex 13.326%                        | 
 | Clefable 13.326%                       | 
 | Celesteela 13.115%                     | 
 | Ferrothorn 12.550%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Gardevoir                              | 
 +----------------------------------------+ 
 | Raw count: 387                         | 
 | Avg. weight: 0.0311606616316           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Trace 99.916%                          | 
 | Synchronize  0.066%                    | 
 | Telepathy  0.018%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 98.630%                   | 
 | Other  1.370%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 99.874%          | 
 | Other  0.126%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Moonblast 99.955%                      | 
 | Mystical Fire 99.919%                  | 
 | Psychic 99.911%                        | 
 | Trick 98.632%                          | 
 | Other  1.583%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Urshifu-Rapid-Strike 98.653%           | 
 | Bisharp 98.634%                        | 
 | Dragonite 98.627%                      | 
 | Zapdos-Galar 98.626%                   | 
 | Landorus-Therian 98.626%               | 
 | Landorus-Therian 98.626%               | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Blastoise                              | 
 +----------------------------------------+ 
 | Raw count: 498                         | 
 | Avg. weight: 0.0257836402806           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Torrent 84.523%                        | 
 | Rain Dish 15.477%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | White Herb 77.491%                     | 
 | Life Orb 14.288%                       | 
 | Focus Sash  6.854%                     | 
 | Other  1.367%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 85.925%         | 
 | Modest:24/0/0/252/0/232  9.213%        | 
 | Other  4.862%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shell Smash 99.864%                    | 
 | Ice Beam 83.383%                       | 
 | Aura Sphere 75.923%                    | 
 | Hydro Pump 59.323%                     | 
 | Surf 26.383%                           | 
 | Water Spout 15.452%                    | 
 | Hyper Beam 14.284%                     | 
 | Terrain Pulse 13.068%                  | 
 | Other 12.320%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragonite 69.266%                      | 
 | Clefable 59.024%                       | 
 | Umbreon 59.022%                        | 
 | Nidoking 59.022%                       | 
 | Scizor 59.022%                         | 
 | Pelipper 14.284%                       | 
 | Blacephalon 11.964%                    | 
 | Zapdos  9.275%                         | 
 | Ferrothorn  9.231%                     | 
 | Barraskewda  9.213%                    | 
 | Seismitoad  9.213%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Porygon-Z                              | 
 +----------------------------------------+ 
 | Raw count: 264                         | 
 | Avg. weight: 0.0425234801576           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Download 91.109%                       | 
 | Adaptability  8.891%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 99.997%                   | 
 | Other  0.003%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/4/252/0/252 60.959%         | 
 | Modest:0/0/0/252/4/252 15.473%         | 
 | Timid:0/0/0/252/4/252 14.683%          | 
 | Modest:32/0/4/252/0/220  8.882%        | 
 | Other  0.003%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Tri Attack 99.997%                     | 
 | Thunderbolt 96.658%                    | 
 | Psyshock 64.299%                       | 
 | Shadow Ball 61.104%                    | 
 | Ice Beam 38.900%                       | 
 | Trick 35.691%                          | 
 | Other  3.350%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 87.498%                     | 
 | Barraskewda 60.828%                    | 
 | Pelipper 60.828%                       | 
 | Tapu Lele 60.688%                      | 
 | Garchomp 57.516%                       | 
 | Landorus-Therian 35.552%               | 
 | Dragonite 14.821%                      | 
 | Tapu Koko 14.681%                      | 
 | Jellicent 14.681%                      | 
 | Urshifu-Rapid-Strike 11.989%           | 
 | Slowking 11.989%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Golisopod                              | 
 +----------------------------------------+ 
 | Raw count: 480                         | 
 | Avg. weight: 0.0224503896215           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Emergency Exit 100.000%                | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 98.340%               | 
 | Other  1.660%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:252/252/0/0/4/0 99.872%        | 
 | Other  0.128%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | First Impression 100.000%              | 
 | Aqua Jet 98.441%                       | 
 | Knock Off 98.348%                      | 
 | Spikes 98.236%                         | 
 | Other  4.975%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Garchomp 98.319%                       | 
 | Celesteela 98.236%                     | 
 | Victini 98.236%                        | 
 | Regieleki 98.236%                      | 
 | Tapu Lele 98.236%                      | 
 | Tapu Lele 98.236%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Diggersby                              | 
 +----------------------------------------+ 
 | Raw count: 170                         | 
 | Avg. weight: 0.0692648286821           | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Huge Power 100.000%                    | 
 | Cheek Pouch  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 77.844%                    | 
 | Leftovers 15.098%                      | 
 | Life Orb  6.986%                       | 
 | Other  0.072%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 44.699%        | 
 | Adamant:0/252/0/0/4/252 25.254%        | 
 | Adamant:252/252/0/0/4/0 15.091%        | 
 | Jolly:0/252/0/0/4/252  8.066%          | 
 | Adamant:4/252/0/0/0/252  6.812%        | 
 | Other  0.078%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 93.195%                     | 
 | Fire Punch 74.652%                     | 
 | Quick Attack 66.393%                   | 
 | Ice Punch 56.594%                      | 
 | Body Slam 33.696%                      | 
 | Knock Off 28.511%                      | 
 | Spikes 15.091%                         | 
 | Mega Kick  9.983%                      | 
 | U-turn  7.951%                         | 
 | Other 13.933%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Slowbro 49.239%                        | 
 | Tornadus-Therian 44.590%               | 
 | Weavile 38.420%                        | 
 | Amoonguss 36.668%                      | 
 | Heatran 36.668%                        | 
 | Corviknight 29.731%                    | 
 | Magnezone 21.970%                      | 
 | Melmetal 20.412%                       | 
 | Tapu Koko 17.833%                      | 
 | Haxorus 17.071%                        | 
 | Alakazam 17.071%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Obstagoon                              | 
 +----------------------------------------+ 
 | Raw count: 447                         | 
 | Avg. weight: 0.0219492467983           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Guts 99.613%                           | 
 | Defiant  0.387%                        | 
 | Reckless  0.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Flame Orb 99.607%                      | 
 | Other  0.393%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 55.839%          | 
 | Adamant:0/252/4/0/0/252 36.438%        | 
 | Adamant:0/252/0/0/4/252  6.924%        | 
 | Other  0.799%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 99.986%                      | 
 | Facade 99.612%                         | 
 | Close Combat 56.237%                   | 
 | Parting Shot 39.006%                   | 
 | Switcheroo 36.140%                     | 
 | Obstruct 25.219%                       | 
 | Bulk Up 24.740%                        | 
 | Other 19.061%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 87.501%                      | 
 | Melmetal 68.130%                       | 
 | Buzzwole 56.423%                       | 
 | Mamoswine 56.418%                      | 
 | Volcanion 48.665%                      | 
 | Heatran 24.428%                        | 
 | Zapdos 24.428%                         | 
 | Tapu Bulu 24.143%                      | 
 | Reuniclus 24.143%                      | 
 | Landorus-Therian 18.966%               | 
 | Slowking 18.635%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Zygarde-10%                            | 
 +----------------------------------------+ 
 | Raw count: 103                         | 
 | Avg. weight: 0.101370837925            | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Aura Break 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 99.983%                    | 
 | Other  0.017%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 99.876%          | 
 | Other  0.124%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Thousand Arrows 99.988%                | 
 | Extreme Speed 99.876%                  | 
 | Iron Tail 62.630%                      | 
 | Toxic 62.629%                          | 
 | Outrage 37.247%                        | 
 | Superpower 37.236%                     | 
 | Other  0.394%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 90.768%               | 
 | Tapu Koko 53.533%                      | 
 | Urshifu-Rapid-Strike 53.533%           | 
 | Melmetal 53.533%                       | 
 | Ferrothorn 53.533%                     | 
 | Keldeo 37.235%                         | 
 | Mamoswine 37.235%                      | 
 | Tapu Bulu 37.235%                      | 
 | Magnezone 37.235%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Azelf                                  | 
 +----------------------------------------+ 
 | Raw count: 203                         | 
 | Avg. weight: 0.0378752414242           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 99.741%                     | 
 | Other  0.259%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 96.474%          | 
 | Other  3.526%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Taunt 99.741%                          | 
 | Stealth Rock 99.741%                   | 
 | Explosion 99.740%                      | 
 | Knock Off 96.545%                      | 
 | Other  4.233%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Garchomp 96.924%                       | 
 | Cloyster 96.264%                       | 
 | Kartana 53.337%                        | 
 | Nihilego 50.535%                       | 
 | Celesteela 50.535%                     | 
 | Dragapult 48.700%                      | 
 | Volcarona 46.003%                      | 
 | Tapu Lele 45.729%                      | 
 | Tapu Lele 45.729%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Ditto                                  | 
 +----------------------------------------+ 
 | Raw count: 515                         | 
 | Avg. weight: 0.0155087861597           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Imposter 100.000%                      | 
 | Limber  0.000%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 97.538%                   | 
 | Other  2.462%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Relaxed:252/4/252/0/0/0 61.257%        | 
 | Impish:248/8/252/0/0/0 22.760%         | 
 | Serious:252/0/4/0/0/252  8.809%        | 
 | Quiet:252/4/0/252/0/0  3.432%          | 
 | Other  3.741%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Nothing 300.000%                       | 
 | Transform 100.000%                     | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 80.823%               | 
 | Dragapult 61.268%                      | 
 | Blacephalon 61.257%                    | 
 | Magnezone 61.257%                      | 
 | Tapu Lele 61.257%                      | 
 | Ferrothorn 29.914%                     | 
 | Blissey 19.457%                        | 
 | Slowbro 19.068%                        | 
 | Toxapex 12.538%                        | 
 | Alakazam 11.644%                       | 
 | Corsola-Galar 10.135%                  | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Rhyperior                              | 
 +----------------------------------------+ 
 | Raw count: 179                         | 
 | Avg. weight: 0.0464500009704           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Solid Rock 69.411%                     | 
 | Lightning Rod 30.589%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 98.525%                      | 
 | Other  1.475%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:36/252/0/0/0/220 66.338%       | 
 | Adamant:252/252/0/0/4/0 32.272%        | 
 | Other  1.391%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Stealth Rock 98.527%                   | 
 | Stone Edge 98.314%                     | 
 | Swords Dance 67.941%                   | 
 | High Horsepower 66.338%                | 
 | Earthquake 33.662%                     | 
 | Ice Punch 31.892%                      | 
 | Other  3.326%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Melmetal 86.265%                       | 
 | Rillaboom 56.045%                      | 
 | Heatran 54.373%                        | 
 | Tapu Fini 54.373%                      | 
 | Landorus-Therian 54.373%               | 
 | Magnezone 30.587%                      | 
 | Crawdaunt 30.586%                      | 
 | Cresselia 30.584%                      | 
 | Porygon2 30.584%                       | 
 | Charizard  1.672%                      | 
 | Dragapult  1.672%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Latias                                 | 
 +----------------------------------------+ 
 | Raw count: 326                         | 
 | Avg. weight: 0.0211361040578           | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 54.807%                      | 
 | Sitrus Berry 20.544%                   | 
 | Choice Scarf 16.155%                   | 
 | Eject Pack  8.199%                     | 
 | Other  0.295%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:248/0/0/8/0/252 53.728%          | 
 | Timid:252/0/0/4/0/252 21.621%          | 
 | Timid:0/0/0/252/4/252 20.128%          | 
 | Other  4.523%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Calm Mind 55.056%                      | 
 | Aura Sphere 55.040%                    | 
 | Stored Power 55.040%                   | 
 | Substitute 53.728%                     | 
 | Draco Meteor 44.941%                   | 
 | Healing Wish 44.898%                   | 
 | Thunder Wave 28.743%                   | 
 | Psyshock 20.544%                       | 
 | Defog 13.847%                          | 
 | Trick 11.929%                          | 
 | Other 16.234%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Kartana 83.742%                        | 
 | Tapu Fini 59.793%                      | 
 | Landorus-Therian 58.725%               | 
 | Magnezone 54.805%                      | 
 | Latios 53.746%                         | 
 | Tyranitar 30.443%                      | 
 | Tapu Lele 29.758%                      | 
 | Mamoswine 25.198%                      | 
 | Corviknight 24.901%                    | 
 | Melmetal 11.929%                       | 
 | Garchomp  8.018%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Alakazam                               | 
 +----------------------------------------+ 
 | Raw count: 439                         | 
 | Avg. weight: 0.0164101928445           | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magic Guard 99.948%                    | 
 | Inner Focus  0.049%                    | 
 | Synchronize  0.003%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 88.344%                       | 
 | Focus Sash 11.431%                     | 
 | Other  0.225%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 53.380%          | 
 | Modest:0/0/0/252/4/252 46.186%         | 
 | Other  0.433%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Nasty Plot 83.105%                     | 
 | Shadow Ball 66.832%                    | 
 | Focus Blast 59.800%                    | 
 | Psyshock 46.478%                       | 
 | Energy Ball 34.173%                    | 
 | Psychic 27.498%                        | 
 | Expanding Force 26.040%                | 
 | Recover 25.789%                        | 
 | Grass Knot 16.032%                     | 
 | Other 14.253%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 66.689%                    | 
 | Landorus-Therian 47.057%               | 
 | Slowbro 38.829%                        | 
 | Melmetal 27.918%                       | 
 | Magnezone 27.904%                      | 
 | Diggersby 27.903%                      | 
 | Haxorus 27.903%                        | 
 | Snorlax 25.911%                        | 
 | Heatran 25.822%                        | 
 | Ferrothorn 21.667%                     | 
 | Kartana 13.362%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Lilligant                              | 
 +----------------------------------------+ 
 | Raw count: 38                          | 
 | Avg. weight: 0.168840392783            | 
 | Viability Ceiling: 81                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Chlorophyll 99.974%                    | 
 | Own Tempo  0.026%                      | 
 | Leaf Guard  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 99.974%                       | 
 | Other  0.026%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 99.789%         | 
 | Other  0.211%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Growth 99.974%                         | 
 | Sleep Powder 99.815%                   | 
 | Pollen Puff 99.789%                    | 
 | Energy Ball 99.789%                    | 
 | Other  0.634%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Torkoal 99.926%                        | 
 | Mandibuzz 99.789%                      | 
 | Hatterene 99.789%                      | 
 | Blacephalon 99.789%                    | 
 | Magnezone 99.789%                      | 
 | Magnezone 99.789%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tangrowth                              | 
 +----------------------------------------+ 
 | Raw count: 702                         | 
 | Avg. weight: 0.00860981650985          | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 100.000%                   | 
 | Chlorophyll  0.000%                    | 
 | Leaf Guard  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Rocky Helmet 59.273%                   | 
 | Eject Button 16.180%                   | 
 | Nothing 14.213%                        | 
 | Heavy-Duty Boots  7.539%               | 
 | Other  2.796%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Relaxed:252/0/252/0/4/0 53.725%        | 
 | Relaxed:248/0/252/0/8/0 30.715%        | 
 | Impish:252/4/252/0/0/0 11.296%         | 
 | Other  4.264%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 97.078%                      | 
 | Giga Drain 88.304%                     | 
 | Focus Blast 81.775%                    | 
 | Sleep Powder 48.935%                   | 
 | Toxic 28.584%                          | 
 | Leech Seed 27.481%                     | 
 | Power Whip 11.298%                     | 
 | Other 16.544%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 44.102%               | 
 | Rotom-Wash 43.406%                     | 
 | Blissey 35.395%                        | 
 | Clefable 35.296%                       | 
 | Excadrill 34.374%                      | 
 | Tyranitar 18.198%                      | 
 | Toxapex 16.977%                        | 
 | Tyrantrum 16.180%                      | 
 | Arctozolt 16.180%                      | 
 | Ninetales-Alola 16.180%                | 
 | Melmetal 15.902%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Raichu-Alola                           | 
 +----------------------------------------+ 
 | Raw count: 260                         | 
 | Avg. weight: 0.0215373859543           | 
 | Viability Ceiling: 83                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Surge Surfer 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 72.421%                       | 
 | Magnet 21.419%                         | 
 | Choice Specs  6.158%                   | 
 | Other  0.002%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 56.519%          | 
 | Modest:0/0/0/252/4/252 35.394%         | 
 | Modest:0/0/4/252/0/252  8.049%         | 
 | Other  0.038%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Psyshock 99.950%                       | 
 | Rising Voltage 95.966%                 | 
 | Nasty Plot 93.832%                     | 
 | Surf 47.479%                           | 
 | Grass Knot 44.816%                     | 
 | Other 17.957%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Koko 98.078%                      | 
 | Garchomp 81.709%                       | 
 | Weavile 58.612%                        | 
 | Mew 52.473%                            | 
 | Celesteela 52.473%                     | 
 | Zapdos 29.277%                         | 
 | Corviknight 29.243%                    | 
 | Tapu Fini 29.236%                      | 
 | Landorus-Therian 16.367%               | 
 | Victini  6.160%                        | 
 | Clefable  6.158%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Krookodile                             | 
 +----------------------------------------+ 
 | Raw count: 709                         | 
 | Avg. weight: 0.0078272239868           | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Moxie 65.861%                          | 
 | Intimidate 34.122%                     | 
 | Anger Point  0.016%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 54.505%                   | 
 | Weakness Policy 29.096%                | 
 | Rocky Helmet  9.100%                   | 
 | Heavy-Duty Boots  6.497%               | 
 | Other  0.802%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 58.805%          | 
 | Jolly:112/140/0/0/4/252 17.526%        | 
 | Jolly:80/176/0/0/0/252  9.100%         | 
 | Jolly:252/4/0/0/0/252  6.497%          | 
 | Adamant:4/156/72/0/24/252  5.305%      | 
 | Other  2.768%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 99.984%                     | 
 | Knock Off 68.756%                      | 
 | Close Combat 64.419%                   | 
 | Stealth Rock 33.325%                   | 
 | Power Trip 29.359%                     | 
 | Scale Shot 29.096%                     | 
 | Toxic 17.526%                          | 
 | Foul Play 17.526%                      | 
 | Taunt 15.597%                          | 
 | Stone Edge 13.944%                     | 
 | Other 10.470%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tornadus-Therian 72.352%               | 
 | Heatran 50.416%                        | 
 | Clefable 38.062%                       | 
 | Rotom-Wash 35.271%                     | 
 | Blacephalon 33.131%                    | 
 | Corviknight 29.992%                    | 
 | Landorus-Therian 28.602%               | 
 | Klefki 28.147%                         | 
 | Nidoking 17.728%                       | 
 | Rillaboom 17.543%                      | 
 | Dragapult 11.632%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Sirfetch'd                             | 
 +----------------------------------------+ 
 | Raw count: 359                         | 
 | Avg. weight: 0.0153040174944           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Scrappy 99.991%                        | 
 | Steadfast  0.009%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 98.654%                    | 
 | Other  1.346%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 98.646%        | 
 | Other  1.354%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Close Combat 99.884%                   | 
 | Brave Bird 99.840%                     | 
 | First Impression 99.840%               | 
 | Knock Off 98.664%                      | 
 | Other  1.772%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Slowbro 98.646%                        | 
 | Landorus-Therian 98.646%               | 
 | Corviknight 89.131%                    | 
 | Blacephalon 83.675%                    | 
 | Toxapex 83.673%                        | 
 | Weavile 14.974%                        | 
 | Clefable 14.974%                       | 
 | Clefable 14.974%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Snorlax                                | 
 +----------------------------------------+ 
 | Raw count: 878                         | 
 | Avg. weight: 0.00567408012122          | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Immunity 62.073%                       | 
 | Thick Fat 37.855%                      | 
 | Gluttony  0.072%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.919%                      | 
 | Other  0.081%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/0/252/0/4/0 48.979%         | 
 | Adamant:252/116/0/0/140/0 37.247%      | 
 | Impish:252/0/200/0/56/0 12.746%        | 
 | Other  1.028%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Body Slam 99.655%                      | 
 | Curse 99.653%                          | 
 | Rest 99.653%                           | 
 | Earthquake 86.576%                     | 
 | Other 14.462%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Cresselia 48.979%                      | 
 | Dragonite 48.979%                      | 
 | Toxapex 48.979%                        | 
 | Buzzwole 48.979%                       | 
 | Suicune 48.979%                        | 
 | Slowbro 41.440%                        | 
 | Alakazam 37.469%                       | 
 | Heatran 37.260%                        | 
 | Corviknight 37.253%                    | 
 | Landorus-Therian 37.248%               | 
 | Togekiss 11.331%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Slurpuff                               | 
 +----------------------------------------+ 
 | Raw count: 215                         | 
 | Avg. weight: 0.0233448826353           | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Unburden 100.000%                      | 
 | Sweet Veil  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Sitrus Berry 97.882%                   | 
 | Other  2.118%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:4/252/0/0/0/252 96.179%        | 
 | Other  3.821%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Play Rough 97.891%                     | 
 | Belly Drum 97.891%                     | 
 | Drain Punch 97.891%                    | 
 | Sticky Web 65.301%                     | 
 | Yawn 35.501%                           | 
 | Other  5.526%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Volcarona 93.485%                      | 
 | Mew 93.485%                            | 
 | Blaziken 93.485%                       | 
 | Blissey 93.485%                        | 
 | Scrafty 59.074%                        | 
 | Azumarill 30.293%                      | 
 | Gyarados  4.118%                       | 
 | Landorus-Therian  2.110%               | 
 | Blacephalon  2.109%                    | 
 | Regieleki  2.109%                      | 
 | Gengar  2.109%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Conkeldurr                             | 
 +----------------------------------------+ 
 | Raw count: 671                         | 
 | Avg. weight: 0.00754996286729          | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Guts 94.484%                           | 
 | Sheer Force  3.304%                    | 
 | Iron Fist  2.212%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Flame Orb 84.016%                      | 
 | Leftovers  7.485%                      | 
 | Choice Band  5.192%                    | 
 | Other  3.306%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:128/252/0/0/0/128 56.466%      | 
 | Adamant:252/252/0/0/4/0 24.024%        | 
 | Careful:236/16/0/0/252/4  7.485%       | 
 | Brave:252/252/4/0/0/0  6.116%          | 
 | Adamant:0/252/0/0/0/252  2.980%        | 
 | Other  2.929%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Mach Punch 92.628%                     | 
 | Knock Off 91.165%                      | 
 | Facade 79.744%                         | 
 | Drain Punch 72.899%                    | 
 | Rock Slide 15.007%                     | 
 | Ice Punch 12.550%                      | 
 | Close Combat 12.084%                   | 
 | Bulk Up  8.586%                        | 
 | Other 15.338%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 62.413%                       | 
 | Toxapex 59.850%                        | 
 | Garchomp 59.325%                       | 
 | Heatran 58.520%                        | 
 | Tornadus-Therian 56.466%               | 
 | Ferrothorn 16.030%                     | 
 | Gyarados 14.717%                       | 
 | Mimikyu 14.705%                        | 
 | Duraludon 11.846%                      | 
 | Reuniclus  9.883%                      | 
 | Landorus-Therian  9.305%               | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Espeon                                 | 
 +----------------------------------------+ 
 | Raw count: 668                         | 
 | Avg. weight: 0.00671144784743          | 
 | Viability Ceiling: 84                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Magic Bounce 100.000%                  | 
 | Synchronize  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 42.482%                   | 
 | Colbur Berry 40.200%                   | 
 | Light Clay 13.683%                     | 
 | Other  3.634%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:248/0/0/8/0/252 81.752%          | 
 | Timid:252/0/0/4/0/252 13.404%          | 
 | Other  4.844%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Psychic 97.645%                        | 
 | Morning Sun 82.379%                    | 
 | Yawn 53.869%                           | 
 | Dazzling Gleam 45.207%                 | 
 | Trick 42.744%                          | 
 | Calm Mind 41.324%                      | 
 | Light Screen 13.866%                   | 
 | Reflect 13.856%                        | 
 | Other  9.110%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mew 81.829%                            | 
 | Magnezone 81.796%                      | 
 | Shuckle 81.752%                        | 
 | Grimmsnarl 81.752%                     | 
 | Jirachi 81.752%                        | 
 | Blastoise 12.015%                      | 
 | Dragonite 11.950%                      | 
 | Chansey 11.604%                        | 
 | Volcarona 11.578%                      | 
 | Ninetales-Alola 11.566%                | 
 | Corviknight  2.247%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tyrantrum                              | 
 +----------------------------------------+ 
 | Raw count: 155                         | 
 | Avg. weight: 0.0269192206668           | 
 | Viability Ceiling: 89                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Rock Head 99.989%                      | 
 | Strong Jaw  0.011%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 99.309%                    | 
 | Other  0.691%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:4/252/0/0/0/252 58.770%          | 
 | Adamant:0/252/4/0/0/252 25.832%        | 
 | Adamant:0/252/0/0/0/252 14.718%        | 
 | Other  0.680%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Head Smash 99.989%                     | 
 | Close Combat 99.986%                   | 
 | Stealth Rock 73.477%                   | 
 | Ice Fang 61.165%                       | 
 | Outrage 38.813%                        | 
 | Scale Shot 23.437%                     | 
 | Other  3.132%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 82.218%               | 
 | Slowbro 61.165%                        | 
 | Toxapex 58.770%                        | 
 | Weavile 58.770%                        | 
 | Tornadus-Therian 58.770%               | 
 | Arctozolt 23.437%                      | 
 | Blissey 23.437%                        | 
 | Tangrowth 23.437%                      | 
 | Ninetales-Alola 23.437%                | 
 | Corviknight 12.677%                    | 
 | Buzzwole 10.282%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Sandaconda                             | 
 +----------------------------------------+ 
 | Raw count: 151                         | 
 | Avg. weight: 0.0279920684293           | 
 | Viability Ceiling: 81                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Shed Skin 99.998%                      | 
 | Sand Spit  0.002%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.998%                      | 
 | Other  0.002%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:252/0/4/0/252/0 59.017%        | 
 | Careful:252/0/0/0/252/4 40.981%        | 
 | Other  0.002%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Earthquake 100.000%                    | 
 | Glare 99.998%                          | 
 | Stealth Rock 99.998%                   | 
 | Rest 99.998%                           | 
 | Other  0.007%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 93.881%                      | 
 | Melmetal 93.881%                       | 
 | Zapdos 93.881%                         | 
 | Blissey 52.900%                        | 
 | Buzzwole 52.900%                       | 
 | Weavile 40.981%                        | 
 | Primarina 40.981%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Primarina                              | 
 +----------------------------------------+ 
 | Raw count: 525                         | 
 | Avg. weight: 0.00691987391402          | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Torrent 98.464%                        | 
 | Liquid Voice  1.536%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 47.681%                   | 
 | Metronome 25.934%                      | 
 | Choice Specs 21.792%                   | 
 | Other  4.593%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/4/252/0/252 47.726%         | 
 | Modest:252/0/0/252/0/4 47.680%         | 
 | Other  4.594%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 97.749%                          | 
 | Moonblast 97.203%                      | 
 | Psychic 96.362%                        | 
 | Flip Turn 48.339%                      | 
 | Substitute 28.888%                     | 
 | Hydro Pump 22.700%                     | 
 | Other  8.758%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 69.097%                      | 
 | Melmetal 68.813%                       | 
 | Weavile 50.949%                        | 
 | Zapdos 47.681%                         | 
 | Sandaconda 47.680%                     | 
 | Aegislash 25.954%                      | 
 | Mandibuzz 25.933%                      | 
 | Tangrowth 25.933%                      | 
 | Rotom-Wash 25.933%                     | 
 | Excadrill 25.933%                      | 
 | Buzzwole 21.138%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Inteleon                               | 
 +----------------------------------------+ 
 | Raw count: 369                         | 
 | Avg. weight: 0.0096647170442           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Torrent 86.422%                        | 
 | Sniper 13.578%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 85.120%                   | 
 | Scope Lens 13.336%                     | 
 | Other  1.544%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 96.547%          | 
 | Other  3.453%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Ice Beam 99.928%                       | 
 | U-turn 95.677%                         | 
 | Surf 86.398%                           | 
 | Weather Ball 85.059%                   | 
 | Snipe Shot 11.952%                     | 
 | Air Slash  9.849%                      | 
 | Other 11.136%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 87.794%                     | 
 | Pelipper 85.359%                       | 
 | Seismitoad 85.066%                     | 
 | Omastar 85.059%                        | 
 | Thundurus-Therian 85.059%              | 
 | Corviknight 11.269%                    | 
 | Toxapex  9.728%                        | 
 | Urshifu-Rapid-Strike  9.616%           | 
 | Landorus-Therian  9.471%               | 
 | Heracross  9.469%                      | 
 | Heracross  9.469%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Salamence                              | 
 +----------------------------------------+ 
 | Raw count: 575                         | 
 | Avg. weight: 0.00594481572062          | 
 | Viability Ceiling: 77                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Moxie 90.964%                          | 
 | Intimidate  9.036%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 90.642%               | 
 | Weakness Policy  5.186%                | 
 | Other  4.173%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:60/252/0/0/0/196 68.979%       | 
 | Jolly:0/252/0/0/4/252 14.775%          | 
 | Timid:0/0/0/252/4/252  5.881%          | 
 | Adamant:252/72/0/0/0/184  5.084%       | 
 | Jolly:8/232/12/0/4/252  2.643%         | 
 | Other  2.637%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Dragon Dance 94.098%                   | 
 | Earthquake 93.990%                     | 
 | Dual Wingbeat 89.407%                  | 
 | Thunder Fang 68.979%                   | 
 | Outrage 17.481%                        | 
 | Dragon Claw  7.163%                    | 
 | Draco Meteor  5.674%                   | 
 | Hurricane  5.673%                      | 
 | Other 17.535%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Victini 68.979%                        | 
 | Rillaboom 68.979%                      | 
 | Scizor 68.979%                         | 
 | Volcanion 68.979%                      | 
 | Hippowdon 68.979%                      | 
 | Krookodile 18.249%                     | 
 | Gyarados 14.791%                       | 
 | Necrozma 14.775%                       | 
 | Cobalion 14.774%                       | 
 | Scolipede 14.774%                      | 
 | Ferrothorn  7.294%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Omastar                                | 
 +----------------------------------------+ 
 | Raw count: 44                          | 
 | Avg. weight: 0.0750514613477           | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Swift Swim 100.000%                    | 
 | Weak Armor  0.000%                     | 
 | Shell Armor  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Air Balloon 91.860%                    | 
 | White Herb  8.140%                     | 
 | Other  0.001%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 100.000%        | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shell Smash 100.000%                   | 
 | Earth Power 100.000%                   | 
 | Ice Beam 99.999%                       | 
 | Hydro Pump 91.860%                     | 
 | Other  8.141%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Pelipper 91.860%                       | 
 | Thundurus-Therian 91.860%              | 
 | Inteleon 91.860%                       | 
 | Ferrothorn 91.860%                     | 
 | Seismitoad 91.860%                     | 
 | Mew  8.140%                            | 
 | Kartana  8.140%                        | 
 | Kartana  8.140%                        | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Scrafty                                | 
 +----------------------------------------+ 
 | Raw count: 130                         | 
 | Avg. weight: 0.0250838640575           | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Shed Skin 91.804%                      | 
 | Moxie  8.196%                          | 
 | Intimidate  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 93.932%                      | 
 | Sitrus Berry  6.061%                   | 
 | Other  0.007%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:192/252/0/0/4/60 90.926%       | 
 | Adamant:0/252/0/0/4/252  6.048%        | 
 | Other  3.026%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Dragon Dance 96.995%                   | 
 | Crunch 96.979%                         | 
 | Ice Punch 90.926%                      | 
 | High Jump Kick 90.926%                 | 
 | Poison Jab  6.062%                     | 
 | Other 18.111%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Volcarona 96.973%                      | 
 | Blaziken 90.927%                       | 
 | Slurpuff 90.926%                       | 
 | Mew 90.926%                            | 
 | Blissey 90.926%                        | 
 | Dragapult  7.868%                      | 
 | Rotom-Wash  7.867%                     | 
 | Rotom-Wash  7.867%                     | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Drapion                                | 
 +----------------------------------------+ 
 | Raw count: 158                         | 
 | Avg. weight: 0.0183968883667           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Battle Armor 98.734%                   | 
 | Sniper  1.266%                         | 
 | Keen Eye  0.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Chesto Berry 98.727%                   | 
 | Other  1.273%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:248/0/20/0/180/60 98.727%       | 
 | Other  1.273%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 99.999%                      | 
 | Rest 98.727%                           | 
 | Acupressure 98.727%                    | 
 | Iron Defense 98.727%                   | 
 | Other  3.820%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 99.360%                      | 
 | Landorus-Therian 98.727%               | 
 | Keldeo 98.727%                         | 
 | Clefable 98.727%                       | 
 | Jirachi 98.727%                        | 
 | Jirachi 98.727%                        | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Metagross                              | 
 +----------------------------------------+ 
 | Raw count: 540                         | 
 | Avg. weight: 0.00503806970513          | 
 | Viability Ceiling: 83                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Clear Body 99.998%                     | 
 | Light Metal  0.002%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 54.733%                      | 
 | Choice Scarf 44.013%                   | 
 | Other  1.254%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:252/0/48/0/208/0 44.013%       | 
 | Adamant:252/160/0/0/0/96 32.027%       | 
 | Jolly:252/0/32/0/0/224 21.565%         | 
 | Other  2.394%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Bullet Punch 77.052%                   | 
 | Rest 65.618%                           | 
 | Meteor Mash 55.392%                    | 
 | Trick 44.013%                          | 
 | Block 44.013%                          | 
 | Stealth Rock 33.241%                   | 
 | Earthquake 33.007%                     | 
 | Body Press 21.605%                     | 
 | Cosmic Power 21.605%                   | 
 | Other  4.454%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Buzzwole 53.592%                       | 
 | Volcarona 40.687%                      | 
 | Ninetales-Alola 40.499%                | 
 | Mantine 40.499%                        | 
 | Quagsire 40.499%                       | 
 | Xatu 40.499%                           | 
 | Rotom-Wash 32.585%                     | 
 | Tyranitar 32.027%                      | 
 | Blacephalon 32.027%                    | 
 | Nidoking 32.027%                       | 
 | Clefable 21.694%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Machamp                                | 
 +----------------------------------------+ 
 | Raw count: 319                         | 
 | Avg. weight: 0.00804473899636          | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Guts 53.181%                           | 
 | No Guard 46.819%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 99.700%                    | 
 | Other  0.300%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/0/252 98.333%        | 
 | Other  1.667%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Ice Punch 98.349%                      | 
 | Heavy Slam 98.333%                     | 
 | Stone Edge 62.808%                     | 
 | Close Combat 53.048%                   | 
 | Knock Off 38.283%                      | 
 | Cross Chop 31.097%                     | 
 | Other 18.081%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 98.309%               | 
 | Rotom-Wash 96.949%                     | 
 | Dragapult 96.936%                      | 
 | Ferrothorn 96.936%                     | 
 | Clefable 96.935%                       | 
 | Clefable 96.935%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Stakataka                              | 
 +----------------------------------------+ 
 | Raw count: 361                         | 
 | Avg. weight: 0.00674837828655          | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Beast Boost 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Air Balloon 79.934%                    | 
 | Leftovers 17.501%                      | 
 | Other  2.566%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Lonely:252/252/0/0/4/0 40.816%         | 
 | Brave:252/252/0/0/4/0 39.775%          | 
 | Careful:252/4/0/0/252/0 12.846%        | 
 | Relaxed:252/0/252/0/4/0  2.985%        | 
 | Other  3.578%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Gyro Ball 96.441%                      | 
 | Trick Room 85.824%                     | 
 | Stone Edge 72.905%                     | 
 | Earthquake 46.129%                     | 
 | Heat Crash 44.128%                     | 
 | Stealth Rock 13.270%                   | 
 | Toxic 12.982%                          | 
 | Zen Headbutt 12.846%                   | 
 | Other 15.476%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Glastrier 40.440%                      | 
 | Cresselia 38.358%                      | 
 | Melmetal 38.182%                       | 
 | Crawdaunt 37.929%                      | 
 | Suicune 37.591%                        | 
 | Dragapult 33.473%                      | 
 | Drifblim 33.410%                       | 
 | Tapu Lele 33.410%                      | 
 | Kartana 31.583%                        | 
 | Garchomp 17.933%                       | 
 | Weavile 17.933%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mimikyu                                | 
 +----------------------------------------+ 
 | Raw count: 922                         | 
 | Avg. weight: 0.00265053828906          | 
 | Viability Ceiling: 74                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Disguise 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 31.233%                      | 
 | Salac Berry 28.217%                    | 
 | Red Card 26.217%                       | 
 | Life Orb 12.208%                       | 
 | Other  2.124%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/0/252 28.659%          | 
 | Jolly:0/252/4/0/0/252 26.362%          | 
 | Jolly:4/252/0/0/0/252 25.462%          | 
 | Jolly:0/252/0/0/4/252 11.120%          | 
 | Adamant:0/252/4/0/0/252  2.901%        | 
 | Hardy:4/252/0/0/0/252  2.888%          | 
 | Other  2.608%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Play Rough 99.994%                     | 
 | Swords Dance 97.122%                   | 
 | Shadow Sneak 80.588%                   | 
 | Shadow Claw 60.294%                    | 
 | Drain Punch 36.855%                    | 
 | Endure 17.942%                         | 
 | Other  7.205%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Gyarados 31.135%                       | 
 | Conkeldurr 30.484%                     | 
 | Ferrothorn 28.277%                     | 
 | Heatran 26.711%                        | 
 | Kommo-o 26.217%                        | 
 | Klefki 26.217%                         | 
 | Gastrodon 26.217%                      | 
 | Xatu 26.217%                           | 
 | Duraludon 25.213%                      | 
 | Butterfree 23.434%                     | 
 | Quagsire 23.434%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Lycanroc-Dusk                          | 
 +----------------------------------------+ 
 | Raw count: 207                         | 
 | Avg. weight: 0.0112536035881           | 
 | Viability Ceiling: 88                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Tough Claws 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 81.718%                       | 
 | Focus Sash 14.303%                     | 
 | Other  3.979%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/4/0/0/252 81.302%          | 
 | Jolly:4/252/0/0/0/252  8.443%          | 
 | Jolly:0/252/0/0/4/252  5.889%          | 
 | Other  4.367%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Accelerock 99.991%                     | 
 | Close Combat 85.474%                   | 
 | Psychic Fangs 81.310%                  | 
 | Swords Dance 81.303%                   | 
 | Stealth Rock 14.303%                   | 
 | Endeavor 14.303%                       | 
 | Taunt 14.132%                          | 
 | Other  9.185%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Weavile 84.847%                        | 
 | Dragonite 81.303%                      | 
 | Slowbro 81.302%                        | 
 | Excadrill 81.302%                      | 
 | Nihilego 81.302%                       | 
 | Ninetales-Alola  7.924%                | 
 | Volcarona  4.386%                      | 
 | Blacephalon  4.172%                    | 
 | Dragapult  4.162%                      | 
 | Blaziken  4.155%                       | 
 | Garchomp  3.769%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Rotom-Heat                             | 
 +----------------------------------------+ 
 | Raw count: 520                         | 
 | Avg. weight: 0.00394429109868          | 
 | Viability Ceiling: 86                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 36.638%               | 
 | Ring Target 28.661%                    | 
 | Leftovers 19.853%                      | 
 | Life Orb 10.656%                       | 
 | Other  4.193%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 62.805%          | 
 | Modest:248/0/0/252/0/8 18.084%         | 
 | Calm:252/0/120/0/134/0 12.873%         | 
 | Calm:248/0/4/0/40/192  1.844%          | 
 | Other  4.394%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Overheat 100.000%                      | 
 | Volt Switch 99.581%                    | 
 | Defog 65.149%                          | 
 | Will-O-Wisp 46.126%                    | 
 | Pain Split 32.083%                     | 
 | Trick 30.515%                          | 
 | Thunderbolt 11.652%                    | 
 | Other 14.894%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 58.184%                    | 
 | Toxapex 55.059%                        | 
 | Clefable 48.019%                       | 
 | Ferrothorn 47.315%                     | 
 | Hippowdon 42.150%                      | 
 | Dragapult 40.738%                      | 
 | Tapu Koko 29.080%                      | 
 | Mamoswine 28.661%                      | 
 | Regieleki 28.661%                      | 
 | Hawlucha 28.661%                       | 
 | Weavile 17.489%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Tentacruel                             | 
 +----------------------------------------+ 
 | Raw count: 180                         | 
 | Avg. weight: 0.0122715402402           | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Liquid Ooze 99.191%                    | 
 | Clear Body  0.809%                     | 
 | Rain Dish  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Black Sludge 99.430%                   | 
 | Other  0.570%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:252/0/0/4/0/252 80.446%          | 
 | Calm:252/0/0/0/240/16 18.464%          | 
 | Other  1.090%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Rapid Spin 100.000%                    | 
 | Toxic 98.353%                          | 
 | Toxic Spikes 81.639%                   | 
 | Scald 81.375%                          | 
 | Sludge Wave 18.068%                    | 
 | Acid Armor 17.907%                     | 
 | Other  2.660%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Corviknight 67.058%                    | 
 | Diggersby 67.046%                      | 
 | Slowbro 67.046%                        | 
 | Vanilluxe 67.046%                      | 
 | Regieleki 35.923%                      | 
 | Rillaboom 22.435%                      | 
 | Kommo-o 17.907%                        | 
 | Meowstic 17.907%                       | 
 | Decidueye 17.907%                      | 
 | Polteageist 17.907%                    | 
 | Ninjask 17.907%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Lanturn                                | 
 +----------------------------------------+ 
 | Raw count: 277                         | 
 | Avg. weight: 0.00827774366423          | 
 | Viability Ceiling: 75                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Volt Absorb 99.993%                    | 
 | Water Absorb  0.007%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 96.355%                      | 
 | Other  3.645%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:248/0/20/0/240/0 96.125%          | 
 | Other  3.875%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 99.829%                          | 
 | Volt Switch 99.765%                    | 
 | Heal Bell 96.136%                      | 
 | Thunder Wave 96.125%                   | 
 | Other  8.145%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Bulu 76.260%                      | 
 | Tornadus-Therian 76.260%               | 
 | Heatran 76.260%                        | 
 | Clefable 76.260%                       | 
 | Kartana 76.260%                        | 
 | Pelipper  3.771%                       | 
 | Kingdra  3.679%                        | 
 | Crawdaunt  3.623%                      | 
 | Ferrothorn  3.623%                     | 
 | Togekiss  3.623%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Cobalion                               | 
 +----------------------------------------+ 
 | Raw count: 160                         | 
 | Avg. weight: 0.0111910375742           | 
 | Viability Ceiling: 77                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Justified 100.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Occa Berry 71.625%                     | 
 | Shuca Berry 28.204%                    | 
 | Other  0.171%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:252/0/0/0/4/252 71.625%          | 
 | Jolly:0/252/0/0/4/252 28.375%          | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Close Combat 99.995%                   | 
 | Stealth Rock 71.628%                   | 
 | Thunder Wave 71.625%                   | 
 | Taunt 71.625%                          | 
 | Swords Dance 28.372%                   | 
 | Stone Edge 28.204%                     | 
 | Megahorn 28.204%                       | 
 | Other  0.348%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 71.793%                      | 
 | Tapu Lele 71.628%                      | 
 | Victini 71.625%                        | 
 | Melmetal 71.625%                       | 
 | Kartana 71.625%                        | 
 | Gyarados 28.367%                       | 
 | Krookodile 28.204%                     | 
 | Scolipede 28.204%                      | 
 | Salamence 28.204%                      | 
 | Necrozma 28.204%                       | 
 | Necrozma 28.204%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Slowbro-Galar                          | 
 +----------------------------------------+ 
 | Raw count: 316                         | 
 | Avg. weight: 0.00593087732651          | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Quick Draw 99.990%                     | 
 | Regenerator  0.007%                    | 
 | Own Tempo  0.003%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Quick Claw 92.579%                     | 
 | Sitrus Berry  7.401%                   | 
 | Other  0.020%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:212/0/0/252/0/44 55.644%        | 
 | Modest:4/0/0/252/252/0 36.793%         | 
 | Brave:252/252/4/0/0/0  7.400%          | 
 | Other  0.162%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Nasty Plot 55.713%                     | 
 | Focus Blast 55.711%                    | 
 | Psyshock 55.645%                       | 
 | Sludge Bomb 55.644%                    | 
 | Psychic 36.935%                        | 
 | Shell Side Arm 36.885%                 | 
 | Flamethrower 36.872%                   | 
 | Calm Mind 36.793%                      | 
 | Drain Punch  7.411%                    | 
 | Belly Drum  7.407%                     | 
 | Other 14.984%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Garchomp 55.648%                       | 
 | Urshifu-Rapid-Strike 55.648%           | 
 | Moltres-Galar 55.644%                  | 
 | Melmetal 55.644%                       | 
 | Pelipper 55.644%                       | 
 | Zapdos-Galar 30.273%                   | 
 | Mimikyu 30.270%                        | 
 | Butterfree 30.270%                     | 
 | Celesteela 30.270%                     | 
 | Quagsire 30.270%                       | 
 | Dragapult  7.465%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Jellicent                              | 
 +----------------------------------------+ 
 | Raw count: 193                         | 
 | Avg. weight: 0.00907547350071          | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Water Absorb 100.000%                  | 
 | Cursed Body  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.992%                      | 
 | Other  0.008%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:248/0/104/0/56/100 94.094%        | 
 | Calm:252/0/0/0/252/0  5.015%           | 
 | Other  0.891%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Will-O-Wisp 99.340%                    | 
 | Recover 94.652%                        | 
 | Hex 94.610%                            | 
 | Taunt 94.383%                          | 
 | Other 17.015%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 99.394%                     | 
 | Landorus-Therian 94.109%               | 
 | Porygon-Z 94.094%                      | 
 | Tapu Koko 94.094%                      | 
 | Dragonite 94.094%                      | 
 | Dragonite 94.094%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Dragalge                               | 
 +----------------------------------------+ 
 | Raw count: 51                          | 
 | Avg. weight: 0.0343129258179           | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Adaptability 100.000%                  | 
 | Poison Point  0.000%                   | 
 | Poison Touch  0.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 99.717%                   | 
 | Other  0.283%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:120/0/0/252/0/136 54.517%       | 
 | Modest:252/0/0/252/4/0 43.615%         | 
 | Other  1.867%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Draco Meteor 100.000%                  | 
 | Flip Turn 99.301%                      | 
 | Focus Blast 56.102%                    | 
 | Sludge Wave 44.597%                    | 
 | Thunderbolt 44.597%                    | 
 | Dragon Tail 30.314%                    | 
 | Sludge Bomb 25.088%                    | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 96.857%                       | 
 | Urshifu-Rapid-Strike 53.525%           | 
 | Rillaboom 53.242%                      | 
 | Landorus-Therian 53.242%               | 
 | Corviknight 53.242%                    | 
 | Crawdaunt 44.310%                      | 
 | Mew 44.310%                            | 
 | Volcarona 43.615%                      | 
 | Melmetal 43.615%                       | 
 | Melmetal 43.615%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Galvantula                             | 
 +----------------------------------------+ 
 | Raw count: 543                         | 
 | Avg. weight: 0.0033001099228           | 
 | Viability Ceiling: 72                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Compound Eyes 79.088%                  | 
 | Swarm 20.347%                          | 
 | Unnerve  0.565%                        | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 99.010%                     | 
 | Other  0.990%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 97.733%          | 
 | Other  2.267%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Sticky Web 99.873%                     | 
 | Bug Buzz 93.490%                       | 
 | Thunder 78.964%                        | 
 | Thunder Wave 74.138%                   | 
 | Volt Switch 24.591%                    | 
 | Thunderbolt 20.303%                    | 
 | Other  8.641%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Rillaboom 86.724%                      | 
 | Excadrill 72.458%                      | 
 | Moltres-Galar 68.231%                  | 
 | Urshifu-Rapid-Strike 66.327%           | 
 | Garchomp 66.244%                       | 
 | Nidoking 24.247%                       | 
 | Bisharp 20.268%                        | 
 | Heatran 20.268%                        | 
 | Hawlucha 20.268%                       | 
 | Gyarados  5.691%                       | 
 | Volcarona  3.197%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Zarude                                 | 
 +----------------------------------------+ 
 | Raw count: 124                         | 
 | Avg. weight: 0.0134666763953           | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Leaf Guard 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 92.437%                    | 
 | Choice Scarf  3.510%                   | 
 | Other  4.053%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 93.497%        | 
 | Jolly:0/252/0/0/4/252  4.461%          | 
 | Other  2.042%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Darkest Lariat 100.000%                | 
 | U-turn 97.906%                         | 
 | Close Combat 90.015%                   | 
 | Grassy Glide 89.987%                   | 
 | Power Whip  5.677%                     | 
 | Other 16.415%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Heatran 90.287%                        | 
 | Rillaboom 89.987%                      | 
 | Zeraora 89.987%                        | 
 | Victini 89.987%                        | 
 | Ninetales-Alola 89.987%                | 
 | Zapdos  4.706%                         | 
 | Necrozma  4.431%                       | 
 | Krookodile  4.406%                     | 
 | Toxapex  4.406%                        | 
 | Blaziken  4.406%                       | 
 | Slowking-Galar  2.859%                 | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Vanilluxe                              | 
 +----------------------------------------+ 
 | Raw count: 56                          | 
 | Avg. weight: 0.0351121858979           | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Snow Warning 100.000%                  | 
 | Weak Armor  0.000%                     | 
 | Ice Body  0.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 90.371%                   | 
 | Choice Specs  9.621%                   | 
 | Other  0.007%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Naive:0/0/4/252/0/252 90.371%          | 
 | Modest:64/0/0/252/4/188  9.621%        | 
 | Other  0.007%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Freeze-Dry 100.000%                    | 
 | Blizzard 100.000%                      | 
 | Aurora Veil 99.993%                    | 
 | Ice Shard 90.371%                      | 
 | Other  9.636%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Diggersby 75.317%                      | 
 | Tentacruel 75.317%                     | 
 | Slowbro 75.317%                        | 
 | Corviknight 75.317%                    | 
 | Regieleki 40.355%                      | 
 | Rillaboom 25.189%                      | 
 | Zapdos-Galar  9.773%                   | 
 | Toxapex  7.286%                        | 
 | Tornadus-Therian  7.286%               | 
 | Weavile  7.286%                        | 
 | Melmetal  7.286%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Milotic                                | 
 +----------------------------------------+ 
 | Raw count: 546                         | 
 | Avg. weight: 0.00332753292275          | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Marvel Scale 95.797%                   | 
 | Competitive  4.031%                    | 
 | Cute Charm  0.173%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 97.073%                      | 
 | Other  2.927%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Relaxed:252/0/188/0/68/0 53.179%       | 
 | Calm:252/0/4/0/252/0 40.474%           | 
 | Serious:136/0/0/224/148/0  3.164%      | 
 | Other  3.183%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Recover 98.260%                        | 
 | Haze 97.728%                           | 
 | Toxic 55.358%                          | 
 | Flip Turn 53.366%                      | 
 | Scald 46.605%                          | 
 | Ice Beam 45.981%                       | 
 | Other  2.701%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Lele 82.520%                      | 
 | Landorus-Therian 82.115%               | 
 | Kartana 42.936%                        | 
 | Dragapult 41.809%                      | 
 | Melmetal 41.657%                       | 
 | Corviknight 40.621%                    | 
 | Buzzwole 40.459%                       | 
 | Slowking-Galar 40.459%                 | 
 | Zapdos  3.344%                         | 
 | Scizor  3.236%                         | 
 | Weavile  3.164%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Kingdra                                | 
 +----------------------------------------+ 
 | Raw count: 899                         | 
 | Avg. weight: 0.00181236292741          | 
 | Viability Ceiling: 81                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Swift Swim 99.851%                     | 
 | Sniper  0.149%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 83.325%                   | 
 | Life Orb 13.910%                       | 
 | Other  2.765%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 81.319%         | 
 | Modest:24/0/0/252/0/232  5.099%        | 
 | Modest:84/0/0/252/0/172  4.244%        | 
 | Modest:4/0/0/252/0/252  3.668%         | 
 | Modest:0/0/0/252/0/252  3.196%         | 
 | Other  2.474%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Hydro Pump 93.940%                     | 
 | Draco Meteor 91.558%                   | 
 | Ice Beam 61.428%                       | 
 | Flash Cannon 52.738%                   | 
 | Surf 30.827%                           | 
 | Flip Turn 24.678%                      | 
 | Hurricane 22.658%                      | 
 | Scald 11.893%                          | 
 | Other 10.279%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Pelipper 82.286%                       | 
 | Scizor 59.593%                         | 
 | Barraskewda 58.482%                    | 
 | Seismitoad 50.507%                     | 
 | Slowking-Galar 27.021%                 | 
 | Ferrothorn 23.219%                     | 
 | Zapdos 16.763%                         | 
 | Toxicroak 16.383%                      | 
 | Melmetal 14.170%                       | 
 | Landorus-Therian 11.888%               | 
 | Volcanion 11.888%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Regigigas                              | 
 +----------------------------------------+ 
 | Raw count: 76                          | 
 | Avg. weight: 0.0217451286488           | 
 | Viability Ceiling: 84                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Slow Start 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.990%                      | 
 | Other  0.010%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:224/252/28/0/0/4 53.123%       | 
 | Careful:252/0/4/0/252/0 46.867%        | 
 | Other  0.010%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Protect 53.123%                        | 
 | Earthquake 53.123%                     | 
 | Substitute 53.123%                     | 
 | Heat Crash 53.123%                     | 
 | Rest 46.877%                           | 
 | Body Slam 46.877%                      | 
 | Sleep Talk 46.867%                     | 
 | Knock Off 46.867%                      | 
 | Other  0.019%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 93.657%               | 
 | Rillaboom 55.223%                      | 
 | Dragapult 46.962%                      | 
 | Slowbro 46.956%                        | 
 | Clefable 46.956%                       | 
 | Corviknight 46.694%                    | 
 | Tapu Lele 46.694%                      | 
 | Toxapex 46.694%                        | 
 | Magnezone 25.393%                      | 
 | Heatran 13.046%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Comfey                                 | 
 +----------------------------------------+ 
 | Raw count: 12                          | 
 | Avg. weight: 0.117676919294            | 
 | Viability Ceiling: 87                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Triage 100.000%                        | 
 | Flower Veil  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 68.885%                       | 
 | Leftovers 31.115%                      | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 68.885%          | 
 | Modest:252/0/4/252/0/0 31.115%         | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Calm Mind 100.000%                     | 
 | Draining Kiss 100.000%                 | 
 | Giga Drain 100.000%                    | 
 | Stored Power 68.885%                   | 
 | Protect 31.115%                        | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Volcarona 68.885%                      | 
 | Dragonite 68.885%                      | 
 | Weavile 68.885%                        | 
 | Mew 68.885%                            | 
 | Scizor 68.885%                         | 
 | Dragapult 31.115%                      | 
 | Melmetal 31.115%                       | 
 | Zoroark 31.115%                        | 
 | Absol 31.115%                          | 
 | Rillaboom 31.115%                      | 
 | Rillaboom 31.115%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Glastrier                              | 
 +----------------------------------------+ 
 | Raw count: 160                         | 
 | Avg. weight: 0.00919386685667          | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Chilling Neigh 100.000%                | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 66.996%                       | 
 | Heavy-Duty Boots 32.393%               | 
 | Other  0.611%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Brave:248/252/0/0/8/0 76.955%          | 
 | Adamant:192/252/0/0/0/64 11.560%       | 
 | Adamant:248/252/0/0/8/0  6.210%        | 
 | Brave:0/252/252/0/4/0  4.719%          | 
 | Other  0.555%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Close Combat 100.000%                  | 
 | Swords Dance 93.790%                   | 
 | High Horsepower 91.149%                | 
 | Icicle Spear 73.837%                   | 
 | Icicle Crash 25.554%                   | 
 | Other 15.670%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Melmetal 73.814%                       | 
 | Stakataka 66.973%                      | 
 | Cresselia 62.254%                      | 
 | Crawdaunt 62.254%                      | 
 | Suicune 62.254%                        | 
 | Landorus-Therian 26.262%               | 
 | Hatterene 19.421%                      | 
 | Audino 14.702%                         | 
 | Toxapex 14.702%                        | 
 | Druddigon 14.702%                      | 
 | Aegislash 11.560%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Avalugg                                | 
 +----------------------------------------+ 
 | Raw count: 109                         | 
 | Avg. weight: 0.0117749093623           | 
 | Viability Ceiling: 79                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sturdy 99.079%                         | 
 | Own Tempo  0.873%                      | 
 | Ice Body  0.048%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 98.801%               | 
 | Other  1.199%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/4/252/0/0/0 96.820%         | 
 | Other  3.180%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Recover 98.823%                        | 
 | Mirror Coat 95.933%                    | 
 | Rapid Spin 82.403%                     | 
 | Avalanche 72.757%                      | 
 | Body Press 30.706%                     | 
 | Other 19.379%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ninetales-Alola 96.423%                | 
 | Arctozolt 96.021%                      | 
 | Aurorus 95.955%                        | 
 | Cloyster 95.933%                       | 
 | Eiscue 77.008%                         | 
 | Sandslash-Alola 19.388%                | 
 | Sandslash-Alola 19.388%                | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Entei                                  | 
 +----------------------------------------+ 
 | Raw count: 135                         | 
 | Avg. weight: 0.00909030220575          | 
 | Viability Ceiling: 77                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Pressure 87.014%                       | 
 | Inner Focus 12.986%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 87.005%                      | 
 | Choice Band 11.957%                    | 
 | Other  1.037%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:248/0/8/0/0/252 87.005%          | 
 | Jolly:0/252/0/0/4/252 11.949%          | 
 | Other  1.046%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Calm Mind 87.007%                      | 
 | Substitute 87.005%                     | 
 | Protect 87.005%                        | 
 | Lava Plume 87.005%                     | 
 | Extreme Speed 12.993%                  | 
 | Sacred Fire 12.993%                    | 
 | Stomping Tantrum 11.396%               | 
 | Other 14.594%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Suicune 87.005%                        | 
 | Weavile 87.005%                        | 
 | Raikou 87.005%                         | 
 | Cresselia 87.005%                      | 
 | Bisharp 87.005%                        | 
 | Moltres-Galar 10.805%                  | 
 | Rotom-Mow 10.805%                      | 
 | Duraludon 10.805%                      | 
 | Toxtricity 10.805%                     | 
 | Toxtricity 10.805%                     | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Incineroar                             | 
 +----------------------------------------+ 
 | Raw count: 1185                        | 
 | Avg. weight: 0.001073449115            | 
 | Viability Ceiling: 71                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Intimidate 97.788%                     | 
 | Blaze  2.212%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Aguav Berry 43.456%                    | 
 | Heavy-Duty Boots 16.288%               | 
 | Iapapa Berry 15.126%                   | 
 | Sitrus Berry 11.822%                   | 
 | Leftovers  8.143%                      | 
 | Protective Pads  2.244%                | 
 | Other  2.922%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 58.107%          | 
 | Careful:252/4/0/0/252/0 13.907%        | 
 | Careful:136/120/0/0/252/0 13.580%      | 
 | Adamant:248/252/0/0/4/0  5.441%        | 
 | Calm:252/0/0/0/232/24  2.244%          | 
 | Impish:252/0/100/0/156/0  1.591%       | 
 | Other  5.131%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 80.616%                      | 
 | Drain Punch 47.088%                    | 
 | Flame Charge 45.079%                   | 
 | Swords Dance 41.114%                   | 
 | Parting Shot 35.895%                   | 
 | Will-O-Wisp 27.499%                    | 
 | Bulk Up 25.746%                        | 
 | Darkest Lariat 18.371%                 | 
 | Fake Out 16.412%                       | 
 | Acrobatics 15.036%                     | 
 | Earthquake 14.516%                     | 
 | Flare Blitz 13.250%                    | 
 | Other 19.378%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Bulu 37.379%                      | 
 | Volcarona 37.283%                      | 
 | Kommo-o 37.216%                        | 
 | Nihilego 37.215%                       | 
 | Bronzong 37.215%                       | 
 | Dragonite 31.243%                      | 
 | Urshifu-Rapid-Strike 30.881%           | 
 | Rillaboom 19.307%                      | 
 | Dragapult 15.497%                      | 
 | Toxapex 15.104%                        | 
 | Shuckle 15.036%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mantine                                | 
 +----------------------------------------+ 
 | Raw count: 174                         | 
 | Avg. weight: 0.00691397577162          | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Water Absorb 99.991%                   | 
 | Swift Swim  0.009%                     | 
 | Water Veil  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.651%                      | 
 | Other  0.349%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:252/0/76/0/180/0 99.532%          | 
 | Other  0.468%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 99.970%                          | 
 | Defog 99.970%                          | 
 | Rest 99.532%                           | 
 | Haze 99.532%                           | 
 | Other  0.996%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Quagsire 91.585%                       | 
 | Volcarona 91.585%                      | 
 | Xatu 91.585%                           | 
 | Ninetales-Alola 91.585%                | 
 | Metagross 91.585%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Corsola-Galar                          | 
 +----------------------------------------+ 
 | Raw count: 201                         | 
 | Avg. weight: 0.00598553713676          | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Cursed Body 99.965%                    | 
 | Weak Armor  0.035%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Eviolite 100.000%                      | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/6/0 58.482%           | 
 | Calm:252/0/4/0/252/0 22.927%           | 
 | Bold:248/0/252/0/8/0 18.188%           | 
 | Other  0.403%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Strength Sap 100.000%                  | 
 | Stealth Rock 99.768%                   | 
 | Will-O-Wisp 99.564%                    | 
 | Night Shade 87.749%                    | 
 | Other 12.919%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 67.284%                        | 
 | Ferrothorn 67.284%                     | 
 | Ditto 67.284%                          | 
 | Claydol 49.096%                        | 
 | Hatterene 49.096%                      | 
 | Corviknight 35.987%                    | 
 | Tornadus-Therian 18.188%               | 
 | Moltres-Galar 17.671%                  | 
 | Weezing-Galar 17.671%                  | 
 | Appletun 17.671%                       | 
 | Dragapult 10.008%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Goodra                                 | 
 +----------------------------------------+ 
 | Raw count: 315                         | 
 | Avg. weight: 0.00323640272795          | 
 | Viability Ceiling: 77                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sap Sipper 95.219%                     | 
 | Hydration  2.572%                      | 
 | Gooey  2.209%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 97.384%                   | 
 | Other  2.616%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Quiet:144/0/96/252/16/0 92.129%        | 
 | Calm:252/0/4/0/252/0  2.810%           | 
 | Mild:248/0/0/252/8/0  2.800%           | 
 | Other  2.261%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Flamethrower 95.213%                   | 
 | Ice Beam 94.153%                       | 
 | Power Whip 92.129%                     | 
 | Earthquake 51.650%                     | 
 | Thunderbolt 42.912%                    | 
 | Draco Meteor  5.849%                   | 
 | Other 18.095%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Koko 92.137%                      | 
 | Corviknight 92.136%                    | 
 | Swampert 92.129%                       | 
 | Tyranitar 92.129%                      | 
 | Mew 51.650%                            | 
 | Heatran 40.479%                        | 
 | Ferrothorn  5.001%                     | 
 | Pelipper  4.868%                       | 
 | Krookodile  2.572%                     | 
 | Heliolisk  2.572%                      | 
 | Heliolisk  2.572%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Dhelmise                               | 
 +----------------------------------------+ 
 | Raw count: 45                          | 
 | Avg. weight: 0.021698465075            | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Steelworker 100.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 76.549%                   | 
 | Heavy-Duty Boots 23.317%               | 
 | Other  0.133%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:124/220/84/0/64/16 76.549%     | 
 | Impish:248/8/252/0/0/0 23.317%         | 
 | Other  0.134%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Power Whip 99.921%                     | 
 | Anchor Shot 76.654%                    | 
 | Poltergeist 76.603%                    | 
 | Earthquake 76.549%                     | 
 | Rapid Spin 23.347%                     | 
 | Synthesis 23.346%                      | 
 | Knock Off 23.336%                      | 
 | Other  0.244%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Koko 99.866%                      | 
 | Tapu Fini 76.549%                      | 
 | Dragonite 76.549%                      | 
 | Heatran 76.549%                        | 
 | Garchomp 76.549%                       | 
 | Volcarona 23.317%                      | 
 | Mew 23.317%                            | 
 | Swampert 23.317%                       | 
 | Swampert 23.317%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Vaporeon                               | 
 +----------------------------------------+ 
 | Raw count: 117                         | 
 | Avg. weight: 0.00816437980689          | 
 | Viability Ceiling: 77                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Water Absorb 100.000%                  | 
 | Hydration  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.247%                      | 
 | Other  0.753%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Relaxed:252/0/252/0/4/0 99.244%        | 
 | Other  0.756%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Flip Turn 99.805%                      | 
 | Heal Bell 99.246%                      | 
 | Protect 99.246%                        | 
 | Wish 99.245%                           | 
 | Other  2.458%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Urshifu-Rapid-Strike 99.431%           | 
 | Gengar 99.244%                         | 
 | Swampert 99.244%                       | 
 | Corviknight 99.244%                    | 
 | Tapu Lele 99.244%                      | 
 | Tapu Lele 99.244%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Scolipede                              | 
 +----------------------------------------+ 
 | Raw count: 218                         | 
 | Avg. weight: 0.00411941881639          | 
 | Viability Ceiling: 77                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Speed Boost 99.997%                    | 
 | Poison Point  0.003%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 98.230%                     | 
 | Other  1.770%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/132/124/0/0/252 56.235%        | 
 | Timid:252/0/0/0/0/252 21.805%          | 
 | Jolly:248/0/100/0/0/160 20.070%        | 
 | Other  1.890%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Endeavor 98.110%                       | 
 | Spikes 98.110%                         | 
 | Earthquake 57.788%                     | 
 | Poison Jab 56.498%                     | 
 | Substitute 42.947%                     | 
 | Toxic 21.925%                          | 
 | Throat Chop 20.070%                    | 
 | Other  4.552%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Gyarados 56.235%                       | 
 | Necrozma 56.235%                       | 
 | Krookodile 56.235%                     | 
 | Salamence 56.235%                      | 
 | Cobalion 56.235%                       | 
 | Urshifu-Rapid-Strike 41.875%           | 
 | Volcarona 22.921%                      | 
 | Tapu Koko 21.805%                      | 
 | Kartana 21.805%                        | 
 | Dragonite 21.805%                      | 
 | Aegislash 20.190%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Drifblim                               | 
 +----------------------------------------+ 
 | Raw count: 54                          | 
 | Avg. weight: 0.0158793259557           | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Unburden 94.942%                       | 
 | Flare Boost  5.058%                    | 
 | Aftermath  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 94.921%                     | 
 | Flame Orb  5.058%                      | 
 | Other  0.022%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/4/252/0/252 94.921%          | 
 | Modest:0/0/0/252/4/252  5.055%         | 
 | Other  0.025%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Hex 94.921%                            | 
 | Thunder Wave 94.921%                   | 
 | Will-O-Wisp 94.921%                    | 
 | Memento 94.921%                        | 
 | Shadow Ball  5.058%                    | 
 | Other 15.260%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Stakataka 94.921%                      | 
 | Tapu Lele 94.921%                      | 
 | Dragapult 94.921%                      | 
 | Weavile 50.950%                        | 
 | Garchomp 50.950%                       | 
 | Tapu Koko 43.971%                      | 
 | Kartana 43.971%                        | 
 | Mandibuzz  5.055%                      | 
 | Mandibuzz  5.055%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Scyther                                | 
 +----------------------------------------+ 
 | Raw count: 177                         | 
 | Avg. weight: 0.0048352846553           | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Technician 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Band 99.967%                    | 
 | Other  0.033%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 99.971%          | 
 | Other  0.029%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Quick Attack 100.000%                  | 
 | Dual Wingbeat 99.987%                  | 
 | U-turn 99.975%                         | 
 | Knock Off 99.967%                      | 
 | Other  0.071%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragonite 99.967%                      | 
 | Clefable 99.967%                       | 
 | Umbreon 99.967%                        | 
 | Scizor 99.967%                         | 
 | Nidoking 99.967%                       | 
 | Nidoking 99.967%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Cursola                                | 
 +----------------------------------------+ 
 | Raw count: 118                         | 
 | Avg. weight: 0.00703438352347          | 
 | Viability Ceiling: 72                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Perish Body 100.000%                   | 
 | Weak Armor  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 96.593%               | 
 | Other  3.407%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:252/0/4/252/0/0 96.593%         | 
 | Other  3.407%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Hex 98.740%                            | 
 | Will-O-Wisp 97.765%                    | 
 | Stealth Rock 97.765%                   | 
 | Strength Sap 96.593%                   | 
 | Other  9.137%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 96.593%                        | 
 | Weavile 96.593%                        | 
 | Hippowdon 96.593%                      | 
 | Clefable 96.593%                       | 
 | Skarmory 96.593%                       | 
 | Skarmory 96.593%                       | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Heracross                              | 
 +----------------------------------------+ 
 | Raw count: 533                         | 
 | Avg. weight: 0.00150537699204          | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Guts 95.289%                           | 
 | Moxie  4.711%                          | 
 | Swarm  0.000%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Flame Orb 94.354%                      | 
 | Choice Scarf  4.711%                   | 
 | Other  0.935%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:4/252/0/0/0/252 45.218%          | 
 | Jolly:0/252/0/0/4/252 43.173%          | 
 | Adamant:0/252/4/0/0/252  4.508%        | 
 | Adamant:0/252/0/0/4/252  4.329%        | 
 | Other  2.772%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Megahorn 95.482%                       | 
 | Facade 95.242%                         | 
 | Close Combat 91.788%                   | 
 | Knock Off 45.129%                      | 
 | Spikes 42.088%                         | 
 | Brick Break  8.212%                    | 
 | Bulk Up  8.212%                        | 
 | Other 13.847%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 81.680%               | 
 | Ferrothorn 47.565%                     | 
 | Garchomp 44.100%                       | 
 | Urshifu-Rapid-Strike 43.097%           | 
 | Toxapex 42.088%                        | 
 | Inteleon 42.088%                       | 
 | Corviknight 42.088%                    | 
 | Slowbro 39.592%                        | 
 | Tapu Lele 39.592%                      | 
 | Linoone  7.973%                        | 
 | Salamence  7.973%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Talonflame                             | 
 +----------------------------------------+ 
 | Raw count: 250                         | 
 | Avg. weight: 0.00315194717233          | 
 | Viability Ceiling: 72                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Flame Body 98.506%                     | 
 | Gale Wings  1.494%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 99.125%               | 
 | Other  0.875%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:248/0/0/8/0/252 96.263%          | 
 | Other  3.737%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Defog 99.278%                          | 
 | U-turn 98.251%                         | 
 | Flamethrower 96.263%                   | 
 | Roost 91.761%                          | 
 | Other 14.447%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Buzzwole 94.305%                       | 
 | Landorus-Therian 94.293%               | 
 | Blissey 94.293%                        | 
 | Tapu Lele 94.293%                      | 
 | Ferrothorn 88.148%                     | 
 | Tangrowth  6.923%                      | 
 | Kommo-o  2.059%                        | 
 | Krookodile  2.059%                     | 
 | Krookodile  2.059%                     | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Duraludon                              | 
 +----------------------------------------+ 
 | Raw count: 77                          | 
 | Avg. weight: 0.00999103931002          | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Light Metal 80.764%                    | 
 | Stalwart 19.236%                       | 
 | Heavy Metal  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 81.478%                   | 
 | Focus Sash 17.236%                     | 
 | Other  1.286%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 80.760%          | 
 | Bold:4/0/252/252/0/0 17.236%           | 
 | Other  2.003%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Thunderbolt 82.763%                    | 
 | Flash Cannon 82.763%                   | 
 | Dragon Pulse 82.016%                   | 
 | Dark Pulse 80.751%                     | 
 | Draco Meteor 19.249%                   | 
 | Body Press 17.975%                     | 
 | Stealth Rock 17.237%                   | 
 | Other 17.246%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mimikyu 80.091%                        | 
 | Gyarados 80.082%                       | 
 | Conkeldurr 78.010%                     | 
 | Ferrothorn 72.640%                     | 
 | Haxorus 62.516%                        | 
 | Moltres-Galar 17.237%                  | 
 | Toxtricity 17.236%                     | 
 | Melmetal 17.236%                       | 
 | Rotom-Mow 17.236%                      | 
 | Entei 17.236%                          | 
 | Hawlucha 10.124%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Ribombee                               | 
 +----------------------------------------+ 
 | Raw count: 201                         | 
 | Avg. weight: 0.00395543088541          | 
 | Viability Ceiling: 85                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Shield Dust 98.328%                    | 
 | Honey Gather  1.614%                   | 
 | Sweet Veil  0.058%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 48.842%               | 
 | Focus Sash 30.423%                     | 
 | Choice Scarf 16.249%                   | 
 | Other  4.485%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/4/252/0/252 48.757%          | 
 | Timid:248/0/0/8/0/252 27.504%          | 
 | Timid:0/0/0/252/4/252 19.314%          | 
 | Other  4.425%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Moonblast 95.619%                      | 
 | Aromatherapy 76.176%                   | 
 | Sticky Web 51.194%                     | 
 | Quiver Dance 48.836%                   | 
 | Roost 48.757%                          | 
 | Tailwind 28.733%                       | 
 | Trick  9.640%                          | 
 | Defog  8.498%                          | 
 | U-turn  7.027%                         | 
 | Bug Buzz  6.986%                       | 
 | Other 18.535%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 70.929%                     | 
 | Landorus-Therian 50.270%               | 
 | Toxapex 43.470%                        | 
 | Bisharp 43.469%                        | 
 | Zeraora 43.469%                        | 
 | Slowbro 27.464%                        | 
 | Clefable 27.423%                       | 
 | Mew 27.419%                            | 
 | Blissey 27.419%                        | 
 | Excadrill  9.353%                      | 
 | Kartana  8.539%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Shedinja                               | 
 +----------------------------------------+ 
 | Raw count: 434                         | 
 | Avg. weight: 0.00174260468668          | 
 | Viability Ceiling: 79                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Wonder Guard 100.000%                  | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 81.243%               | 
 | Safety Goggles 16.477%                 | 
 | Other  2.280%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 68.099%        | 
 | Adamant:0/252/0/0/0/252 21.342%        | 
 | Modest:0/0/0/252/0/252  4.045%         | 
 | Lonely:0/252/0/0/0/0  1.912%           | 
 | Other  4.602%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Shadow Sneak 78.660%                   | 
 | Swords Dance 68.633%                   | 
 | Shadow Claw 58.841%                    | 
 | X-Scissor 57.815%                      | 
 | Toxic 37.597%                          | 
 | Will-O-Wisp 33.491%                    | 
 | Poltergeist 17.581%                    | 
 | Protect 16.714%                        | 
 | Gust 16.138%                           | 
 | Other 14.530%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 81.642%                        | 
 | Clefable 78.401%                       | 
 | Blissey 66.062%                        | 
 | Slowking-Galar 58.658%                 | 
 | Skarmory 55.382%                       | 
 | Corviknight 25.728%                    | 
 | Chansey 15.209%                        | 
 | Xatu 14.625%                           | 
 | Tapu Fini 11.263%                      | 
 | Ferrothorn 10.675%                     | 
 | Pelipper 10.591%                       | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Zoroark                                | 
 +----------------------------------------+ 
 | Raw count: 234                         | 
 | Avg. weight: 0.00313145858985          | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Illusion 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 61.908%                       | 
 | Ring Target 37.911%                    | 
 | Other  0.181%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/4/252/0/252 97.873%          | 
 | Other  2.127%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Dark Pulse 98.173%                     | 
 | Flamethrower 98.006%                   | 
 | Sludge Bomb 97.993%                    | 
 | Calm Mind 59.962%                      | 
 | Trick 37.911%                          | 
 | Other  7.955%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 97.886%                      | 
 | Melmetal 97.873%                       | 
 | Rillaboom 97.873%                      | 
 | Absol 97.873%                          | 
 | Comfey 59.962%                         | 
 | Regieleki 37.911%                      | 
 | Regieleki 37.911%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Weezing-Galar                          | 
 +----------------------------------------+ 
 | Raw count: 405                         | 
 | Avg. weight: 0.00194082452434          | 
 | Viability Ceiling: 74                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 65.094%                       | 
 | Neutralizing Gas 34.805%               | 
 | Misty Surge  0.101%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Black Sludge 97.841%                   | 
 | Other  2.159%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/252/0/4/0 62.951%           | 
 | Bold:252/0/252/4/0/0 34.637%           | 
 | Other  2.412%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Will-O-Wisp 65.219%                    | 
 | Defog 63.202%                          | 
 | Sludge Bomb 62.943%                    | 
 | Flamethrower 60.808%                   | 
 | Strange Steam 36.963%                  | 
 | Corrosive Gas 34.637%                  | 
 | Haze 34.637%                           | 
 | Taunt 34.637%                          | 
 | Other  6.954%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Urshifu-Rapid-Strike 68.920%           | 
 | Ferrothorn 60.965%                     | 
 | Landorus-Therian 60.900%               | 
 | Tyranitar 60.801%                      | 
 | Vikavolt 60.800%                       | 
 | Moltres-Galar 27.047%                  | 
 | Appletun 27.046%                       | 
 | Corsola-Galar 27.046%                  | 
 | Corviknight 27.046%                    | 
 | Dragapult 14.975%                      | 
 | Latios  6.055%                         | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Absol                                  | 
 +----------------------------------------+ 
 | Raw count: 84                          | 
 | Avg. weight: 0.00854908940339          | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Pressure 99.991%                       | 
 | Justified  0.007%                      | 
 | Super Luck  0.002%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Black Glasses 99.868%                  | 
 | Other  0.132%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/4/0/0/252 99.868%        | 
 | Other  0.132%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Sucker Punch 99.876%                   | 
 | Knock Off 99.874%                      | 
 | Will-O-Wisp 99.868%                    | 
 | Taunt 99.868%                          | 
 | Other  0.514%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Zoroark 99.868%                        | 
 | Dragapult 99.868%                      | 
 | Melmetal 99.868%                       | 
 | Rillaboom 99.868%                      | 
 | Comfey 61.184%                         | 
 | Regieleki 38.684%                      | 
 | Regieleki 38.684%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Toxtricity                             | 
 +----------------------------------------+ 
 | Raw count: 467                         | 
 | Avg. weight: 0.00158577324054          | 
 | Viability Ceiling: 78                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Punk Rock 100.000%                     | 
 | Technician  0.000%                     | 
 | Plus  0.000%                           | 
 | Minus  0.000%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 57.829%                       | 
 | Choice Specs 39.890%                   | 
 | Other  2.281%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 39.770%         | 
 | Rash:0/144/0/180/8/176 39.243%         | 
 | Mild:0/4/0/252/0/252 17.944%           | 
 | Other  3.042%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Boomburst 99.344%                      | 
 | Overdrive 83.910%                      | 
 | Shift Gear 59.272%                     | 
 | Drain Punch 57.196%                    | 
 | Volt Switch 39.871%                    | 
 | Snarl 21.446%                          | 
 | Sludge Wave 20.222%                    | 
 | Other 18.738%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Melmetal 42.066%                       | 
 | Tapu Koko 37.872%                      | 
 | Cloyster 36.766%                       | 
 | Moltres-Galar 31.795%                  | 
 | Garchomp 24.133%                       | 
 | Hawlucha 23.066%                       | 
 | Incineroar 20.350%                     | 
 | Crobat 20.339%                         | 
 | Gardevoir 20.339%                      | 
 | Gastrodon 20.339%                      | 
 | Steelix 20.339%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Heliolisk                              | 
 +----------------------------------------+ 
 | Raw count: 364                         | 
 | Avg. weight: 0.00201392781516          | 
 | Viability Ceiling: 79                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Dry Skin 99.935%                       | 
 | Solar Power  0.065%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 90.312%                       | 
 | Leftovers  4.775%                      | 
 | Other  4.913%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 98.743%          | 
 | Other  1.257%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Thunder 95.078%                        | 
 | Volt Switch 93.959%                    | 
 | Hyper Voice 77.995%                    | 
 | Weather Ball 69.737%                   | 
 | Surf 21.921%                           | 
 | Grass Knot 16.599%                     | 
 | Focus Blast  5.417%                    | 
 | Other 19.296%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Pelipper 96.842%                       | 
 | Barraskewda 93.253%                    | 
 | Ferrothorn 92.054%                     | 
 | Seismitoad 78.340%                     | 
 | Dragapult 69.619%                      | 
 | Zapdos 10.099%                         | 
 | Kingdra 10.099%                        | 
 | Tornadus-Therian  8.721%               | 
 | Urshifu-Rapid-Strike  4.814%           | 
 | Melmetal  4.775%                       | 
 | Thundurus-Therian  4.775%              | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Druddigon                              | 
 +----------------------------------------+ 
 | Raw count: 52                          | 
 | Avg. weight: 0.0158877986695           | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Rough Skin 60.110%                     | 
 | Mold Breaker 39.890%                   | 
 | Sheer Force  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Rocky Helmet 60.110%                   | 
 | Focus Sash 36.884%                     | 
 | Other  3.006%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/0/252/0/0/0 46.930%         | 
 | Adamant:248/0/0/0/104/156 39.890%      | 
 | Impish:252/0/252/0/4/0 13.162%         | 
 | Other  0.019%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Glare 99.997%                          | 
 | Stealth Rock 67.883%                   | 
 | Gunk Shot 60.646%                      | 
 | Taunt 53.056%                          | 
 | Dragon Tail 46.944%                    | 
 | Protect 46.930%                        | 
 | Roar 13.167%                           | 
 | Other 11.378%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Audino 46.930%                         | 
 | Toxapex 46.930%                        | 
 | Landorus-Therian 46.930%               | 
 | Hatterene 46.930%                      | 
 | Melmetal 37.823%                       | 
 | Glastrier 26.177%                      | 
 | Zeraora 24.665%                        | 
 | Hydreigon 24.661%                      | 
 | Volcarona 24.661%                      | 
 | Togekiss 24.661%                       | 
 | Conkeldurr 20.753%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mareanie                               | 
 +----------------------------------------+ 
 | Raw count: 3                           | 
 | Avg. weight: 0.232843425134            | 
 | Viability Ceiling: 82                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 100.000%                   | 
 | Merciless  0.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Eviolite 100.000%                      | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Calm:252/0/4/0/252/0 100.000%          | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Scald 100.000%                         | 
 | Toxic Spikes 100.000%                  | 
 | Poison Jab 100.000%                    | 
 | Recover 100.000%                       | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 100.000%                       | 
 | Reuniclus 100.000%                     | 
 | Tornadus-Therian 100.000%              | 
 | Landorus-Therian 100.000%              | 
 | Dracozolt 100.000%                     | 
 | Dracozolt 100.000%                     | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Audino                                 | 
 +----------------------------------------+ 
 | Raw count: 21                          | 
 | Avg. weight: 0.0315071455134           | 
 | Viability Ceiling: 91                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 100.000%                   | 
 | Healer  0.000%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Heavy-Duty Boots 100.000%              | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:252/4/120/0/132/0 58.599%      | 
 | Careful:252/0/4/0/252/0 41.401%        | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Knock Off 100.000%                     | 
 | Wish 100.000%                          | 
 | Protect 100.000%                       | 
 | Toxic 100.000%                         | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 100.000%              | 
 | Hatterene 58.599%                      | 
 | Toxapex 58.599%                        | 
 | Druddigon 58.599%                      | 
 | Slowbro 41.401%                        | 
 | Skarmory 41.401%                       | 
 | Clefable 41.401%                       | 
 | Dragapult 41.401%                      | 
 | Glastrier 32.685%                      | 
 | Conkeldurr 25.913%                     | 
 | Conkeldurr 25.913%                     | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Darmanitan                             | 
 +----------------------------------------+ 
 | Raw count: 554                         | 
 | Avg. weight: 0.00123377373739          | 
 | Viability Ceiling: 84                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sheer Force 99.869%                    | 
 | Zen Mode  0.131%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 85.917%                   | 
 | Life Orb 13.944%                       | 
 | Other  0.139%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 62.284%          | 
 | Jolly:4/252/0/0/0/252 34.527%          | 
 | Other  3.190%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | U-turn 89.600%                         | 
 | Flare Blitz 86.236%                    | 
 | Earthquake 76.512%                     | 
 | Rock Slide 59.342%                     | 
 | Superpower 42.088%                     | 
 | Fire Punch 14.388%                     | 
 | Stone Edge 11.050%                     | 
 | Iron Head 10.269%                      | 
 | Other 10.516%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 39.089%                      | 
 | Rotom-Wash 38.700%                     | 
 | Dragonite 33.902%                      | 
 | Ferrothorn 30.548%                     | 
 | Cloyster 28.855%                       | 
 | Volcarona 28.846%                      | 
 | Scrafty 28.846%                        | 
 | Corviknight 22.684%                    | 
 | Clefable 22.379%                       | 
 | Pelipper 22.373%                       | 
 | Barraskewda 22.372%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Lickilicky                             | 
 +----------------------------------------+ 
 | Raw count: 12                          | 
 | Avg. weight: 0.0525495486064           | 
 | Viability Ceiling: 79                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Cloud Nine 100.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 100.000%                  | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Brave:252/88/0/0/168/0 100.000%        | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Explosion 100.000%                     | 
 | Steel Roller 100.000%                  | 
 | Seismic Toss 100.000%                  | 
 | Flamethrower 100.000%                  | 
 | Other  0.000%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Blacephalon 100.000%                   | 
 | Melmetal 100.000%                      | 
 | Slowbro 100.000%                       | 
 | Umbreon 100.000%                       | 
 | Landorus-Therian 100.000%              | 
 | Landorus-Therian 100.000%              | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Claydol                                | 
 +----------------------------------------+ 
 | Raw count: 136                         | 
 | Avg. weight: 0.00526366900282          | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 99.809%                   | 
 | Other  0.191%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:252/0/4/252/0/0 98.287%         | 
 | Other  1.713%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Rapid Spin 99.983%                     | 
 | Body Press 98.287%                     | 
 | Earth Power 98.287%                    | 
 | Future Sight 98.287%                   | 
 | Other  5.156%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Toxapex 82.637%                        | 
 | Ferrothorn 82.518%                     | 
 | Hatterene 82.514%                      | 
 | Ditto 82.512%                          | 
 | Corsola-Galar 82.512%                  | 
 | Mew  0.822%                            | 
 | Gengar  0.822%                         | 
 | Scizor  0.822%                         | 
 | Zapdos  0.822%                         | 
 | Kartana  0.822%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Butterfree                             | 
 +----------------------------------------+ 
 | Raw count: 276                         | 
 | Avg. weight: 0.00256001470702          | 
 | Viability Ceiling: 68                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Compound Eyes 100.000%                 | 
 | Tinted Lens  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 97.664%                     | 
 | Other  2.336%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/0/252 97.594%          | 
 | Other  2.406%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Bug Buzz 99.854%                       | 
 | Quiver Dance 99.807%                   | 
 | Hurricane 99.045%                      | 
 | Sleep Powder 98.637%                   | 
 | Other  2.657%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Quagsire 81.053%                       | 
 | Mimikyu 81.053%                        | 
 | Slowbro-Galar 80.291%                  | 
 | Celesteela 80.291%                     | 
 | Zapdos-Galar 80.291%                   | 
 | Durant  1.468%                         | 
 | Volcarona  1.468%                      | 
 | Shuckle  1.363%                        | 
 | Galvantula  1.363%                     | 
 | Scolipede  1.363%                      | 
 | Pikachu  0.780%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mr. Rime                               | 
 +----------------------------------------+ 
 | Raw count: 101                         | 
 | Avg. weight: 0.00572228423387          | 
 | Viability Ceiling: 80                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Screen Cleaner 99.978%                 | 
 | Tangled Feet  0.022%                   | 
 | Ice Body  0.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Scarf 92.190%                   | 
 | Heavy-Duty Boots  6.307%               | 
 | Other  1.503%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Timid:0/0/0/252/4/252 92.190%          | 
 | Timid:0/0/0/244/12/252  5.667%         | 
 | Other  2.143%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Psychic 98.497%                        | 
 | Ice Beam 97.857%                       | 
 | Trick 93.670%                          | 
 | Focus Blast 92.190%                    | 
 | Other 17.786%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tyranitar 93.670%                      | 
 | Toxapex 92.190%                        | 
 | Landorus-Therian 92.190%               | 
 | Magnezone 92.190%                      | 
 | Tapu Lele 92.190%                      | 
 | Urshifu-Rapid-Strike  5.077%           | 
 | Cloyster  4.417%                       | 
 | Espeon  4.108%                         | 
 | Espeon  4.108%                         | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Bronzong                               | 
 +----------------------------------------+ 
 | Raw count: 323                         | 
 | Avg. weight: 0.00187672604438          | 
 | Viability Ceiling: 67                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 90.556%                       | 
 | Heatproof  9.381%                      | 
 | Heavy Metal  0.063%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 90.474%                      | 
 | Lagging Tail  9.380%                   | 
 | Other  0.146%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Brave:252/252/0/0/4/0 90.445%          | 
 | Sassy:252/0/208/0/48/0  9.380%         | 
 | Other  0.175%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Gyro Ball 90.461%                      | 
 | Earthquake 90.449%                     | 
 | Light Screen 90.435%                   | 
 | Reflect 90.371%                        | 
 | Trick Room  9.491%                     | 
 | Stealth Rock  9.452%                   | 
 | Other 19.340%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Kommo-o 78.094%                        | 
 | Volcarona 78.093%                      | 
 | Tapu Bulu 78.093%                      | 
 | Nihilego 78.093%                       | 
 | Incineroar 78.093%                     | 
 | Marowak-Alola  9.464%                  | 
 | Reuniclus  9.450%                      | 
 | Porygon2  9.405%                       | 
 | Conkeldurr  9.389%                     | 
 | Cresselia  9.380%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Mienshao                               | 
 +----------------------------------------+ 
 | Raw count: 332                         | 
 | Avg. weight: 0.0016248718508           | 
 | Viability Ceiling: 75                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Regenerator 100.000%                   | 
 | Reckless  0.000%                       | 
 | Inner Focus  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 38.819%                   | 
 | Life Orb 35.500%                       | 
 | Protective Pads 21.995%                | 
 | Other  3.685%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 59.574%          | 
 | Jolly:156/0/0/0/100/252 37.018%        | 
 | Other  3.408%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | U-turn 99.999%                         | 
 | Close Combat 96.917%                   | 
 | Knock Off 61.457%                      | 
 | Fake Out 45.189%                       | 
 | Stone Edge 42.161%                     | 
 | Taunt 21.995%                          | 
 | Blaze Kick 15.708%                     | 
 | Other 16.573%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Clefable 65.074%                       | 
 | Dragapult 52.885%                      | 
 | Landorus-Therian 51.990%               | 
 | Ferrothorn 37.611%                     | 
 | Rotom-Wash 37.605%                     | 
 | Slowbro 26.315%                        | 
 | Zapdos 25.886%                         | 
 | Jirachi 21.995%                        | 
 | Garchomp 17.789%                       | 
 | Hatterene 15.782%                      | 
 | Volcarona 15.485%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Vikavolt                               | 
 +----------------------------------------+ 
 | Raw count: 134                         | 
 | Avg. weight: 0.00369253432365          | 
 | Viability Ceiling: 67                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Levitate 100.000%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 96.630%                   | 
 | Other  3.370%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:56/0/0/252/0/200 96.586%        | 
 | Other  3.414%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Bug Buzz 99.907%                       | 
 | Volt Switch 99.905%                    | 
 | Thunderbolt 98.474%                    | 
 | Energy Ball 98.404%                    | 
 | Other  3.311%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Urshifu-Rapid-Strike 97.428%           | 
 | Ferrothorn 96.679%                     | 
 | Weezing-Galar 96.586%                  | 
 | Landorus-Therian 96.586%               | 
 | Tyranitar 96.586%                      | 
 | Tyranitar 96.586%                      | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Sceptile                               | 
 +----------------------------------------+ 
 | Raw count: 283                         | 
 | Avg. weight: 0.00167053711558          | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Unburden 70.156%                       | 
 | Overgrow 29.844%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Electric Seed 59.205%                  | 
 | Choice Specs 29.808%                   | 
 | Focus Sash  8.909%                     | 
 | Other  2.079%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 47.807%        | 
 | Timid:0/0/0/252/4/252 29.808%          | 
 | Adamant:0/252/4/0/0/252 11.424%        | 
 | Modest:0/0/0/252/4/252  5.122%         | 
 | Naughty:0/252/0/4/0/252  3.330%        | 
 | Other  2.508%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Leaf Blade 65.036%                     | 
 | Acrobatics 64.906%                     | 
 | Swords Dance 61.705%                   | 
 | Drain Punch 48.381%                    | 
 | Focus Blast 34.952%                    | 
 | Leaf Storm 34.932%                     | 
 | Dragon Pulse 34.930%                   | 
 | Energy Ball 29.808%                    | 
 | Dragon Claw 11.333%                    | 
 | Other 14.017%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Landorus-Therian 87.172%               | 
 | Tapu Koko 59.259%                      | 
 | Slowbro 49.680%                        | 
 | Bisharp 48.871%                        | 
 | Raichu-Alola 47.780%                   | 
 | Dragapult 28.014%                      | 
 | Magnezone 28.003%                      | 
 | Rotom-Wash 28.003%                     | 
 | Clefable 28.003%                       | 
 | Melmetal 11.340%                       | 
 | Volcarona 11.333%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Pikachu                                | 
 +----------------------------------------+ 
 | Raw count: 293                         | 
 | Avg. weight: 0.00149085792645          | 
 | Viability Ceiling: 75                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Lightning Rod 73.723%                  | 
 | Static 26.277%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Light Ball 98.731%                     | 
 | Other  1.269%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/4/252 65.674%         | 
 | Naive:0/100/0/156/0/252 20.686%        | 
 | Adamant:0/252/0/0/4/252  6.637%        | 
 | Jolly:0/252/4/0/0/252  3.865%          | 
 | Other  3.139%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Thunderbolt 87.953%                    | 
 | Nasty Plot 65.941%                     | 
 | Surf 65.689%                           | 
 | Agility 65.674%                        | 
 | Volt Tackle 31.276%                    | 
 | Extreme Speed 27.340%                  | 
 | Fake Out 20.817%                       | 
 | Substitute  6.691%                     | 
 | Focus Punch  6.637%                    | 
 | Iron Tail  5.279%                      | 
 | Other 16.705%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Weavile 65.926%                        | 
 | Garchomp 65.674%                       | 
 | Durant 65.674%                         | 
 | Blacephalon 65.674%                    | 
 | Tapu Koko 65.674%                      | 
 | Slowking-Galar 27.322%                 | 
 | Mimikyu 21.918%                        | 
 | Keldeo 20.686%                         | 
 | Salamence 20.686%                      | 
 | Tsareena 20.686%                       | 
 | Corviknight  6.638%                    | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Ninjask                                | 
 +----------------------------------------+ 
 | Raw count: 86                          | 
 | Avg. weight: 0.00465954692163          | 
 | Viability Ceiling: 68                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Speed Boost 100.000%                   | 
 | Infiltrator  0.000%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Focus Sash 99.984%                     | 
 | Other  0.016%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:0/252/0/0/4/252 99.988%        | 
 | Other  0.012%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Swords Dance 100.000%                  | 
 | Leech Life 99.996%                     | 
 | Acrobatics 98.879%                     | 
 | Night Slash 98.710%                    | 
 | Other  2.415%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Kommo-o 98.705%                        | 
 | Meowstic 98.705%                       | 
 | Decidueye 98.705%                      | 
 | Polteageist 98.705%                    | 
 | Tentacruel 98.705%                     | 
 | Tentacruel 98.705%                     | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Decidueye                              | 
 +----------------------------------------+ 
 | Raw count: 150                         | 
 | Avg. weight: 0.00264849267987          | 
 | Viability Ceiling: 68                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Overgrow 100.000%                      | 
 | Long Reach  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 99.575%                      | 
 | Other  0.425%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Brave:252/252/0/4/0/0 99.562%          | 
 | Other  0.438%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Substitute 99.602%                     | 
 | Leaf Storm 99.562%                     | 
 | Brave Bird 99.562%                     | 
 | Poltergeist 99.562%                    | 
 | Other  1.712%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Polteageist 99.956%                    | 
 | Kommo-o 99.562%                        | 
 | Meowstic 99.562%                       | 
 | Tentacruel 99.562%                     | 
 | Ninjask 99.562%                        | 
 | Ninjask 99.562%                        | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Meowstic                               | 
 +----------------------------------------+ 
 | Raw count: 281                         | 
 | Avg. weight: 0.00141050421639          | 
 | Viability Ceiling: 70                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Prankster 100.000%                     | 
 | Competitive  0.000%                    | 
 | Keen Eye  0.000%                       | 
 +----------------------------------------+ 
 | Items                                  | 
 | Light Clay 99.997%                     | 
 | Other  0.003%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:0/0/252/0/252/0 99.794%           | 
 | Other  0.206%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Light Screen 100.000%                  | 
 | Reflect 100.000%                       | 
 | Yawn 99.796%                           | 
 | Magic Coat 99.796%                     | 
 | Other  0.407%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Polteageist 99.796%                    | 
 | Kommo-o 99.794%                        | 
 | Decidueye 99.794%                      | 
 | Tentacruel 99.794%                     | 
 | Ninjask 99.794%                        | 
 | Ninjask 99.794%                        | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Araquanid                              | 
 +----------------------------------------+ 
 | Raw count: 135                         | 
 | Avg. weight: 0.00299170317462          | 
 | Viability Ceiling: 69                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Water Bubble 89.948%                   | 
 | Water Absorb 10.052%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 89.520%                      | 
 | Focus Sash  6.782%                     | 
 | Other  3.698%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Careful:252/4/0/0/252/0 79.126%        | 
 | Impish:0/252/0/0/252/0  8.956%         | 
 | Adamant:0/252/0/0/0/252  6.765%        | 
 | Careful:248/100/0/0/160/0  1.690%      | 
 | Other  3.463%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Sticky Web 99.412%                     | 
 | Liquidation 98.904%                    | 
 | Toxic 80.226%                          | 
 | Rest 79.126%                           | 
 | Leech Life 17.904%                     | 
 | Poison Jab  8.999%                     | 
 | Other 15.429%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Slowbro 85.891%                        | 
 | Blissey 79.126%                        | 
 | Ferrothorn 75.245%                     | 
 | Torkoal 72.458%                        | 
 | Dragonite 43.231%                      | 
 | Clefable 15.392%                       | 
 | Haxorus 13.835%                        | 
 | Heracross  9.135%                      | 
 | Garchomp  8.992%                       | 
 | Kabutops  8.956%                       | 
 | Weavile  8.956%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Sableye                                | 
 +----------------------------------------+ 
 | Raw count: 225                         | 
 | Avg. weight: 0.00191962761771          | 
 | Viability Ceiling: 70                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Prankster 99.998%                      | 
 | Keen Eye  0.002%                       | 
 | Stall  0.000%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 98.397%                      | 
 | Other  1.603%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Bold:252/0/144/0/112/0 98.209%         | 
 | Other  1.791%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Will-O-Wisp 99.857%                    | 
 | Recover 99.593%                        | 
 | Mud-Slap 98.209%                       | 
 | Calm Mind 98.209%                      | 
 | Other  4.132%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Togekiss 82.338%                       | 
 | Snorlax 82.338%                        | 
 | Blaziken 82.197%                       | 
 | Reuniclus 82.197%                      | 
 | Jirachi 82.197%                        | 
 | Clefable  1.068%                       | 
 | Shuckle  0.825%                        | 
 | Corsola-Galar  0.825%                  | 
 | Tentacruel  0.825%                     | 
 | Kartana  0.825%                        | 
 | Hydreigon  0.533%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Toxicroak                              | 
 +----------------------------------------+ 
 | Raw count: 575                         | 
 | Avg. weight: 0.000592496077205         | 
 | Viability Ceiling: 70                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Dry Skin 87.800%                       | 
 | Anticipation 12.094%                   | 
 | Poison Touch  0.106%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 99.769%                       | 
 | Other  0.231%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:4/252/0/0/0/252 77.093%        | 
 | Adamant:0/252/0/0/0/252 12.207%        | 
 | Adamant:0/252/0/0/4/252  7.695%        | 
 | Other  3.004%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Drain Punch 87.906%                    | 
 | Sucker Punch 87.562%                   | 
 | Earthquake 77.277%                     | 
 | Bulk Up 77.210%                        | 
 | Swords Dance 21.455%                   | 
 | Poison Jab 13.456%                     | 
 | Cross Chop 12.090%                     | 
 | Fake Out 12.090%                       | 
 | Other 10.954%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Pelipper 84.995%                       | 
 | Kingdra 78.350%                        | 
 | Barraskewda 78.232%                    | 
 | Seismitoad 77.093%                     | 
 | Scizor 77.093%                         | 
 | Ferrothorn 21.042%                     | 
 | Garchomp 12.090%                       | 
 | Chandelure 12.090%                     | 
 | Tyranitar 12.090%                      | 
 | Charizard 12.090%                      | 
 | Krookodile  7.695%                     | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Malamar                                | 
 +----------------------------------------+ 
 | Raw count: 389                         | 
 | Avg. weight: 0.000840401983706         | 
 | Viability Ceiling: 66                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Contrary 100.000%                      | 
 | Suction Cups  0.000%                   | 
 +----------------------------------------+ 
 | Items                                  | 
 | Assault Vest 90.086%                   | 
 | Leftovers  8.006%                      | 
 | Other  1.908%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:0/192/76/0/40/200 65.485%       | 
 | Careful:0/192/104/0/12/200 13.626%     | 
 | Careful:0/192/0/0/116/200 10.936%      | 
 | Adamant:252/252/0/0/4/0  7.862%        | 
 | Other  2.090%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Superpower 99.978%                     | 
 | Rock Slide 97.948%                     | 
 | Knock Off 91.371%                      | 
 | Pluck 65.485%                          | 
 | Liquidation 25.671%                    | 
 | Other 19.547%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 93.816%                      | 
 | Krookodile 86.193%                     | 
 | Shuckle 85.986%                        | 
 | Blacephalon 85.915%                    | 
 | Tapu Lele 85.884%                      | 
 | Octillery  7.862%                      | 
 | Morpeko  7.862%                        | 
 | Eiscue  7.862%                         | 
 | Cramorant  7.862%                      | 
 | Kommo-o  1.105%                        | 
 | Tapu Koko  1.105%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Steelix                                | 
 +----------------------------------------+ 
 | Raw count: 118                         | 
 | Avg. weight: 0.00255510295233          | 
 | Viability Ceiling: 81                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Sturdy 99.946%                         | 
 | Sheer Force  0.051%                    | 
 | Rock Head  0.003%                      | 
 +----------------------------------------+ 
 | Items                                  | 
 | Leftovers 80.899%                      | 
 | Rocky Helmet 19.063%                   | 
 | Other  0.038%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Impish:252/0/4/0/252/0 49.851%         | 
 | Impish:252/4/0/0/252/0 31.014%         | 
 | Relaxed:132/124/252/0/0/0 19.063%      | 
 | Other  0.072%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Body Press 99.952%                     | 
 | Earthquake 99.949%                     | 
 | Stealth Rock 99.940%                   | 
 | Heavy Slam 80.877%                     | 
 | Other 19.282%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Incineroar 49.851%                     | 
 | Toxtricity 49.851%                     | 
 | Crobat 49.851%                         | 
 | Gardevoir 49.851%                      | 
 | Gastrodon 49.851%                      | 
 | Raikou 31.014%                         | 
 | Flygon 31.014%                         | 
 | Bewear 31.014%                         | 
 | Umbreon 31.014%                        | 
 | Chandelure 31.014%                     | 
 | Weavile 19.063%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Durant                                 | 
 +----------------------------------------+ 
 | Raw count: 79                          | 
 | Avg. weight: 0.00376658822839          | 
 | Viability Ceiling: 75                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Hustle 96.684%                         | 
 | Truant  3.286%                         | 
 | Swarm  0.031%                          | 
 +----------------------------------------+ 
 | Items                                  | 
 | Salac Berry 96.409%                    | 
 | Other  3.591%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:0/252/0/0/4/252 96.410%          | 
 | Other  3.590%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Iron Head 96.733%                      | 
 | Hone Claws 96.410%                     | 
 | Stomping Tantrum 96.410%               | 
 | Thunder Fang 96.409%                   | 
 | Other 14.038%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Tapu Koko 96.409%                      | 
 | Pikachu 96.409%                        | 
 | Weavile 96.409%                        | 
 | Garchomp 96.409%                       | 
 | Blacephalon 96.409%                    | 
 | Blacephalon 96.409%                    | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Wigglytuff                             | 
 +----------------------------------------+ 
 | Raw count: 14                          | 
 | Avg. weight: 0.0209743465398           | 
 | Viability Ceiling: 76                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Frisk 99.984%                          | 
 | Competitive  0.016%                    | 
 | Cute Charm  0.000%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Life Orb 99.480%                       | 
 | Other  0.520%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/252/252/4/0 99.463%         | 
 | Other  0.537%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Stealth Rock 99.849%                   | 
 | Ice Beam 99.463%                       | 
 | Toxic 99.463%                          | 
 | Fire Blast 99.463%                     | 
 | Other  1.760%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 99.463%                      | 
 | Urshifu-Rapid-Strike 99.463%           | 
 | Ferrothorn 99.463%                     | 
 | Slowking-Galar 99.463%                 | 
 | Zapdos 99.463%                         | 
 | Zapdos 99.463%                         | | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Linoone                                | 
 +----------------------------------------+ 
 | Raw count: 182                         | 
 | Avg. weight: 0.00153223199221          | 
 | Viability Ceiling: 79                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Gluttony 99.983%                       | 
 | Quick Feet  0.017%                     | 
 | Pickup  0.000%                         | 
 +----------------------------------------+ 
 | Items                                  | 
 | Figy Berry 74.322%                     | 
 | Iapapa Berry 23.628%                   | 
 | Other  2.050%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Adamant:248/252/8/0/0/0 74.322%        | 
 | Adamant:252/252/0/0/0/4 23.628%        | 
 | Other  2.050%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Extreme Speed 99.999%                  | 
 | Belly Drum 99.983%                     | 
 | Stomping Tantrum 99.978%               | 
 | Seed Bomb 74.323%                      | 
 | Shadow Claw 23.633%                    | 
 | Other  2.084%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Mew 76.349%                            | 
 | Blaziken 74.323%                       | 
 | Volcarona 74.322%                      | 
 | Azumarill 74.322%                      | 
 | Blissey 50.485%                        | 
 | Dragonite 25.864%                      | 
 | Salamence 22.939%                      | 
 | Magmortar 22.939%                      | 
 | Ferrothorn 22.939%                     | 
 | Polteageist 22.939%                    | 
 | Heracross 22.939%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Charizard                              | 
 +----------------------------------------+ 
 | Raw count: 761                         | 
 | Avg. weight: 0.000615899125513         | 
 | Viability Ceiling: 72                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Blaze 91.246%                          | 
 | Solar Power  8.754%                    | 
 +----------------------------------------+ 
 | Items                                  | 
 | Sitrus Berry 41.963%                   | 
 | Heavy-Duty Boots 33.748%               | 
 | Leftovers 10.310%                      | 
 | Focus Sash  8.036%                     | 
 | Choice Scarf  2.422%                   | 
 | Other  3.521%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Jolly:4/252/0/0/0/252 41.993%          | 
 | Timid:0/0/0/252/4/252 32.456%          | 
 | Modest:0/0/0/252/4/252  9.914%         | 
 | Timid:224/0/0/112/0/172  8.788%        | 
 | Timid:0/0/4/252/0/252  3.602%          | 
 | Other  3.247%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Roost 50.246%                          | 
 | Flamethrower 45.013%                   | 
 | Acrobatics 43.122%                     | 
 | Earthquake 42.684%                     | 
 | Belly Drum 42.097%                     | 
 | Flame Charge 42.016%                   | 
 | Defog 37.988%                          | 
 | Scorching Sands 32.382%                | 
 | Air Slash 20.635%                      | 
 | Fire Blast 11.346%                     | 
 | Sunny Day  7.717%                      | 
 | Solar Beam  6.191%                     | 
 | Other 18.561%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Dragapult 30.249%                      | 
 | Rillaboom 30.152%                      | 
 | Aegislash 29.776%                      | 
 | Haxorus 29.668%                        | 
 | Rhyperior 29.660%                      | 
 | Garchomp 17.059%                       | 
 | Tyranitar  9.530%                      | 
 | Ferrothorn  9.045%                     | 
 | Chandelure  8.816%                     | 
 | Toxicroak  8.788%                      | 
 | Weavile  7.717%                        | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
 +----------------------------------------+ 
 | Chandelure                             | 
 +----------------------------------------+ 
 | Raw count: 488                         | 
 | Avg. weight: 0.000555102934389         | 
 | Viability Ceiling: 66                  | 
 +----------------------------------------+ 
 | Abilities                              | 
 | Flash Fire 89.186%                     | 
 | Infiltrator  6.506%                    | 
 | Flame Body  4.308%                     | 
 +----------------------------------------+ 
 | Items                                  | 
 | Choice Specs 84.877%                   | 
 | Choice Scarf  9.232%                   | 
 | Oran Berry  3.325%                     | 
 | Other  2.567%                          | 
 +----------------------------------------+ 
 | Spreads                                | 
 | Modest:0/0/0/252/0/252 47.630%         | 
 | Timid:0/0/0/252/4/252 46.512%          | 
 | Bold:208/20/192/0/0/88  3.325%         | 
 | Other  2.533%                          | 
 +----------------------------------------+ 
 | Moves                                  | 
 | Energy Ball 99.151%                    | 
 | Shadow Ball 98.794%                    | 
 | Flamethrower 57.328%                   | 
 | Trick 42.372%                          | 
 | Fire Blast 39.093%                     | 
 | Psychic 32.516%                        | 
 | Will-O-Wisp 15.552%                    | 
 | Other 15.194%                          | 
 +----------------------------------------+ 
 | Teammates                              | 
 | Ferrothorn 47.650%                     | 
 | Flygon 34.898%                         | 
 | Raikou 34.529%                         | 
 | Umbreon 34.520%                        | 
 | Steelix 34.519%                        | 
 | Bewear 34.519%                         | 
 | Scizor 34.203%                         | 
 | Gyarados 32.898%                       | 
 | Jellicent 32.478%                      | 
 | Excadrill 32.426%                      | 
 | Tyranitar 18.529%                      | 
 +----------------------------------------+ 
 | Checks and Counters                    | 
 +----------------------------------------+ 
"""
_json = (convert_to_json(input_text))
# Assuming `input_text` is a dictionary or a list
open('data.json', 'w').write(_json)
