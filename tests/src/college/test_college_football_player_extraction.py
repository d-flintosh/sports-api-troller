import csv
import json
from dataclasses import dataclass

import pytest

from src.college.college_football_player_extraction import do_things
from src.models.Player import EnhancedJSONEncoder


@pytest.mark.skip(reason="only run this manually")
def test_do_things():
    do_things()


@dataclass
class GoogleDocFormat:
    sr_player_path: str
    sr_team_name: str
    drafted_by: str
    name: str
    position: str
    school_2022: str
    school_2021: str
    total_2021: str
    avg_2021: str
    unknown: str
    active: str


SR_PLAYER_PATH = 0
SR_TEAM_NAME = 1
DRAFTED_BY = 2
NAME = 3
POSITION = 4
SCHOOL_2021 = 5
TOTAL_2021 = 6
AVG_2021 = 7
UNKNOWN = 8
ACTIVE_CHECK = 9


@dataclass
class GoogleDocPlayerNames:
    name: str
    index: int


@pytest.mark.skip(reason="only run this manually")
def test_get_positions():
    the_players = json.loads(players)
    reader = csv.reader(google_doc_csv.splitlines())
    google_doc_players = list(reader)
    google_doc_players_names = []
    ourlads_players_names = []
    missing_players = []
    found_multiple = []
    found_players = []

    for idx, player in enumerate(google_doc_players):
        google_doc_players_names.append(GoogleDocPlayerNames(name=simplify_name(name=player[NAME]), index=idx))

    for google_player in google_doc_players_names:
        found_player = False
        times_found = 0
        for player in the_players.get('players'):
            if simplify_name(name=f'{player.get("first_name")}{player.get("last_name")}') == google_player.name:
                found_player = True
                times_found += 1
                found_players.append(GoogleDocFormat(
                    sr_player_path=google_doc_players[google_player.index][SR_PLAYER_PATH],
                    sr_team_name=google_doc_players[google_player.index][SR_TEAM_NAME],
                    drafted_by=google_doc_players[google_player.index][DRAFTED_BY],
                    name=google_doc_players[google_player.index][NAME],
                    position=google_doc_players[google_player.index][POSITION],
                    school_2022=player.get('team_city'),
                    school_2021=google_doc_players[google_player.index][SCHOOL_2021],
                    total_2021=google_doc_players[google_player.index][TOTAL_2021],
                    avg_2021=google_doc_players[google_player.index][AVG_2021],
                    unknown='',
                    active=google_doc_players[google_player.index][ACTIVE_CHECK],
                ))

        if times_found > 1:
            found_multiple.append(google_player)

        if not found_player:
            missing_players.append(google_player)

    for player in the_players.get('players'):
        is_found_player = False
        for found_player in found_players:
            if simplify_name(name=f'{player.get("first_name")}{player.get("last_name")}') == simplify_name(name=found_player.name):
                is_found_player = True

        if not is_found_player:
            found_players.append(GoogleDocFormat(
                sr_player_path='',
                sr_team_name='',
                drafted_by='',
                name=f'{player.get("first_name")} {player.get("last_name")}',
                position=player.get('position'),
                school_2022=player.get('team_city'),
                school_2021='',
                total_2021='',
                avg_2021='',
                unknown='',
                active='',
            ))
    # print(json.dumps(found_multiple, cls=EnhancedJSONEncoder))
    print(json.dumps(missing_players, cls=EnhancedJSONEncoder))
    # print(json.dumps(found_players, cls=EnhancedJSONEncoder))
    f = open('/Users/drew/workspace/sports-api-troller/2022_players.csv', "w")
    for player in found_players:
        f.write(f'{player.sr_player_path},{player.sr_team_name},{player.drafted_by},{player.name},{player.position},{player.school_2022},{player.school_2021},{player.total_2021},{player.avg_2021},{player.unknown},{player.active}\n')

    f.close()


def simplify_name(name: str):
    return ''.join(filter(str.isalnum, name.lower()))


google_doc_csv = '''brennan-armstrong-1,Virginia,Pras,Brennan Armstrong,QB,Virginia,445.86,40.53,,Yes
,,,Dillon Gabriel,QB,Central Florida,120.06,40.02,,Yes
,,,Mohamed Ibrahim,RB,Minnesota,38.3,38.3,,Yes
malik-cunningham-1,Louisville,Zax,Malik Cunningham,QB,Louisville,476.64,36.66,,Yes
cj-stroud-1,Ohio State,Greg,C.J. Stroud,QB,Ohio State,439.4,36.62,,Yes
,,Drew,Sam Hartman,QB,Wake Forest,506.82,36.2,,Yes
,,,Lew Nichols III,RB,Central Michigan,453.24,34.86,,Yes
,,,Tanner Mordecai,QB,Southern Methodist,411.32,34.28,,Yes
bryce-young-1,Alabama,Bill,Bryce Young,QB,Alabama,494.88,32.99,,Yes
,,,Deuce Vaughn,RB,Kansas State,423.2,32.55,,Yes
,,,Dorian Thompson-Robinson,QB,UCLA,342.26,31.11,,Yes
,,,Adrian Martinez,QB,Nebraska,339.02,30.82,,Yes
hendon-hooker-1,Tennessee,Ryan N,Hendon Hooker,QB,Tennessee,400.4,30.8,,Yes
,,,Jordan Addison,WR,Pittsburgh,427.9,30.56,,Yes
,,,Will Rogers,QB,Mississippi State,396.46,30.5,,Yes
,,,Grayson McCall,QB,Coastal Carolina,329.92,29.99,,Yes
,,,Sean Tucker,RB,Syracuse,354.1,29.51,,Yes
,,,Devin Leary,QB,North Carolina State,352.02,29.33,,Yes
,,,Bijan Robinson,RB,Texas,293.2,29.32,,Yes
,,,Jake Haener,QB,Fresno State,380.54,29.27,,Yes
,,,Deven Thompkins,WR,Utah State,405.1,28.94,,Yes
,,,Brett Gabbert,QB,Miami (OH),282.62,28.26,,Yes
,,,Frank Harris,QB,Texas-San Antonio,394.28,28.16,,Yes
,,,Tyler Van Dyke,QB,Miami (FL),278.94,27.89,,Yes
,,,Chris Reynolds,QB,Charlotte,303.6,27.6,,Yes
,,,Jaren Hall,QB,Brigham Young,275.32,27.53,,Yes
,,,Will Levis,QB,Kentucky,356.14,27.4,,Yes
jaxon-smith-njigba-1,Ohio State,Ryan N,Jaxon Smith-Njigba,WR,Ohio State,354.6,27.28,,Yes
,,,Spencer Sanders,QB,Oklahoma State,342.96,26.38,,Yes
,,,Logan Bonner,QB,Utah State,367.72,26.27,,Yes
,,,KJ Jefferson,QB,Arkansas,340.44,26.19,,Yes
,,,Jordan Travis,QB,Florida State,261.56,26.16,,Yes
,,,Emory Jones,QB,Florida,339.06,26.08,,Yes
,,,Aidan O'Connell,QB,Purdue,310.48,25.87,,Yes
,,,Payton Thorne,QB,Michigan State,335.88,25.84,,Yes
,,,Kayshon Boutte,WR,Louisiana State,152.9,25.48,,Yes
,,,Taulia Tagovailoa,QB,Maryland,330.5,25.42,,Yes
,,,Holton Ahlers,QB,East Carolina,300.14,25.01,,Yes
,,,Jacob Cowing,WR,UTEP,324.9,24.99,,Yes
,,,Clayton Tune,QB,Houston,349.16,24.94,,Yes
,,,Garrett Shrader,QB,Syracuse,298.9,24.91,,Yes
,,,Zach Evans,RB,Texas Christian,148.8,24.8,,Yes
,,,TreVeyon Henderson,RB,Ohio State,322,24.77,,Yes
,,,Travis Dye,RB,Oregon,346.3,24.74,,Yes
,,,Nathaniel Dell,WR,Houston,345.4,24.67,,Yes
,,,Jeff Sims,QB,Georgia Tech,196.92,24.62,,Yes
,,,Josh Downs,WR,North Carolina,317.5,24.42,,Yes
,,,Michael Pratt,QB,Tulane,266.64,24.24,,Yes
,,,Chevan Cordeiro,QB,Hawaii,265.92,24.17,,Yes
,,,Gerry Bohanon,QB,Baylor,287.8,23.98,,Yes
,,,Cameron Rising,QB,Utah,305.62,23.51,,Yes
,,,Chase Brice,QB,Appalachian State,328.38,23.46,,Yes
,,,Phil Jurkovec,QB,Boston College,140.76,23.46,,Yes
,,,Max Duggan,QB,Texas Christian,231.12,23.11,,Yes
,,,Rocky Lombardi,QB,Northern Illinois,300.18,23.09,,Yes
,,,Max Johnson,QB,Louisiana State,276.5,23.04,,Yes
,,,Zach Charbonnet,RB,UCLA,275.4,22.95,,Yes
,,,Jayden de Laura,QB,Washington State,274.62,22.88,,Yes
,,,N'Kosi Perry,QB,Florida Atlantic,273.24,22.77,,Yes
,,,Jaylan Knighton,RB,Miami (FL),180.1,22.51,,Yes
,,,Casey Thompson,QB,Texas,268.22,22.35,,Yes
,,,Dontay Demus Jr.,WR,Maryland,111.7,22.34,,Yes
,,,Todd Centeio,QB,Colorado State,266.42,22.2,,Yes
,,,Grant Wells,QB,Marshall,285,21.92,,Yes
,,,Chris Rodriguez Jr.,RB,Kentucky,284.9,21.92,,Yes
,,,Brady McBride,QB,Texas State,152.38,21.77,,Yes
,,,Zakhari Franklin,WR,Texas-San Antonio,280.7,21.59,,Yes
,,,Sean Clifford,QB,Penn State,278.58,21.43,,Yes
,,,Jalen Cropper,WR,Frenso State,278.54,21.43,,Yes
,,,Tyler Shough,QB,Texas Tech,84.28,21.07,,Yes
,,,Tanner McKee,QB,Stanford,207.48,20.75,,Yes
,,,Harrison Waylee,RB,Northern Illinois,103,20.6,,Yes
,,,Chance Nolan,QB,Oregon State,267.68,20.59,,Yes
,,,Keaton Mitchell,RB,East Carolina,245.5,20.46,,Yes
,,,Haaziq Daniels,QB,Air Force,243.76,20.31,,Yes
,,,Hank Bachmeier,QB,Boise State,241.16,20.1,,Yes
,,,DeWayne McBride,RB,Alabama-Birmingham,260,20,,Yes
,,,Braxton Burmeister,QB,Virginia Tech,238.8,19.9,,Yes
,,,Bo Nix,QB,Auburn,198.56,19.86,,Yes
,,,Brad Roberts,RB,Air Force,253.6,19.51,,Yes
,,,Davis Brin,QB,Tulsa,253.56,19.5,,Yes
,,,Kurtis Rourke,QB,Ohio,193.54,19.35,,Yes
,,,Jayden Reed,WR,Michigan State,251,19.31,,Yes
,,,Layne Hatcher,QB,Arkansas State,211.52,19.23,,Yes
,,,Quentin Johnston,WR,Texas Christian,153.6,19.2,,Yes
,,,Blake Corum,RB,Michigan,230.3,19.19,,Yes
,,,Hassan Beydoun,WR,Eastern Michigan,248.02,19.08,,Yes
,,,Daniel Richardson,QB,Central Michigan,245.52,18.89,,Yes
,,,Chase Brown,RB,Illinois,188.7,18.87,,Yes
,,,Will Shipley,RB,Clemson,188.58,18.86,,Yes
,,,Devon Achane,RB,Texas A&M,226.1,18.84,,Yes
,,,Xavier Hutchinson,WR,Iowa State,241.46,18.57,,Yes
,,,Tank Bigsby,RB,Auburn,239.3,18.41,,Yes
,,,Corey Rucker,WR,Arkansas State,218.6,18.22,,Yes
,,,Dylan Morris,QB,Washington,197.82,17.98,,Yes
,,,Gavin Hardison,QB,Texas-El Paso,232.32,17.87,,Yes
,,,Connor Bazelak,QB,Missouri,195.62,17.78,,Yes
,,,Jo'quavious Marks,RB,Mississippi State,228.8,17.6,,Yes
,,,Marquez Cooper,RB,Kent State,246,17.57,,Yes
,,,Travell Harris,WR,Washington State,227.6,17.51,,TBD
,,,Kalil Pimpleton,WR,Central Michigan,227.56,17.5,,TBD
,,,Jarret Doege,QB,West Virginia,225.72,17.36,,TBD
,,,Samori Toure,WR,Nebraska,208.1,17.34,,TBD
,,,Tyler Snead,WR,East Carolina,207.48,17.29,,TBD
,,,Tyquan Thornton,WR,Baylor,241.94,17.28,,TBD
,,,Jahmyr Gibbs,RB,Georgia Tech,207.1,17.26,,TBD
,,,Michael Mayer,TE,Notre Dame,207,17.25,,TBD
,,,Gunnar Holmberg,QB,Duke,189.02,17.18,,TBD
,,,Xavier Hutchinson,WR,Texas Tech,188.3,17.12,,TBD
,,,Nick Starkel,QB,San Jose State,118.7,16.96,,TBD
,,,Max Borghi,RB,Washington State,201.6,16.8,,TBD
,,,Spencer Rattler,QB,Oklahoma,151.02,16.78,,TBD
,,,Jashaun Corbin,RB,Florida State,201.1,16.76,,TBD
,,,Milton Wright,WR,Purdue,183.3,16.66,,TBD
,,,Matt McDonald,QB,Bowling Green State,199.5,16.62,,TBD
,,,Tyjae Spears,RB,Tulane,198.8,16.57,,TBD
,,,D.J. Mack Jr.,QB,Old Dominion,115.76,16.54,,TBD
,,,Kedon Slovis,QB,Southern California,148.52,16.5,,TBD
,,,Xazavian Valladay,RB,Wyoming,213.6,16.43,,TBD
,,,Camerun Peoples,RB,Appalachian State,195.5,16.29,,TBD
,,,Kevin Austin Jr.,WR,Notre Dame,194.6,16.22,,TBD
,,,Zach Calzada,QB,Texas A&M,194.5,16.21,,TBD
,,,Billy Kemp IV,WR,Virginia,193.4,16.12,,TBD
,,,Terry Wilson,QB,New Mexico,96.52,16.09,,TBD
,,,Jerrion Ealy,RB,Mississippi,192.6,16.05,,TBD
,,,Gary Bryant Jr.,WR,Southern California,160.2,16.02,,TBD
,,,Frank Gore Jr.,RB,Southern Mississippi,192.16,16.01,,TBD
,,,Emeka Emezie,WR,North Carolina State,191.2,15.93,,TBD
,,,Doug Brumfield,QB,Nevada-Las Vegas,47.7,15.9,,TBD
,,,Tyler Lytle,QB,Massachusetts,31.46,15.73,,TBD
,,,Stephen Carr,RB,Indiana,141.3,15.7,,TBD
,,,Cam'Ron Harris,RB,Miami (FL),109.8,15.69,,TBD
,,,Brandon Bowling,WR,Utah State,219.5,15.68,,TBD
,,,Smoke Harris,WR,Louisiana Tech,188,15.67,,TBD
,,,Tayon Fleet-Davis,RB,Maryland,203.6,15.66,,TBD
,,,Logan Wright,RB,Georgia Southern,187.3,15.61,,TBD
,,,Velus Jones Jr.,WR,Tennessee,201.2,15.48,,TBD
,,,Jabari Small,RB,Tennessee,170.3,15.48,,TBD
,,,Rashee Rice,WR,Southern Methodist,185,15.42,,TBD
,,,Charlie Kolar,TE,Iowa State,183.6,15.3,,TBD
,,,Jason Brownlee,WR,Southern Mississippi,168.3,15.3,,TBD
,,Drew,D.J. Uiagalelei,QB,Clemson,198.64,15.28,,TBD
,,,D'vonte Price,RB,Florida International,137.5,15.28,,TBD
,,,Gunner Romney,WR,Brigham Young,121.6,15.2,,TBD
,,,Kyle Vantrease,QB,Buffalo,151.94,15.19,,TBD
,,,Bo Melton,WR,Rutgers,149.9,14.99,,TBD
,,,Dameon Pierce,RB,Florida,194,14.92,,TBD
,,,Toa Taua,RB,Nevada,193.8,14.91,,TBD
,,,Sean Chambers,QB,Wyoming,118.8,14.85,,TBD
,,,Marcus Williams Jr.,RB,Louisiana Tech,177.9,14.82,,TBD
,,,Tyrion Davis-Price,RB,Louisiana State,177.7,14.81,,TBD
,,,Tre Turner,WR,Virginia Tech,146.9,14.69,,TBD
,,,De'Montre Tuggle,RB,Ohio,176,14.67,,TBD
,,,Dante Wright,WR,Colorado State,131.9,14.66,,TBD
,,,Rakim Jarrett,WR,Maryland,190.1,14.62,,TBD
,,,Shamari Brooks,RB,Tulsa,190,14.62,,TBD
,,,Victor Tucker,WR,Charlotte,146.1,14.61,,TBD
,,,Peter Parrish,QB,Memphis,14.6,14.6,,TBD
,,,Ronnie Bell,WR,Michigan,14.6,14.6,,TBD
,,,Neil Pau'u,WR,Brigham Young,145.24,14.52,,TBD
,,,Joshua Cephus,WR,Texas-San Antonio,202.32,14.45,,TBD
,,,Cade McNamara,QB,Michigan,201.64,14.4,,TBD
,,,Jason Bean,QB,Kansas,143.98,14.4,,TBD
,,,Corey Gammage,WR,Marshall,186.9,14.38,,TBD
,,,Henry Colombi,QB,Texas Tech,100.24,14.32,,TBD
,,,Sean McGrew,RB,Washington,114.5,14.31,,TBD
,,,Jelani Woods,TE,Virginia,156.9,14.26,,TBD
,,,Michael Penix Jr.,QB,Indiana,71.16,14.23,,TBD
,,,Sean Dykes,TE,Memphis,170.7,14.22,,TBD
,,,Luke Doty,QB,South Carolina,70.9,14.18,,TBD
,,,Austin Aune,QB,North Texas,184.14,14.16,,TBD
,,,D'Wan Mathis,QB,Temple,99.12,14.16,,TBD
,,,Tyler Vitt,QB,Texas State,70.74,14.15,,TBD
,,,Greg Bell,RB,San Diego State,197.6,14.11,,TBD
,,,Chris Smith,RB,Louisiana,183.48,14.11,,TBD
,,,Raheem Blackshear,RB,Virginia Tech,182.6,14.05,,TBD
,,,Greg Dulcich,TE,UCLA,154.5,14.05,,TBD
,,,Gunnar Watson,QB,Troy,112.12,14.02,,TBD
,,,Parker Washington,WR,Penn State,181.2,13.94,,TBD
,,,Brittain Brown,RB,UCLA,139.4,13.94,,TBD
,,,Devin Neal,RB,Kansas,152.4,13.85,,TBD
,,,Dae Dae Hunter,RB,Hawaii,138.4,13.84,,TBD
,,,JT Daniels,QB,Georgia,69.08,13.82,,TBD
,,,Thomas Hennigan,WR,Appalachian State,193.3,13.81,,TBD
,,,Zay Flowers,WR,Boston College,165.5,13.79,,TBD
,,,Thayer Thomas,WR,North Carolina State,165.5,13.79,,TBD
,,,Kimani Vidal,RB,Troy,150.5,13.68,,TBD
,,,James Cook,RB,Georgia,204.2,13.61,,TBD
,,,Ricky Person Jr.,RB,North Carolina State,162.6,13.55,,TBD
,,,Snoop Conner,RB,Mississippi,174.9,13.45,,TBD
,,,Emani Bailey,RB,Louisiana,147.5,13.41,,TBD
,,,Ulysses Bentley IV,RB,Southern Methodist,134,13.4,,TBD
,,,Jonathan Mingo,WR,Mississippi,79.6,13.27,,TBD
,,,Tyler Nevens,RB,San Jose State,145.8,13.25,,TBD
,,,Winston Wright Jr.,WR,West Virginia,172,13.23,,TBD
,,,Haynes King,QB,Texas A&M,26.4,13.2,,TBD
,,,Elijah Cooks,WR,Nevada,52.7,13.18,,TBD
,,,Jaylen Hall,WR,Western Michigan,144.2,13.11,,TBD
,,,Desmond Trotter,QB,South Alabama,65.24,13.05,,TBD
,,,Charlie Brewer,QB,Utah,38.96,12.99,,TBD
,,,La'Darius Jefferson,RB,Western Michigan,155.4,12.95,,TBD
,,,Stephon Robinson Jr.,WR,Northwestern,142.5,12.95,,TBD
,,,Reggie Roberson,WR,Southern Methodist,154.5,12.88,,TBD
,,,Spencer Petras,QB,Iowa,154.3,12.86,,TBD
,,,Trea Shropshire,WR,Alabama-Birmingham,154.3,12.86,,TBD
,,,Kobe Pace,RB,Clemson,140.2,12.75,,TBD
,,,Tai Lavatai,QB,Navy,127.06,12.71,,TBD
,,,Brendon Lewis,QB,Colorado,152.4,12.7,,TBD
,,,Taj Harris,WR,Syracuse,38.1,12.7,,TBD
,,,AJ Mayer,QB,Miami (OH),88.74,12.68,,TBD
,,,Kyric McGowan,WR,Georgia Tech,125.7,12.57,,TBD
,,,Jase McClellan,RB,Alabama,62.8,12.56,,TBD
,,,Jordan Whittington,WR,Texas,87.5,12.5,,TBD
,,,Kyle Williams,WR,Nevada-Las Vegas,124.8,12.48,,TBD
,,,Israel Abanikanda,RB,Pittsburgh,161.8,12.45,,TBD
,,,Graham Mertz,QB,Wisconsin,159.82,12.29,,TBD
,,,Tyrice Richie,WR,Northern Illinois,109.6,12.18,,TBD
,,,Tommy DeVito,QB,Syracuse,36.52,12.17,,TBD
,,,Noah Vedral,QB,Rutgers,157.86,12.14,,TBD
,,,Reese White,RB,Coastal Carolina,109.3,12.14,,TBD
,,,Bailey Hockman,QB,Middle Tennessee State,36.32,12.11,,TBD
,,,George Holani,RB,Boise State,108.8,12.09,,TBD
,,,Zonovan Knight,RB,North Carolina State,144.9,12.08,,TBD
,,,Brennan Presley,WR,Oklahoma State,156.74,12.06,,TBD
,,,Avery Davis,WR,Notre Dame,96.5,12.06,,TBD
,,,Chris Autman-Bell,WR,Minnesota,132.6,12.05,,TBD
,,,Chris Pierce Jr.,WR,Vanderbilt,144.4,12.03,,TBD
,,,SaRodorick Thompson,RB,Texas Tech,132.3,12.03,,TBD
,,,Jacob Sirmon,QB,Central Michigan,60.06,12.01,,TBD
,,,Devon Williams,WR,Oregon,119.7,11.97,,TBD
,,,Jaray Jenkins,WR,Louisiana State,130.2,11.84,,TBD
,,,Jaden Walley,WR,Mississippi State,153.8,11.83,,TBD
,,,Ainias Smith,RB,Texas A&M,141.5,11.79,,TBD
,,,Mike Harley,WR,Miami (FL),141.4,11.78,,TBD
,,,Tyrell Robinson,RB,Army,152.9,11.76,,TBD
,,,Tanner Morgan,QB,Minnesota,152.86,11.76,,TBD
,,,Tayvion Robinson,WR,Virginia Tech,140.72,11.73,,TBD
,,,Michael Wiley,RB,Arizona,128.9,11.72,,TBD
,,,Malik Davis,RB,Florida,140.4,11.7,,TBD
,,,Christopher Brown Jr.,RB,California,139.8,11.65,,TBD
,,,Trey Lowe,QB,Southern Mississippi,23.28,11.64,,TBD
,,,Re'Mahn Davis,RB,Vanderbilt,34.8,11.6,,TBD
,,,Trevon Bradford,WR,Oregon State,150.6,11.58,,TBD
,,,Zamir White,RB,Georgia,173.1,11.54,,TBD
,,,Justyn Ross,WR,Clemson,115.4,11.54,,TBD
,,,Marvin Mims,WR,Oklahoma,149,11.46,,TBD
,,,Nykeim Johnson,WR,Kent State,159.3,11.38,,TBD
,,,Jarrin Pierce,WR,Middle Tennessee State,136.3,11.36,,TBD
,,,Jacob Copeland,WR,Florida,146.2,11.25,,TBD
,,,Jaylon Robinson,WR,Central Florida,67.2,11.2,,TBD
,,,Lincoln Pare,RB,Arkansas State,123.1,11.19,,TBD
,,,Bryce Ford-Wheaton,WR,West Virginia,122.5,11.14,,TBD
,,,Shadrick Byrd,RB,Charlotte,133.1,11.09,,TBD
,,,Rahjai Harris,RB,East Carolina,133.1,11.09,,TBD
,,,Jalen Mitchell,RB,Louisville,131.3,10.94,,TBD
,,,Kobe Hudson,WR,Auburn,131,10.92,,TBD
,,,Jack Plummer,QB,Purdue,76.26,10.89,,TBD
,,,Jyaire Shorter,WR,North Texas,21.7,10.85,,TBD
,,,Keric Wheatfall,WR,Fresno State,128.8,10.73,,TBD
,,,Armani Rogers,QB,Ohio,128.4,10.7,,TBD
,,,Yusuf Ali,WR,Middle Tennessee State,117.7,10.7,,TBD
,,,Marcell Barbee,WR,Texas State,127,10.58,,TBD
,,,Micah Bernard,RB,Utah,137.4,10.57,,TBD
,,,T.J. Pledger,RB,Utah,146.1,10.44,,TBD
,,,Calvin Hill,RB,Texas State,125.1,10.42,,TBD
,,,Austin Jones,RB,Stanford,114.5,10.41,,TBD
,,,Jarek Broussard,RB,Colorado,114.2,10.38,,TBD
,,,Cameron Carroll,RB,Tulane,124.4,10.37,,TBD
,,,Joseph Ngata,WR,Clemson,82.8,10.35,,TBD
,,,Justin Tomlin,QB,Georgia Southern,82.58,10.32,,TBD
,,,Yo'Heinz Tyler,WR,Ball State,133.7,10.28,,TBD
,,,Drew Pyne,QB,Notre Dame,20.36,10.18,,TBD
,,,Kaylon Geiger,WR,Texas Tech,122.1,10.17,,TBD
,,,Roschon Johnson,RB,Texas,121.28,10.11,,TBD
,,,Ken Seals,QB,Vanderbilt,80.44,10.06,,TBD
,,,Tahj Washington,WR,Southern California,120.2,10.02,,TBD
,,,Vavae Malepeai,RB,Southern California,109.7,9.97,,TBD
,,,Rhett Rodriguez,QB,Louisiana-Monroe,59.46,9.91,,TBD
,,,Jeff Foreman,WR,Arkansas State,108.6,9.87,,TBD
,,,Brandon Peters,QB,Illinois,88.8,9.87,,TBD
,,,Braylon Sanders,WR,Mississippi,108.5,9.86,,TBD
,,,Christian Beal-Smith,RB,Wake Forest,116.9,9.74,,TBD
,,,Donovan Edwards,RB,Michigan,106.9,9.72,,TBD
,,,Zander Horvath,RB,Purdue,77.8,9.72,,TBD
,,,Jalen Wydermyer,TE,Texas A&M,115.5,9.62,,TBD
,,,Isaih Pacheco,RB,Rutgers,115.2,9.6,,TBD
,,,Jadon Haselwood,WR,Oklahoma,114.9,9.58,,TBD
,,,Cornelius Johnson,WR,Michigan,133.7,9.55,,TBD
,,,Tyhier Tyler,QB,Army,104.76,9.52,,TBD
,,,Miyan Williams,RB,Ohio State,95.2,9.52,,TBD
,,,Dahu Green,WR,Arkansas State,66.6,9.51,,TBD
,,,Mario Williams,WR,Oklahoma,103.6,9.42,,TBD
,,,Ja'Varrius Johnson,WR,Auburn,75.3,9.41,,TBD
,,,Britain Covey,WR,Utah,131.3,9.38,,TBD
,,,Michael Wilson,WR,Stanford,37.5,9.38,,TBD
,,,Jordan Watkins,WR,Louisville,112.1,9.34,,TBD
,,,Rodrigues Clark,RB,Memphis,93.2,9.32,,TBD
,,,C.J. Johnson,WR,East Carolina,93,9.3,,TBD
,,,Terion Stewart,RB,Bowling Green State,82.2,9.13,,TBD
,,,Chip Trayanum,RB,Arizona State,82.1,9.12,,TBD
,,,Duece Watts,WR,Tulane,72.1,9.01,,TBD
,,,Master Teague III,RB,Ohio State,62.7,8.96,,TBD
,,,Arian Smith,WR,Georgia,26.7,8.9,,TBD
,,,Ty Fryfogle,WR,Indiana,106.6,8.88,,TBD
,,,Vincent Davis,RB,Pittsburgh,123.8,8.84,,TBD
,,,Deion Hankins,RB,UTEP,88.2,8.82,,TBD
,,,Jermaine Burton,WR,Georgia,105.7,8.81,,TBD
,,,Reggie Todd,WR,Troy,61.6,8.8,,TBD
,,,Jarrett Guarantano,QB,Washington State,17.56,8.78,,TBD
,,,Hudson Card,QB,Texas,61.3,8.76,,TBD
,,,D.J. Matthews,WR,Indiana,43.3,8.66,,TBD
,,,Chris Tyree,RB,Notre Dame,95,8.64,,TBD
,,,Marvin Harrison Jr.,WR,Ohio State,42.9,8.58,,TBD
,,,Joshua Moore,WR,Texas,68.5,8.56,,TBD
,,,Eric Gray,RB,Oklahoma,111.1,8.55,,TBD
,,,Jake Ferguson,TE,Wisconsin,109,8.38,,TBD
,,,Cam Johnson,WR,Vanderbilt,91.7,8.34,,TBD
,,,Kevin Marks Jr.,RB,Buffalo,81.9,8.19,,TBD
,,,Isaac Ruoss,RB,Navy,97.6,8.13,,TBD
,,,Cornelious Brown IV,QB,Georgia State,32.26,8.06,,TBD
,,,Hunter Dekkers,QB,Iowa State,31.82,7.96,,TBD
,,,McKenzie Milton,QB,Florida State,47.7,7.95,,TBD
,,,Mike Woods,WR,Oklahoma,87.2,7.93,,TBD
,,,Jahcour Pearson,WR,Mississippi,78.2,7.82,,TBD
,,,Isaiah Winstead,WR,Toledo,101,7.77,,TBD
,,,Trelon Smith,RB,Arkansas,100.9,7.76,,TBD
,,,Javon Baker,WR,Alabama,23.1,7.7,,TBD
,,,Isaiah Hamilton,WR,San Jose State,84.4,7.67,,TBD
,,,Darius Boone Jr.,RB,Eastern Michigan,98.8,7.6,,TBD
,,,Carter Bradley,QB,Toledo,60.28,7.54,,TBD
,,,Noah Cain,RB,Penn State,89.4,7.45,,TBD
,,,Harrison Bailey,QB,Tennessee,7.44,7.44,,TBD
,,,Mark-Antony Richards,RB,Central Florida,81.5,7.41,,TBD
,,,Cade Otton,TE,Washington,59,7.38,,TBD
,,,Shaun Shivers,RB,Auburn,59,7.38,,TBD
,,,Brock Sturges,RB,Texas State,58.6,7.32,,TBD
,,,Khafre Brown,WR,North Carolina,14.5,7.25,,TBD
,,,LV Bunkley-Shelton,WR,Arizona State,86.8,7.23,,TBD
,,,Andrew Parchment,WR,Florida State,72.3,7.23,,TBD
,,,Keyvone Lee,RB,Penn State,93,7.15,,TBD
,,,Asa Martin,RB,Memphis,63.8,7.09,,TBD
,,,Chance Lovertich,QB,Mississippi State,14.16,7.08,,TBD
,,,Cameron Ross,WR,Connecticut,14,7,,TBD
,,,Omar Manning,WR,Nebraska,76.1,6.92,,TBD
,,,Johnny Johnson III,WR,Oregon,62.1,6.9,,TBD
,,,Lawrance Toafili,RB,Florida State,55.2,6.9,,TBD
,,,Jadan Blue,WR,Temple,54.8,6.85,,TBD
,,,Keylon Stokes,WR,Tulsa,27.4,6.85,,TBD
,,,Carson Beck,QB,Gerogia,20.54,6.85,,TBD
,,,J.J. Mccarthy,QB,Michigan,75.04,6.82,,TBD
,,,Wayne Taulapapa,RB,Virginia,67.6,6.76,,TBD
,,,Jabari Laws,QB,Army,40.54,6.76,,TBD
,,,Slade Bolden,WR,Alabama,100.8,6.72,,TBD
,,,J.D. King,RB,Georgia Southern,26.9,6.72,,TBD
,,,Deshaun Fenwick,RB,Oregon State,79.2,6.6,,TBD
,,,Ja'Corey Brooks,WR,Alabama,46.2,6.6,,TBD
,,,Drake Anderson,RB,Arizona,72,6.55,,TBD
,,,Markese Stepp,RB,Nebraska,38.7,6.45,,TBD
,,,Sheldon Evans,RB,Marshall,83.2,6.4,,TBD
,,,DJ Stubbs,WR,Liberty,68.96,6.27,,TBD
,,,Joshua Mack,RB,Liberty,68.8,6.25,,TBD
,,,Roydell Williams,RB,Alabama,56.1,6.23,,TBD
,,,Jalen Berger,RB,Wisconsin,18.5,6.17,,TBD
,,,Jordan Mason,RB,Georgia Tech,73.9,6.16,,TBD
,,,Dezmon Jackson,RB,Oklahoma State,36.8,6.13,,TBD
,,,Isaac Rex,TE,Brigham Young,55.1,6.12,,TBD
,,,Travis Levy,RB,Boston College,73.2,6.1,,TBD
,,,Bryce Mitchell,WR,Toledo,48.3,6.04,,TBD
,,,Bobby Cole,RB,New Mexico,65.4,5.95,,TBD
,,,Sam Pinckney,WR,Georgia State,65.3,5.94,,TBD
,,,Xavier Arline,QB,Navy,41.28,5.9,,TBD
,,,Donald Chaney Jr.,RB,Miami (FL),11.8,5.9,,TBD
,,,Tyler Johnston III,QB,Alabama-Birmingham,29.22,5.84,,TBD
,,,Caleb Chapman,WR,Texas A&M,34,5.67,,TBD
,,,Ja'Shaun Poke,WR,Kent State,67.5,5.62,,TBD
,,,Jalen Holston,RB,Virginia Tech,39.1,5.59,,TBD
,,,Davis Allen,TE,Clemson,66.8,5.57,,TBD
,,,Luke McCaffrey,QB,Rice,49.72,5.52,,TBD
,,,Ty Thompson,QB,Oregon,16.48,5.49,,TBD
,,,Kyle McCord,QB,Ohio State,27.04,5.41,,TBD
,,,Austin Stogner,RB,Oklahoma,48.6,5.4,,TBD
,,,Miles Marshall,WR,Indiana,53.1,5.31,,TBD
,,,Johnathan Bennett,QB,Liberty,42.16,5.27,,TBD
,,,John Rhys Plumlee,QB,Mississippi,51.54,5.15,,TBD
,,,LD Brown,RB,Oklahoma State,20.6,5.15,,TBD
,,,Garrett Nussmeier,QB,Louisiana State,20.56,5.14,,TBD
,,,Jack Tuttle,QB,Indiana,30.62,5.1,,TBD
,,,Xzavier Henderson,WR,Florida,65.7,5.05,,TBD
,,,Bradley Rozner,WR,Rice,5,5,,TBD
,,,Kendall Milton,RB,Georgia,34.9,4.99,,TBD
,,,Justin Rogers,QB,Nevada-Las Vegas,29.6,4.93,,TBD
,,,Micah Kelly,RB,Toledo,58.8,4.9,,TBD
,,,Daetrich Harrington,RB,Appalachian State,29.3,4.88,,TBD
,,,CJ Lewis,WR,Boston College,33.1,4.73,,TBD
,,,Destin Coates,RB,Georgia State,28.1,4.68,,TBD
,,,Isaiah Jacobs,RB,Maryland,23.3,4.66,,TBD
,,,Traeshon Holden,WR,Alabama,50.9,4.63,,TBD
,,,Jha'Quan Jackson,WR,Tulane,55,4.58,,TBD
,,,Lopini Katoa,RB,BYU,54,4.5,,TBD
,,,Lyn-J Dixon,RB,Clemson,13.5,4.5,,TBD
,,,Cade Fortin,QB,South Florida,17.02,4.26,,TBD
,,,Knowledge McDaniel,RB,Marshall,16.7,4.18,,TBD
,,,Ryan Luehrman,TE,Ohio,41.7,4.17,,TBD
,,,Deonte Simpson,WR,North Texas,12.3,4.1,,TBD
,,,Kevin Mensah,RB,Connecticut,48.9,4.08,,TBD
,,,Koy Moore,WR,Louisiana State,12.1,4.03,,TBD
,,,Nick Tronti,QB,Florida Atlantic,23.7,3.95,,TBD
,,,George Pickens,WR,Georgia,15.7,3.92,,TBD
,,,Trey Cleveland,WR,Texas Tech,31.1,3.89,,TBD
,,,Dimitri Stanley,WR,Colorado,34.1,3.79,,TBD
,,,John Lovett,RB,Penn State,30.3,3.79,,TBD
,,,Ike Ogbogu,QB,Houston,22.64,3.77,,TBD
,,,Agiye Hall,WR,Alabama,11.2,3.73,,TBD
,,,Cornelius McCoy,WR,Georgia State,25.8,3.69,,TBD
,,,James Charles,RB,Florida Atlantic,44.1,3.68,,TBD
,,,Mason Garcia,QB,East Carolina,14.74,3.68,,TBD
,,,Joey Hobert,WR,Washington State,40.2,3.65,,TBD
,,,CT Thomas,WR,Boise State,21.4,3.57,,TBD
,,,Emeka Egbuka,WR,Ohio State,28.1,3.51,,TBD
,,,Jaylon Bester,RB,Miami (OH),10.4,3.47,,TBD
,,,Jirehl Brock,RB,Iowa State,40.7,3.39,,TBD
,,,Marcel Murray,RB,Arkansas State,13.4,3.35,,TBD
,,,Jalen Milroe,QB,Alabama,13.34,3.34,,TBD
,,,MarShawn Lloyd,RB,South Carolina,36.2,3.29,,TBD
,,,Preston Hutchinson,QB,Eastern Michigan,26.24,3.28,,TBD
,,,John Gentry,RB,Utah State,31.8,3.18,,TBD
,,,Trae Hall,QB,New Mexico,22.1,3.16,,TBD
,,,Sam Huard,QB,Washington,12.44,3.11,,TBD
,,,Kearis Jackson,WR,Georgia,45.1,3.01,,TBD
,,,Ben Ratzlaff,WR,Western Kentucky,23.8,2.98,,TBD
,,,Joey Gatewood,QB,Kentucky,26.88,2.69,,TBD
,,,Mulbah Car,RB,Houston,26.2,2.62,,TBD
,,,Ben Bresnahan,TE,Vanderbilt,20.4,2.55,,TBD
,,,Jack Sears,QB,Boise State,9.92,2.48,,TBD
,,,Trey Smith,RB,Wyoming,17.2,2.46,,TBD
,,,DeCarlos Brooks,RB,California,11.3,2.26,,TBD
,,,Kaylan Wiggins,QB,Florida International,4.48,2.24,,TBD
,,,E.J. Williams,WR,Clemson,15.6,2.23,,TBD
,,,Elijah Canion,WR,Auburn,8.6,2.15,,TBD
,,,Tim Baldwin Jr.,RB,Indiana,10.3,2.06,,TBD
,,,Demarkcus Bowman,RB,Florida,8.1,2.02,,TBD
,,,Ze'Vian Capers,WR,Auburn,11.4,1.9,,TBD
,,,Aaron Moore,WR,Old Dominion,1.9,1.9,,TBD
,,,Sam Noyer,QB,Oregon State,3.74,1.87,,TBD
,,,Javion Posey,QB,Florida Atlantic,10.74,1.53,,TBD
,,,Frank Ladson Jr.,WR,Clemson,5.9,1.48,,TBD
,,,Hunter Helms,QB,Clemson,2.72,1.36,,TBD
,,,Shai Werts,WR,Louisville,5.4,1.35,,TBD
,,,Paul Tyson,QB,Alabama,6,1.2,,TBD
,,,Darius Maberry,RB,Southern Mississippi,2.1,1.05,,TBD
,,,Jack West,QB,Stanford,2.9,0.97,,TBD
,,,Anthony Russo,QB,Michigan State,2.72,0.91,,TBD
,,,Chris Curry,RB,Utah,5.5,0.69,,TBD
,,,Jacob Zeno,QB,Baylor,1.34,0.67,,TBD
,,,Tate Martell,QB,Nevada-Las Vegas,1.28,0.64,,TBD
,,,Ty Evans,QB,Texas State,0.5,0.5,,TBD
,,,Preston Stone,QB,Southern Methodist,1.16,0.39,,TBD
,,,Bryson Lucero,QB,Alabama-Birmingham,0.3,0.3,,TBD
,,,Alan Bowman,QB,Michigan,0.36,0.18,,TBD
,,,Myles Brennan,QB,Louisiana State,0,0,,TBD
,,,Jack Abraham,QB,Mississippi State,0,0,,TBD
,,,Beau Corrales,WR,North Carolina,0,0,,TBD
,,,Jordan Johnson,WR,Central Florida,0,0,,TBD
,,,Sawyer Robertson,QB,Mississippi State,0,0,,TBD
,,,Oscar Adaway III,RB,North Texas,0,0,,TBD
,,,Grant Gunnell,QB,Memphis,0,0,,TBD
,,,Luke Anthony,QB,Louisiana Tech,0,0,,TBD
,,,Kobe Lewis,RB,Central Michigan,0,0,,TBD
,,,Theo Wease,WR,Oklahoma,0,0,,TBD
,,,J.T. Shrout,QB,Colorado,0,0,,TBD
,,,Cam Porter,RB,Northwestern,0,0,,TBD
,,,Tristan Gebbia,QB,Oregon State,0,0,,TBD
,,,Willie Taggart Jr.,QB,Florida Atlantic,0,0,,TBD
,,,Michael Johnson Jr.,QB,Florida Atlantic,0,0,,TBD
,,,Troy Omeire,WR,Texas,0,0,,TBD
,,,David Bailey,RB,Boston College,0,0,,TBD
,,,Arik Gilbert,WR,Georgia,0,0,,TBD
,,,Danny Davis III,WR,Wisconsin,0,0,,TBD
,,,Kendric Pryor,WR,Wisconsin,0,0,,TBD
,,,Qua Davis,WR,Mississippi,0,0,,TBD
,,,Kevin Harris,RB,South Carolina,0,0,,TBD
,,,Teon Dollard,RB,Akron,0,0,,TBD
,,,John Emery Jr.,RB,Louisiana State,0,0,,TBD
,,,Eric Najarian,QB,Maryland,0,0,,TBD
,,,Fred Orr,RB,Tennessee,0,0,,TBD
,,,,,,,,,
caleb-williams-3,Southern California,Jeremy,Caleb Williams,QB,USC,,,,
,Texas,Ryan B.,Quinn Ewers,QB,Ohio State,,,,
'''
players = '''
{
  "players": [
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Kobe",
      "last_name": "Hudson",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Jaylon",
      "last_name": "Griffin",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Jordan",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Amari",
      "last_name": "Johnson",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Ryan",
      "last_name": "O'Keefe",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Dionte",
      "last_name": "Marks",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Kemore",
      "last_name": "Gamble",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Alec",
      "last_name": "Holler",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Mikey",
      "last_name": "Keene",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "John",
      "last_name": "Plumlee",
      "position": "QB",
      "year": "Rhys SR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Joey",
      "last_name": "Gatewood",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Isaiah",
      "last_name": "Bowser",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Johnny",
      "last_name": "Richardson",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Central Florida",
      "team_name": "Knights",
      "first_name": "Mark-Antony",
      "last_name": "Richards",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Jadon",
      "last_name": "Thompson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Nick",
      "last_name": "Mardner",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Tyler",
      "last_name": "Scott",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Chris",
      "last_name": "Scott",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Tre",
      "last_name": "Tucker",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Will",
      "last_name": "Pauling",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Josh",
      "last_name": "Whyle",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Leonard",
      "last_name": "Taylor",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Payten",
      "last_name": "Singletary",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Evan",
      "last_name": "Prater",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Ben",
      "last_name": "Bryant",
      "position": "QB",
      "year": "SR/TR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Brady",
      "last_name": "Lichtenberg",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Corey",
      "last_name": "Kiner",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Ryan",
      "last_name": "Montgomery",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Cincinnati",
      "team_name": "Bearcats",
      "first_name": "Charles",
      "last_name": "McClelland",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Jsi",
      "last_name": "Hatfield",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Taji",
      "last_name": "Hudson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Jaylen",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Tyler",
      "last_name": "Savage",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Andre",
      "last_name": "Pegues",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Maceo",
      "last_name": "Donald",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Kerry",
      "last_name": "King",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Jhari",
      "last_name": "Patterson",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Ryan",
      "last_name": "Jones",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Shane",
      "last_name": "Calhoun",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Aaron",
      "last_name": "Jarman",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Holton",
      "last_name": "Ahlers",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Mason",
      "last_name": "Garcia",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Ryan",
      "last_name": "Stubblefield",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Keaton",
      "last_name": "Mitchell",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Rahjai",
      "last_name": "Harris",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "East Carolina",
      "team_name": "Pirates",
      "first_name": "Joseph",
      "last_name": "McKay",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "KeSean",
      "last_name": "Carter",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "C.J.",
      "last_name": "Guidry",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Matthew",
      "last_name": "Golden",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Samuel",
      "last_name": "Brown",
      "position": "WR",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Nathaniel",
      "last_name": "Dell",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Joseph",
      "last_name": "Manjack IV",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Christian",
      "last_name": "Trahan",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Logan",
      "last_name": "Compton",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Clayton",
      "last_name": "Tune",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Ike",
      "last_name": "Ogbogu",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Lucas",
      "last_name": "Coley",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Ta'Zhawn",
      "last_name": "Henry",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Brandon",
      "last_name": "Campbell",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Houston",
      "team_name": "Cougars",
      "first_name": "Stacy",
      "last_name": "Sneed",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Eddie",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Koby",
      "last_name": "Drake",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Roc",
      "last_name": "Taylor",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Gabriel",
      "last_name": "Rogers",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Marcayll",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Zach",
      "last_name": "Switzer",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Javon",
      "last_name": "Ivory",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Joseph",
      "last_name": "Scates",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Cameron",
      "last_name": "Wright",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Caden",
      "last_name": "Prieskorn",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Anthony",
      "last_name": "Landphere",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Seth",
      "last_name": "Henigan",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Tevin",
      "last_name": "Carter",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Brandon",
      "last_name": "Thomas",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Rodrigues",
      "last_name": "Clark",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Marquavius",
      "last_name": "Weaver",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Asa",
      "last_name": "Martin",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "Jevyon",
      "last_name": "Ducker",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Memphis",
      "team_name": "Tigers",
      "first_name": "JP",
      "last_name": "Martin",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Jayden",
      "last_name": "Umbarger",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Kroy",
      "last_name": "Myers",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Zachary",
      "last_name": "Kuhlman",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Mark",
      "last_name": "Walker",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Camari",
      "last_name": "Williams",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Michael",
      "last_name": "Naze",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Tai",
      "last_name": "Lavatai",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Xavier",
      "last_name": "Arline",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Maasai",
      "last_name": "Maynor",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Anton",
      "last_name": "Hall Jr.",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Logan",
      "last_name": "Point",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Navy",
      "team_name": "Midshipmen",
      "first_name": "Mike",
      "last_name": "Mauai",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Jordan",
      "last_name": "Kerley",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Beau",
      "last_name": "Barker",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Rashee",
      "last_name": "Rice",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Roderick",
      "last_name": "Daniels Jr.",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Dylan",
      "last_name": "Goffney",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Austin",
      "last_name": "Upshaw",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Simon",
      "last_name": "Gonzalez",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Nolan",
      "last_name": "Matthews-Harris",
      "position": "TE",
      "year": "JR/TR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Tanner",
      "last_name": "Mordecai",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Preston",
      "last_name": "Stone",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Camar",
      "last_name": "Wheaton",
      "position": "RB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Tre",
      "last_name": "Siggers",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "SMU",
      "team_name": "Mustangs",
      "first_name": "Tyler",
      "last_name": "Lavine",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Xavier",
      "last_name": "Weaver",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Omarion",
      "last_name": "Dollison",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Yusuf",
      "last_name": "Terry",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Jimmy",
      "last_name": "Horn Jr.",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Sean",
      "last_name": "Atkins",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Chris",
      "last_name": "Carter",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Timmy",
      "last_name": "McClain",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Jaren",
      "last_name": "Mangham",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Kelley",
      "last_name": "Joiner",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Brian",
      "last_name": "Battie",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Vincent",
      "last_name": "Davis",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "South Florida",
      "team_name": "Bulls",
      "first_name": "Christopher",
      "last_name": "Townsel",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Amad",
      "last_name": "Anderson Jr.",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Kadas",
      "last_name": "Reams",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Zae",
      "last_name": "Baines",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Jose",
      "last_name": "Barbon",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Shekuna",
      "last_name": "Kamara",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Malik",
      "last_name": "Cooper",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "De'Von",
      "last_name": "Fox",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Kwesi",
      "last_name": "Evans",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "David",
      "last_name": "Martin-Robinson",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Jordan",
      "last_name": "Smith",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "James",
      "last_name": "Della Pesca",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "D'Wan",
      "last_name": "Mathis",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Mariano",
      "last_name": "Valenti",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Edward",
      "last_name": "Saydee",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Darvon",
      "last_name": "Hubbard",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Temple",
      "team_name": "Owls",
      "first_name": "Trey",
      "last_name": "Blair",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Duece",
      "last_name": "Watts",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Shae",
      "last_name": "Wyatt",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Phat",
      "last_name": "Watts",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Jha'Quan",
      "last_name": "Jackson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Bryce",
      "last_name": "Bohanon",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Tyrick",
      "last_name": "James",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Michael",
      "last_name": "Pratt",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Justin",
      "last_name": "Ibieta",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Kai",
      "last_name": "Horton",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Cameron",
      "last_name": "Carroll",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Tulane",
      "team_name": "Green Wave",
      "first_name": "Tyjae",
      "last_name": "Spears",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Isaiah",
      "last_name": "Epps",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Malachai",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "JuanCarlos",
      "last_name": "Santana",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Malachai",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Keylon",
      "last_name": "Stokes",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Kamdyn",
      "last_name": "Benjamin",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Ethan",
      "last_name": "Hall",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Bayne",
      "last_name": "Tryon",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Davis",
      "last_name": "Brin",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Roman",
      "last_name": "Fuller",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Braylon",
      "last_name": "Braxton",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Deneric",
      "last_name": "Prince",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Anthony",
      "last_name": "Watkins",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Steven",
      "last_name": "Anderson",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Grant",
      "last_name": "Sawyer",
      "position": "RB",
      "year": "GR"
    },
    {
      "team_city": "Tulsa",
      "team_name": "Golden Hurricane",
      "first_name": "Mitchell",
      "last_name": "Kulkin",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Jaden",
      "last_name": "Williams",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Lewis",
      "last_name": "Bond",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Dino",
      "last_name": "Tomlin",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Zay",
      "last_name": "Flowers",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Dante",
      "last_name": "Reynolds",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Joseph",
      "last_name": "Griffin",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Jaelen",
      "last_name": "Gill",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Taji",
      "last_name": "Johnson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "George",
      "last_name": "Takacs",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Joey",
      "last_name": "Luchetti",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Spencer",
      "last_name": "Witter",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Phil",
      "last_name": "Jurkovec",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Emmett",
      "last_name": "Morehead",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Pat",
      "last_name": "Garwo III",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Alec",
      "last_name": "Sinkfield",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "Boston College",
      "team_name": "Eagles",
      "first_name": "Xavier",
      "last_name": "Coleman",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Joseph",
      "last_name": "Ngata",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Dacari",
      "last_name": "Collins",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Beaux",
      "last_name": "Collins",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Troy",
      "last_name": "Stellato",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Antonio",
      "last_name": "Williams",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "E.J.",
      "last_name": "Williams",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Brannon",
      "last_name": "Spector",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Will",
      "last_name": "Taylor",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Davis",
      "last_name": "Allen",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Jake",
      "last_name": "Briningstool",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Sage",
      "last_name": "Ennis",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "DJ",
      "last_name": "Uiagalelei",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Cade",
      "last_name": "Klubnik",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Hunter",
      "last_name": "Helms",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Will",
      "last_name": "Shipley",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Kobe",
      "last_name": "Pace",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Clemson",
      "team_name": "Tigers",
      "first_name": "Phil",
      "last_name": "Mafah",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Darrell",
      "last_name": "Harding Jr.",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Sahmir",
      "last_name": "Hagans",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Eli",
      "last_name": "Pancol",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Luca",
      "last_name": "Diamont",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Jalon",
      "last_name": "Calhoun",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Jontavis",
      "last_name": "Robertson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Nicky",
      "last_name": "Dalmolin",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Cole",
      "last_name": "Finney",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Riley",
      "last_name": "Leonard",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Jordan",
      "last_name": "Moore",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Jordan",
      "last_name": "Waters",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Jaquez",
      "last_name": "Moore",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Duke",
      "team_name": "Blue Devils",
      "first_name": "Jaylen",
      "last_name": "Coleman",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Malik",
      "last_name": "McClain",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Johnny",
      "last_name": "Wilson",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Mycah",
      "last_name": "Pittman",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Ontaria",
      "last_name": "Wilson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Joshua",
      "last_name": "Burrell",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Ja'Khi",
      "last_name": "Douglas",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Keyshawn",
      "last_name": "Helton",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Camren",
      "last_name": "McDonald",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Wyatt",
      "last_name": "Rector",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Preston",
      "last_name": "Daniel",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Jordan",
      "last_name": "Travis",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Tate",
      "last_name": "Rodemaker",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "AJ",
      "last_name": "Duffy",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Trey",
      "last_name": "Benson",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Treshaun",
      "last_name": "Ward",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Florida State",
      "team_name": "Seminoles",
      "first_name": "Lawrance",
      "last_name": "Toafili",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Malachi",
      "last_name": "Carter",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Leo",
      "last_name": "Blackburn",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "D.J.",
      "last_name": "Moore",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Kalani",
      "last_name": "Norris",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Ryan",
      "last_name": "King",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "James",
      "last_name": "BlackStrain",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Nate",
      "last_name": "McCollum",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Malik",
      "last_name": "Rutherford",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Peje'",
      "last_name": "Harris",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Dylan",
      "last_name": "Leonard",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Luke",
      "last_name": "Benson",
      "position": "TE",
      "year": "JR/TR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Jeff",
      "last_name": "Sims",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Zach",
      "last_name": "Gibson",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Brody",
      "last_name": "Rhodes",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Dontae",
      "last_name": "Smith",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Hassan",
      "last_name": "Hall",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Georgia Tech",
      "team_name": "Yellow Jackets",
      "first_name": "Antonio",
      "last_name": "Martin",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Tyler",
      "last_name": "Hudson",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Elijah",
      "last_name": "Downing",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Dee",
      "last_name": "Wiggins",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Ahmari",
      "last_name": "Huggins-Bruce",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Braden",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Josh",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Dez",
      "last_name": "Melton",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Duane",
      "last_name": "Martin",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Francis",
      "last_name": "Sherman",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Marshon",
      "last_name": "Ford",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Isaac",
      "last_name": "Martin",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Malik",
      "last_name": "Cunningham",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Khalib",
      "last_name": "Johnson",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Brock",
      "last_name": "Domann",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Jalen",
      "last_name": "Mitchell",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Tiyon",
      "last_name": "Evans",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Louisville",
      "team_name": "Cardinals",
      "first_name": "Trevion",
      "last_name": "Cooley",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Jacolby",
      "last_name": "George",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Romello",
      "last_name": "Brinson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Michael",
      "last_name": "Redding III",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Key'Shawn",
      "last_name": "Smith",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Frank",
      "last_name": "Ladson Jr.",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Xavier",
      "last_name": "Restrepo",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Brashard",
      "last_name": "Smith",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Will",
      "last_name": "Mallory",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Elijah",
      "last_name": "Arroyo",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Jaleel",
      "last_name": "Skinner",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Tyler",
      "last_name": "Van Dyke",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Jake",
      "last_name": "Garcia",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Jacurri",
      "last_name": "Brown",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Henry",
      "last_name": "Parrish Jr.",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Jaylan",
      "last_name": "Knighton",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Miami",
      "team_name": "Hurricanes",
      "first_name": "Donald",
      "last_name": "Chaney Jr.",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Antoine",
      "last_name": "Green",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "J.J.",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Tylee",
      "last_name": "Craft",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Kobe",
      "last_name": "Paysour",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Justin",
      "last_name": "Olson",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Josh",
      "last_name": "Downs",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Gavin",
      "last_name": "Blackwell",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Bryson",
      "last_name": "Nesbit",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Kamari",
      "last_name": "Morales",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "John",
      "last_name": "Copenhaver",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Jacolby",
      "last_name": "Criswell",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Drake",
      "last_name": "Maye",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Conner",
      "last_name": "Harrell",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "British",
      "last_name": "Brooks",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "D.J.",
      "last_name": "Jones",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "North Carolina",
      "team_name": "Tar Heels",
      "first_name": "Elijah",
      "last_name": "Green",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Devin",
      "last_name": "Carter",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Anthony",
      "last_name": "Smith",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Josh",
      "last_name": "Crabtree",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Darryl",
      "last_name": "Jones",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Keyon",
      "last_name": "Lesane",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Thayer",
      "last_name": "Thomas",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Porter",
      "last_name": "Rooks",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Julian",
      "last_name": "Gray",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Kameron",
      "last_name": "Walker",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Fred",
      "last_name": "Seabrough Jr.",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Ezemdi",
      "last_name": "Udoh",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Trent",
      "last_name": "Pennix",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Christopher",
      "last_name": "Toudle",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Devin",
      "last_name": "Leary",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Ben",
      "last_name": "Finley",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Jordan",
      "last_name": "Houston",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Demie",
      "last_name": "Sumo-Karngbaye",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "North Carolina State",
      "team_name": "Wolfpack",
      "first_name": "Michael",
      "last_name": "Allen",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Jared",
      "last_name": "Wayne",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Jaden",
      "last_name": "Bradley",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Konata",
      "last_name": "Mumpfield",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Jaylon",
      "last_name": "Barden",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Gavin",
      "last_name": "Bartholomew",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Kedon",
      "last_name": "Slovis",
      "position": "QB",
      "year": "SR/TR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Nick",
      "last_name": "Patti",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Israel",
      "last_name": "Abanikanda",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Vincent",
      "last_name": "Davis",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Rodney",
      "last_name": "Hammond Jr.",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Buddy",
      "last_name": "Mack III",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Pittsburgh",
      "team_name": "Panthers",
      "first_name": "Shayne",
      "last_name": "Simon",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Anthony",
      "last_name": "Queeley",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Umari",
      "last_name": "Hatcher",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "CJ",
      "last_name": "Hayes",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Damien",
      "last_name": "Alford",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Oronde",
      "last_name": "Gadsden II",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Kendall",
      "last_name": "Long",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Courtney",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Devaughn",
      "last_name": "Cooper",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Trebor",
      "last_name": "Pena",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Maximilian",
      "last_name": "Mang",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Steven",
      "last_name": "Mahar Jr.",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Garrett",
      "last_name": "Shrader",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Justin",
      "last_name": "Lamson",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Dan",
      "last_name": "Villari",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Sean",
      "last_name": "Tucker",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Juwaun",
      "last_name": "Price",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "LeQuint",
      "last_name": "Allen",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Syracuse",
      "team_name": "Orange",
      "first_name": "Chris",
      "last_name": "Elmore",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Dontayvion",
      "last_name": "Wicks",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Keytaon",
      "last_name": "Thompson",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Lavel",
      "last_name": "Davis Jr.",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Malachi",
      "last_name": "Fields",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Billy",
      "last_name": "Kemp IV",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Demick",
      "last_name": "Starling",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Josh",
      "last_name": "Clifford",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Grant",
      "last_name": "Misch",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Sackett",
      "last_name": "Wood Jr.",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Brennan",
      "last_name": "Armstrong",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Jay",
      "last_name": "Woolfolk",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Mike",
      "last_name": "Hollins",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Ronnie",
      "last_name": "Walker Jr.",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Virginia",
      "team_name": "Cavaliers",
      "first_name": "Amaad",
      "last_name": "Foston",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Kaleb",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Stephen",
      "last_name": "Gosnell",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Christian",
      "last_name": "Moss",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Da'Wain",
      "last_name": "Lofton",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Dallan",
      "last_name": "Wright",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "DJ",
      "last_name": "Sims",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Jadan",
      "last_name": "Blue",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Jaylen",
      "last_name": "Jones",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Tucker",
      "last_name": "Holloway",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Nick",
      "last_name": "Gallo",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Drake",
      "last_name": "DeIuliis",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Connor",
      "last_name": "Blumrick",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Grant",
      "last_name": "Wells",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Jason",
      "last_name": "Brown",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Tahj",
      "last_name": "Bullock",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Malachi",
      "last_name": "Thomas",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Jalen",
      "last_name": "Holston",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Virginia Tech",
      "team_name": "Hokies",
      "first_name": "Chance",
      "last_name": "Black",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Donavon",
      "last_name": "Greene",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Jackson",
      "last_name": "Hensley",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "A.T.",
      "last_name": "Perry",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Jahmal",
      "last_name": "Banks",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Taylor",
      "last_name": "Morin",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Ke'Shawn",
      "last_name": "Williams",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Blake",
      "last_name": "Whiteheart",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Jaeger",
      "last_name": "Bull",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Sam",
      "last_name": "Hartman",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Michael",
      "last_name": "Kern",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Mitch",
      "last_name": "Griffis",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Justice",
      "last_name": "Ellison",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Christian",
      "last_name": "Turner",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Wake Forest",
      "team_name": "Demon Deacons",
      "first_name": "Demond",
      "last_name": "Claiborne",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Casey",
      "last_name": "Washington",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Brian",
      "last_name": "Hightower",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Hank",
      "last_name": "Beatty",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Isaiah",
      "last_name": "Williams",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Miles",
      "last_name": "Scott",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Khmari",
      "last_name": "Thompson",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Pat",
      "last_name": "Bryant",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Shawn",
      "last_name": "Miller",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Ashton",
      "last_name": "Hollins",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Luke",
      "last_name": "Ford",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Owen",
      "last_name": "Anderson",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Griffin",
      "last_name": "Moore",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Tip",
      "last_name": "Reiman",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Michael",
      "last_name": "Marchese",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Henry",
      "last_name": "Boyer",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Tommy",
      "last_name": "DeVito",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Artur",
      "last_name": "Sitkowski",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Ryan",
      "last_name": "Johnson",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Chase",
      "last_name": "Brown",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Josh",
      "last_name": "McCray",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Illinois",
      "team_name": "Fighting Illini",
      "first_name": "Aidan",
      "last_name": "Laughery",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Cam",
      "last_name": "Camper",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Malachi",
      "last_name": "Holt-Bennett",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "David",
      "last_name": "Baker",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Emery",
      "last_name": "Simmons",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Javon",
      "last_name": "Swinton",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Jaquez",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "D.J.",
      "last_name": "Matthews Jr.",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Omar",
      "last_name": "Cooper Jr.",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Kamryn",
      "last_name": "Perry",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "AJ",
      "last_name": "Barner",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Aaron",
      "last_name": "Steinfeldt",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Brody",
      "last_name": "Foley",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Connor",
      "last_name": "Bazelak",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Jack",
      "last_name": "Tuttle",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Donaven",
      "last_name": "McCulley",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Shaun",
      "last_name": "Shivers",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Josh",
      "last_name": "Henderson",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Indiana",
      "team_name": "Hoosiers",
      "first_name": "Jaylin",
      "last_name": "Lucas",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Keagan",
      "last_name": "Johnson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Jackson",
      "last_name": "Ritter",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Arland",
      "last_name": "Bruce IV",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Nico",
      "last_name": "Ragaini",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Sam",
      "last_name": "LaPorta",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Luke",
      "last_name": "Lachey",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Steven",
      "last_name": "Stilianos",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Spencer",
      "last_name": "Petras",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Alex",
      "last_name": "Padilla",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Joe",
      "last_name": "Labas",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Gavin",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Leshon",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Monte",
      "last_name": "Pottebaum",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Turner",
      "last_name": "Pallissard",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Iowa",
      "team_name": "Hawkeyes",
      "first_name": "Mike",
      "last_name": "Timm",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Dontay",
      "last_name": "Demus Jr.",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Jeshaun",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Rakim",
      "last_name": "Jarrett",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Marcus",
      "last_name": "Fleming",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Corey",
      "last_name": "Dyches",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Taulia",
      "last_name": "Tagovailoa",
      "position": "QB",
      "year": "SR/TR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Challen",
      "last_name": "Faamatau",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Maryland",
      "team_name": "Terrapins",
      "first_name": "Colby",
      "last_name": "McDonald",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Roman",
      "last_name": "Wilson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Darrius",
      "last_name": "Clemons",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Cristian",
      "last_name": "Dixon",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Cornelius",
      "last_name": "Johnson",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Andrel",
      "last_name": "Anthony",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Amorion",
      "last_name": "Walker",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Ronnie",
      "last_name": "Bell",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "A.J.",
      "last_name": "Henning",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Tyler",
      "last_name": "Morris",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Erick",
      "last_name": "All",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Luke",
      "last_name": "Schoonmaker",
      "position": "TE",
      "year": "GR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Joel",
      "last_name": "Honigford",
      "position": "TE",
      "year": "GR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Cade",
      "last_name": "McNamara",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "J.J.",
      "last_name": "McCarthy",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Davis",
      "last_name": "Warren",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Blake",
      "last_name": "Corum",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Donovan",
      "last_name": "Edwards",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan",
      "team_name": "Wolverines",
      "first_name": "Tavierre",
      "last_name": "Dunlap",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Jayden",
      "last_name": "Reed",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Montorie",
      "last_name": "Foster",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Germie",
      "last_name": "Bernard",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Keon",
      "last_name": "Coleman",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Christian",
      "last_name": "Fitzpatrick",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Antonio",
      "last_name": "Gates Jr.",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Tre",
      "last_name": "Mosley",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Terry",
      "last_name": "Lockett Jr.",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Tyrell",
      "last_name": "Henry",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Daniel",
      "last_name": "Barker",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Maliq",
      "last_name": "Carr",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Jack",
      "last_name": "Nickel",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Payton",
      "last_name": "Thorne",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Noah",
      "last_name": "Kim",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Katin",
      "last_name": "Houser",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Jalen",
      "last_name": "Berger",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Jarek",
      "last_name": "Broussard",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Michigan State",
      "team_name": "Spartans",
      "first_name": "Davion",
      "last_name": "Primm",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Chris",
      "last_name": "Autman-Bell",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Dylan",
      "last_name": "Wright",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Daniel",
      "last_name": "Jackson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Le'Meke",
      "last_name": "Brockington",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Ike",
      "last_name": "White",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Michael",
      "last_name": "Brown-Stephens",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Clay",
      "last_name": "Geary",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Brevyn",
      "last_name": "Spann-Ford",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Nick",
      "last_name": "Kallerup",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Jameson",
      "last_name": "Geers",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Tanner",
      "last_name": "Morgan",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Cole",
      "last_name": "Kramer",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Athan",
      "last_name": "Kaliakmanis",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Mohamed",
      "last_name": "Ibrahim",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Trey",
      "last_name": "Potts",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Minnesota",
      "team_name": "Golden Gophers",
      "first_name": "Bryce",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Trey",
      "last_name": "Palmer",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Omar",
      "last_name": "Manning",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Isaiah",
      "last_name": "Garcia-Castaneda",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Oliver",
      "last_name": "Martin",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Wyatt",
      "last_name": "Liewer",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Alante",
      "last_name": "Brown",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Brody",
      "last_name": "Belt",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Travis",
      "last_name": "Vokolek",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Chris",
      "last_name": "Hickman",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Chancellor",
      "last_name": "Brewington",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Casey",
      "last_name": "Thompson",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Logan",
      "last_name": "Smothers",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Chubba",
      "last_name": "Purdy",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Gabe",
      "last_name": "Ervin Jr.",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Rahmir",
      "last_name": "Johnson",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Nebraska",
      "team_name": "Cornhuskers",
      "first_name": "Jaquez",
      "last_name": "Yant",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Malik",
      "last_name": "Washington",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Raymond",
      "last_name": "Niro III",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Bryce",
      "last_name": "Kirtz",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Jacob",
      "last_name": "Gill",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Genson",
      "last_name": "Hooper Price",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Charlie",
      "last_name": "Mangieri",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Ryan",
      "last_name": "Hilinski",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Brendan",
      "last_name": "Sullivan",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Cole",
      "last_name": "Freeman",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Evan",
      "last_name": "Hull",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Northwestern",
      "team_name": "Wildcats",
      "first_name": "Andrew",
      "last_name": "Clair",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Marvin",
      "last_name": "Harrison Jr.",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Kamryn",
      "last_name": "Babb",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Xavier",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Julian",
      "last_name": "Fleming",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Jayden",
      "last_name": "Ballard",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Kaleb",
      "last_name": "Brown",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Jaxon",
      "last_name": "Smith-Njigba",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Emeka",
      "last_name": "Egbuka",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Kyion",
      "last_name": "Grayes",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Cade",
      "last_name": "Stover",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Joe",
      "last_name": "Royer",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Mitch",
      "last_name": "Rossi",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "C.J.",
      "last_name": "Stroud",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Kyle",
      "last_name": "McCord",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Devin",
      "last_name": "Brown",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "TreVeyon",
      "last_name": "Henderson",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Miyan",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Ohio State",
      "team_name": "Buckeyes",
      "first_name": "Evan",
      "last_name": "Pryor",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Parker",
      "last_name": "Washington",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Malick",
      "last_name": "Meiga",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Harrison",
      "last_name": "Wallace III",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "KeAndre",
      "last_name": "Lambert-Smith",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Jaden",
      "last_name": "Dottin",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Kaden",
      "last_name": "Saunders",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Mitchell",
      "last_name": "Tinsley",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Liam",
      "last_name": "Clifford",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Mason",
      "last_name": "Stahl",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Brenton",
      "last_name": "Strange",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Theo",
      "last_name": "Johnson",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Tyler",
      "last_name": "Warren",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Sean",
      "last_name": "Clifford",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Christian",
      "last_name": "Veilleux",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Drew",
      "last_name": "Allar",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Keyvone",
      "last_name": "Lee",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Devyn",
      "last_name": "Ford",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Penn State",
      "team_name": "Nittany Lions",
      "first_name": "Nicholas",
      "last_name": "Singleton",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Milton",
      "last_name": "Wright",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Mershawn",
      "last_name": "Rice",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Collin",
      "last_name": "Sullivan",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Broc",
      "last_name": "Thompson",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Abdur-Rahmaan",
      "last_name": "Yaseen",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Preston",
      "last_name": "Terrell",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Tyrone",
      "last_name": "Tracy",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "TJ",
      "last_name": "Sheffield",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Deion",
      "last_name": "Burks",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Payne",
      "last_name": "Durham",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Garrett",
      "last_name": "Miller",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Paul",
      "last_name": "Piferi",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Aidan",
      "last_name": "O'Connell",
      "position": "QB",
      "year": "GR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Austin",
      "last_name": "Burton",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Michael",
      "last_name": "Alaimo",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "King",
      "last_name": "Doerue",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Sampson",
      "last_name": "James",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Purdue",
      "team_name": "Boilermakers",
      "first_name": "Dylan",
      "last_name": "Downing",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Taj",
      "last_name": "Harris",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Shameen",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Sean",
      "last_name": "Ryan",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Isaiah",
      "last_name": "Washington",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Aron",
      "last_name": "Cruickshank",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Joshua",
      "last_name": "Youngblood",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Brandon",
      "last_name": "Sanders",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Johnny",
      "last_name": "Langan",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Victor",
      "last_name": "Konopka",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Matt",
      "last_name": "Alaimo",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Noah",
      "last_name": "Vedral",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Gavin",
      "last_name": "Wimsatt",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Evan",
      "last_name": "Simon",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Kyle",
      "last_name": "Monangai",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Aaron",
      "last_name": "Young",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Rutgers",
      "team_name": "Scarlet Knights",
      "first_name": "Al-Shadee",
      "last_name": "Salaam",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Chimere",
      "last_name": "Dike",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Keontez",
      "last_name": "Lewis",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Dean",
      "last_name": "Engram",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Skyler",
      "last_name": "Bell",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Markus",
      "last_name": "Allen",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Stephan",
      "last_name": "Bracey Jr.",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Jack",
      "last_name": "Eschenbach",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Clay",
      "last_name": "Cundiff",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Jaylan",
      "last_name": "Franklin",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Hayden",
      "last_name": "Rucci",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Cole",
      "last_name": "Dakovich",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Cam",
      "last_name": "Large",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Graham",
      "last_name": "Mertz",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Chase",
      "last_name": "Wolf",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Deacon",
      "last_name": "Hill",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Braelon",
      "last_name": "Allen",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Chez",
      "last_name": "Mellusi",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Isaac",
      "last_name": "Guerendo",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Jackson",
      "last_name": "Acker",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Riley",
      "last_name": "Nowakowski",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Wisconsin",
      "team_name": "Badgers",
      "first_name": "Garrison",
      "last_name": "Solliday",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Gavin",
      "last_name": "Holmes",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Hal",
      "last_name": "Presley",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Josh",
      "last_name": "Cameron",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Javon",
      "last_name": "Gipson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Monaray",
      "last_name": "Baldwin",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Seth",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Ben",
      "last_name": "Sims",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Drake",
      "last_name": "Dabney",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Gavin",
      "last_name": "Yates",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Blake",
      "last_name": "Shapen",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Kyron",
      "last_name": "Drones",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "CJ",
      "last_name": "Rogers",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Taye",
      "last_name": "McWilliams",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Craig",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Josh",
      "last_name": "Fleeks",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Devin",
      "last_name": "Neal",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Cisco",
      "last_name": "Caston",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Lorando",
      "last_name": "Johnson",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Romario",
      "last_name": "Noel",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Baylor",
      "team_name": "Bears",
      "first_name": "Alfonzo",
      "last_name": "Allen",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Xavier",
      "last_name": "Hutchinson",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Darren",
      "last_name": "Wilson Jr.",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Aidan",
      "last_name": "Bitter",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Sean",
      "last_name": "Shaw Jr.",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Greg",
      "last_name": "Gaines III",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Tristan",
      "last_name": "Michaud",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Jaylin",
      "last_name": "Noel",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Daniel",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Easton",
      "last_name": "Dean",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Tyler",
      "last_name": "Moore",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Jared",
      "last_name": "Rus",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "DeShawn",
      "last_name": "Hanika",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Hunter",
      "last_name": "Dekkers",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Ashton",
      "last_name": "Cook",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Rocco",
      "last_name": "Becht",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Jirehl",
      "last_name": "Brock",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Deon",
      "last_name": "Silas",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Iowa State",
      "team_name": "Cyclones",
      "first_name": "Eli",
      "last_name": "Sanders",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Luke",
      "last_name": "Grimm",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Trevor",
      "last_name": "Wilson",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Lawrence",
      "last_name": "Arnold",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Douglas",
      "last_name": "Emilien",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Steven",
      "last_name": "McBride",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Mason",
      "last_name": "Fairchild",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Trevor",
      "last_name": "Kardell",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Tevita",
      "last_name": "Noa",
      "position": "TE",
      "year": "JR/TR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Jalon",
      "last_name": "Daniels",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Jason",
      "last_name": "Bean",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Jack",
      "last_name": "Jackson",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Devin",
      "last_name": "Neal",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Ky",
      "last_name": "Thomas",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Kansas",
      "team_name": "Jayhawks",
      "first_name": "Sevion",
      "last_name": "Morrison",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Malik",
      "last_name": "Knowles",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Keenan",
      "last_name": "Garber",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Xavier",
      "last_name": "Loyd",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Phillip",
      "last_name": "Brooks",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Kade",
      "last_name": "Warner",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "RJ",
      "last_name": "Garcia II",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Sammy",
      "last_name": "Wheeler",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Konner",
      "last_name": "Fox",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Will",
      "last_name": "Swanson",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Adrian",
      "last_name": "Martinez",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Will",
      "last_name": "Howard",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Jake",
      "last_name": "Rubley",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Deuce",
      "last_name": "Vaughn",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "DJ",
      "last_name": "Giddens",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Devrin",
      "last_name": "Weathers",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Ben",
      "last_name": "Sinnott",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Jax",
      "last_name": "Dineen",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Christian",
      "last_name": "Moore",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Kobe",
      "last_name": "Savage",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Kansas State",
      "team_name": "Wildcats",
      "first_name": "Cincere",
      "last_name": "Mason",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Theo",
      "last_name": "Wease",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Trevon",
      "last_name": "West",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Jayden",
      "last_name": "Gibson",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Drake",
      "last_name": "Stoops",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Jalil",
      "last_name": "Farooq",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Nic",
      "last_name": "Anderson",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Marvin",
      "last_name": "Mims",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Brian",
      "last_name": "Darby",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Brayden",
      "last_name": "Willis",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Daniel",
      "last_name": "Parker",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Kaden",
      "last_name": "Helms",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Dillon",
      "last_name": "Gabriel",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Nick",
      "last_name": "Evers",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Ralph",
      "last_name": "Rucker",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Eric",
      "last_name": "Gray",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Marcus",
      "last_name": "Major",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Oklahoma",
      "team_name": "Sooners",
      "first_name": "Jovantae",
      "last_name": "Barnes",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Jaden",
      "last_name": "Bray",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Bryson",
      "last_name": "Green",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Langston",
      "last_name": "Anderson",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Rashod",
      "last_name": "Owens",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Talyn",
      "last_name": "Shettron",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Brennan",
      "last_name": "Presley",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "John",
      "last_name": "Richardson",
      "position": "WR",
      "year": "Paul FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Braydon",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Blaine",
      "last_name": "Green",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Cale",
      "last_name": "Cabbiness",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Spencer",
      "last_name": "Sanders",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Gunnar",
      "last_name": "Gundy",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Garret",
      "last_name": "Rangel",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Dominic",
      "last_name": "Richardson",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Jaden",
      "last_name": "Nixon",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Oklahoma State",
      "team_name": "Cowboys",
      "first_name": "Zach",
      "last_name": "Middleton",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Quincy",
      "last_name": "Brown",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Savion",
      "last_name": "Williams",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Quentin",
      "last_name": "Johnston",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Blake",
      "last_name": "Nowell",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Derius",
      "last_name": "Davis",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Taye",
      "last_name": "Barber",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Blair",
      "last_name": "Conwright",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Geor'Quarius",
      "last_name": "Spivey",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "D'Andre",
      "last_name": "Rogers",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Carter",
      "last_name": "Ware",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Dominic",
      "last_name": "DiNunzio",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Brent",
      "last_name": "Matiscik",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Max",
      "last_name": "Duggan",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Chandler",
      "last_name": "Morris",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Sam",
      "last_name": "Jackson",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Emari",
      "last_name": "Demercado",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Kendre",
      "last_name": "Miller",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Daimarqua",
      "last_name": "Foster",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "TCU",
      "team_name": "Horned Frogs",
      "first_name": "Nook",
      "last_name": "Bradford",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Xavier",
      "last_name": "Worthy",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Agiye",
      "last_name": "Hall",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Isaiah",
      "last_name": "Neyor",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Troy",
      "last_name": "Omeire",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Casey",
      "last_name": "Cain",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Jordan",
      "last_name": "Whittington",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Brenen",
      "last_name": "Thompson",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Ja'Tavion",
      "last_name": "Sanders",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Gunnar",
      "last_name": "Helm",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Jahleel",
      "last_name": "Billingsley",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Hudson",
      "last_name": "Card",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Quinn",
      "last_name": "Ewers",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Ben",
      "last_name": "Ballard",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Bijan",
      "last_name": "Robinson",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Roschon",
      "last_name": "Johnson",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Texas",
      "team_name": "Longhorns",
      "first_name": "Keilan",
      "last_name": "Robinson",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "J.J.",
      "last_name": "Sparkman",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Trey",
      "last_name": "Cleveland",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Brady",
      "last_name": "Boyd",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Loic",
      "last_name": "Fouonji",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Jerand",
      "last_name": "Bradley",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Nate",
      "last_name": "Floyd",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Myles",
      "last_name": "Price",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Xavier",
      "last_name": "White",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Chadarius",
      "last_name": "Townsend",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Baylor",
      "last_name": "Cupp",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Mason",
      "last_name": "Tharp",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Tyler",
      "last_name": "Shough",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Donovan",
      "last_name": "Smith",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Behren",
      "last_name": "Morton",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "SaRodorick",
      "last_name": "Thompson",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Tahj",
      "last_name": "Brooks",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Texas Tech",
      "team_name": "Red Raiders",
      "first_name": "Cam'Ron",
      "last_name": "Valdez",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Bryce",
      "last_name": "Ford-Wheaton",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Preston",
      "last_name": "Fox",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Jeremiah",
      "last_name": "Aaron",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Kaden",
      "last_name": "Prather",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Jarel",
      "last_name": "Williams",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Cortez",
      "last_name": "Braham",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Sam",
      "last_name": "James",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Reese",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Graeson",
      "last_name": "Malashevich",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Brian",
      "last_name": "Polendey",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Mike",
      "last_name": "O'Laughlin",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Victor",
      "last_name": "Wikstrom",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "JT",
      "last_name": "Daniels",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Garrett",
      "last_name": "Greene",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Will",
      "last_name": "Crowder",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Tony",
      "last_name": "Mathis Jr.",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Lyn-J",
      "last_name": "Dixon",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "West Virginia",
      "team_name": "Mountaineers",
      "first_name": "Justin",
      "last_name": "Johnson Jr.",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Victor",
      "last_name": "Tucker",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Elijah",
      "last_name": "Spencer",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Tre'",
      "last_name": "Goode",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Grant",
      "last_name": "DuBose",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Jairus",
      "last_name": "Mack",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Taylor",
      "last_name": "Thompson",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Jake",
      "last_name": "Clemons",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Bryce",
      "last_name": "Kennon",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Chris",
      "last_name": "Reynolds",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "James",
      "last_name": "Foster",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Xavier",
      "last_name": "Williams",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Shadrick",
      "last_name": "Byrd",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "Calvin",
      "last_name": "Camp",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Charlotte",
      "team_name": "49ers",
      "first_name": "ChaVon",
      "last_name": "McEachern",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Jahmal",
      "last_name": "Edrine",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Javion",
      "last_name": "Posey",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "William",
      "last_name": "Ford",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Je'Quan",
      "last_name": "Burton",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Jymetre",
      "last_name": "Hester",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "LaJohntay",
      "last_name": "Wester",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Tony",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Austin",
      "last_name": "Evans",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "N'Kosi",
      "last_name": "Perry",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Willie",
      "last_name": "Taggart Jr.",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Michael",
      "last_name": "Johnson Jr.",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Johnny",
      "last_name": "Ford",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Florida Atlantic",
      "team_name": "Owls",
      "first_name": "Marvin",
      "last_name": "Scott III",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Randall",
      "last_name": "St.Felix",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Artez",
      "last_name": "Hooker",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Kris",
      "last_name": "Mitchell",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Jordan",
      "last_name": "Underwood",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Rivaldo",
      "last_name": "Fairweather",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Jackson",
      "last_name": "McDonald",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Haden",
      "last_name": "Carlson",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Grayson",
      "last_name": "James",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Florida International",
      "team_name": "Panthers",
      "first_name": "Lexington",
      "last_name": "Joseph",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Tre",
      "last_name": "Harris",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Kyle",
      "last_name": "Maxwell",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Julien",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Praise",
      "last_name": "Okorie",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Smoke",
      "last_name": "Harris",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Tahj",
      "last_name": "Magee",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Solomon",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Griffin",
      "last_name": "Hebert",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Ivan",
      "last_name": "Thomas",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Carson",
      "last_name": "Rieder",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Greg",
      "last_name": "Garner",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Keyon",
      "last_name": "Henry-Brooks",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Louisiana Tech",
      "team_name": "Bulldogs",
      "first_name": "Harlan",
      "last_name": "Dixon",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Corey",
      "last_name": "Gammage",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Stone",
      "last_name": "Scarcelle",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Caleb",
      "last_name": "McMillan",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Shadeed",
      "last_name": "Ahmed",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Jayden",
      "last_name": "Harrison",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Bryan",
      "last_name": "Robinson",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Talik",
      "last_name": "Keaton",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "EJ",
      "last_name": "Horton",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Charles",
      "last_name": "Montgomery",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Devin",
      "last_name": "Miller",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Amir",
      "last_name": "Richardson",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Henry",
      "last_name": "Colombi",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Cam",
      "last_name": "Fancher",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Rasheen",
      "last_name": "Ali",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Khalan",
      "last_name": "Laborn",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Marshall",
      "team_name": "Thundering Herd",
      "first_name": "Ethan",
      "last_name": "Payne",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "Izaiah",
      "last_name": "Gathings",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "Jaylin",
      "last_name": "Lane",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "DJ",
      "last_name": "England-Chisolm",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "Yusuf",
      "last_name": "Ali",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "Chase",
      "last_name": "Cunningham",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "Nicholas",
      "last_name": "Vattiato",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Middle Tennessee",
      "team_name": "Blue Raiders",
      "first_name": "Frank",
      "last_name": "Peasant",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Jyaire",
      "last_name": "Shorter",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Bryson",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Zhighlil",
      "last_name": "McMillan",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Damon",
      "last_name": "Ward",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Detraveon",
      "last_name": "Brown",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Tommy",
      "last_name": "Bush",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Roderic",
      "last_name": "Burns",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Khatib",
      "last_name": "Lyles",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Jake",
      "last_name": "Roberts",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Asher",
      "last_name": "Alberding",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Var'Keyes",
      "last_name": "Gumms",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Austin",
      "last_name": "Aune",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Jace",
      "last_name": "Ruder",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Oscar",
      "last_name": "Adaway III",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Isaiah",
      "last_name": "Johnson",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "North Texas",
      "team_name": "Mean Green",
      "first_name": "Ikaika",
      "last_name": "Ragsdale",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Ali",
      "last_name": "Jennings III",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Noah",
      "last_name": "Robinson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Javon",
      "last_name": "Harvey",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Aaron",
      "last_name": "Moore",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Isiah",
      "last_name": "Paige",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Jordan",
      "last_name": "Bly",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Zack",
      "last_name": "Kuntz",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Donta",
      "last_name": "Anthony Jr.",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Avery",
      "last_name": "Ford",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Hayden",
      "last_name": "Wolff",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "D.J.",
      "last_name": "Mack Jr.",
      "position": "QB",
      "year": "SR/TR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Blake",
      "last_name": "Watson",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Elijah",
      "last_name": "Davis",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Old Dominion",
      "team_name": "Monarchs",
      "first_name": "Jon-Luke",
      "last_name": "Peaker",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Bradley",
      "last_name": "Rozner",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Bennett",
      "last_name": "Mecom",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Cedric",
      "last_name": "Patterson III",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Andrew",
      "last_name": "Mason",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Luke",
      "last_name": "McCaffrey",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Andrew",
      "last_name": "Mason",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Jack",
      "last_name": "Bradley",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Wiley",
      "last_name": "Green",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "TJ",
      "last_name": "McMahon",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Ari",
      "last_name": "Broussard",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Rice",
      "team_name": "Owls",
      "first_name": "Jerry",
      "last_name": "Johnson III",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Jason",
      "last_name": "Brownlee",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Zay",
      "last_name": "Franks",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Brandon",
      "last_name": "Hayes",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Jalen",
      "last_name": "May",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Jakarius",
      "last_name": "Caston",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Brad",
      "last_name": "Dennis",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Luke",
      "last_name": "Baker",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Trey",
      "last_name": "Lowe",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Ty",
      "last_name": "Keyes",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Jake",
      "last_name": "Lange",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Frank",
      "last_name": "Gore Jr.",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Dajon",
      "last_name": "Richard",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Cole",
      "last_name": "Cavallo",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Ray",
      "last_name": "Ladner",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Malik",
      "last_name": "Shorts",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Jay",
      "last_name": "Jones",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Southern Miss",
      "team_name": "Golden Eagles",
      "first_name": "Camron",
      "last_name": "Harrell",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Samario",
      "last_name": "Rudolph",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Fred",
      "last_name": "Farrier II",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Tejhaun",
      "last_name": "Palmer",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "T.J.",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Ryan",
      "last_name": "Davis",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Terrell",
      "last_name": "McDonald",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Bryce",
      "last_name": "Damous",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Dylan",
      "last_name": "Hopkins",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Bryson",
      "last_name": "Lucero",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Jermaine",
      "last_name": "Brown Jr.",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "DeWayne",
      "last_name": "McBride",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Keondre",
      "last_name": "Swoopes",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "UAB",
      "team_name": "Blazers",
      "first_name": "Damien",
      "last_name": "Miller",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Jostein",
      "last_name": "Clarke",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Jeremiah",
      "last_name": "Ballard",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Kelly",
      "last_name": "Akharaiyi",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Josh",
      "last_name": "Farr",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Tyrin",
      "last_name": "Smith",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Walter",
      "last_name": "Dawn Jr.",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Reynaldo",
      "last_name": "Flores",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Trent",
      "last_name": "Thompson",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Zach",
      "last_name": "Fryar",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Gavin",
      "last_name": "Hardison",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Calvin",
      "last_name": "Brownholtz",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Ronald",
      "last_name": "Awatt",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Deion",
      "last_name": "Hankins",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "Willie",
      "last_name": "Eldridge",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "UTEP",
      "team_name": "Miners",
      "first_name": "James",
      "last_name": "Tupou",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "De'Corian",
      "last_name": "Clark",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Tre'Von",
      "last_name": "Bradley",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Zakhari",
      "last_name": "Franklin",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Tykee",
      "last_name": "Ogle-Kellogg",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Joshua",
      "last_name": "Cephus",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Chris",
      "last_name": "Carpenter",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Oscar",
      "last_name": "Cardenas",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Gavin",
      "last_name": "Sharp",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Dan",
      "last_name": "Dishman",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Frank",
      "last_name": "Harris",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Eddie",
      "last_name": "Marburger",
      "position": "QB",
      "year": "Lee FR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Brenden",
      "last_name": "Brady",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Tye",
      "last_name": "Edwards",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "UTSA",
      "team_name": "Roadrunners",
      "first_name": "Kevorian",
      "last_name": "Barnes",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Jaylen",
      "last_name": "Hall",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Craig",
      "last_name": "Burt Jr.",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Daewood",
      "last_name": "Davis",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Dakota",
      "last_name": "Thomas",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Josh",
      "last_name": "Sterns",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Malachi",
      "last_name": "Corley",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Dalvin",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Joshua",
      "last_name": "Simon",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Joey",
      "last_name": "Beljan",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Jarret",
      "last_name": "Doege",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Chance",
      "last_name": "McDonald",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Kye",
      "last_name": "Robichaux",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Western Kentucky",
      "team_name": "Hilltoppers",
      "first_name": "Jakairi",
      "last_name": "Moses",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Isaiah",
      "last_name": "Alston",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Ryan",
      "last_name": "Jackovic",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Veshe",
      "last_name": "Daniyan",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Joshua",
      "last_name": "Lingenfelter",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Tyhier",
      "last_name": "Tyler",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Cade",
      "last_name": "Ballard",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Jemel",
      "last_name": "Jones",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Jakobi",
      "last_name": "Buchanan",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Tyson",
      "last_name": "Riley",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Army",
      "team_name": "Black Knights",
      "first_name": "Markel",
      "last_name": "Johnson",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Gunner",
      "last_name": "Romney",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Brayden",
      "last_name": "Cosper",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Talmage",
      "last_name": "Gunther",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Keanu",
      "last_name": "Hill",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Kody",
      "last_name": "Epps",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Maguire",
      "last_name": "Anderson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Puka",
      "last_name": "Nacua",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Chase",
      "last_name": "Roberts",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Hobbs",
      "last_name": "Nyberg",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Isaac",
      "last_name": "Rex",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Dallin",
      "last_name": "Holker",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Ethan",
      "last_name": "Erickson",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Jaren",
      "last_name": "Hall",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Jacob",
      "last_name": "Conover",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Cade",
      "last_name": "Fennegan",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Christopher",
      "last_name": "Brooks",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Lopini",
      "last_name": "Katoa",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Jackson",
      "last_name": "McChesney",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Masen",
      "last_name": "Wake",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "BYU",
      "team_name": "Cougars",
      "first_name": "Houston",
      "last_name": "Heimuli",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Keelan",
      "last_name": "Marion",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Matt",
      "last_name": "Drayton",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Jacob",
      "last_name": "Flynn",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Kevens",
      "last_name": "Clercius",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Nigel",
      "last_name": "Fitzgerald",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Elijah",
      "last_name": "Jeffreys",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Cameron",
      "last_name": "Ross",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Aaron",
      "last_name": "Turner",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Darius",
      "last_name": "Bush",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Brandon",
      "last_name": "Niemenski",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Bo",
      "last_name": "Estes",
      "position": "TE",
      "year": "SO/TR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Christopher",
      "last_name": "Johnson",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Ta'Quan",
      "last_name": "Roberson",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Tyler",
      "last_name": "Phommachanh",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Nathan",
      "last_name": "Carter",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Will",
      "last_name": "Knight",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Connecticut",
      "team_name": "Huskies",
      "first_name": "Brian",
      "last_name": "Brewton",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "CJ",
      "last_name": "Yarbrough",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Treon",
      "last_name": "Sibley",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Brody",
      "last_name": "Brumm",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Caleb",
      "last_name": "Snead",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Noah",
      "last_name": "Frith",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Demario",
      "last_name": "Douglas",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Jaivian",
      "last_name": "Lofton",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Kylen",
      "last_name": "Austin",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Jerome",
      "last_name": "Jackson",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Austin",
      "last_name": "Henderson",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Charlie",
      "last_name": "Brewer",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Kaidon",
      "last_name": "Salter",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Johnathan",
      "last_name": "Bennett",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "T.J.",
      "last_name": "Green",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Dae",
      "last_name": "Hunter",
      "position": "RB",
      "year": "Dae SO/TR"
    },
    {
      "team_city": "Liberty",
      "team_name": "Flames",
      "first_name": "Shedro",
      "last_name": "Louis",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Rico",
      "last_name": "Arnold",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Onuma",
      "last_name": "Dieke",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Melvin",
      "last_name": "Hill",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Jermaine",
      "last_name": "Johnson Jr.",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Josiah",
      "last_name": "Johnson",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Jaret",
      "last_name": "Pallotta",
      "position": "TE",
      "year": "GR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Jacob",
      "last_name": "Orlando",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Brady",
      "last_name": "Olson",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Zamar",
      "last_name": "Wise",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Garrett",
      "last_name": "Dzuro",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Ellis",
      "last_name": "Merriweather",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Kay'Ron",
      "last_name": "Adams",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Massachusetts",
      "team_name": "Minutemen",
      "first_name": "Carter",
      "last_name": "Scudo",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Justice",
      "last_name": "Powers",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Cole",
      "last_name": "Harrity",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Dominic",
      "last_name": "Gicinto",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Thomaz",
      "last_name": "Whitford",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Weston",
      "last_name": "Eget",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Dino",
      "last_name": "Maldonado",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "O'Maury",
      "last_name": "Samuels",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "New Mexico State",
      "team_name": "Aggies",
      "first_name": "Alex",
      "last_name": "Escobar",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Lorenzo",
      "last_name": "Styles",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Braden",
      "last_name": "Lenzy",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Conor",
      "last_name": "Ratigan",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Joe",
      "last_name": "Wilkins Jr.",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Deion",
      "last_name": "Colzie",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Tobias",
      "last_name": "Merriweather",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Avery",
      "last_name": "Davis",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Jayden",
      "last_name": "Thomas",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Matt",
      "last_name": "Salerno",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Michael",
      "last_name": "Mayer",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Mitchell",
      "last_name": "Evans",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Kevin",
      "last_name": "Bauman",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Tyler",
      "last_name": "Buchner",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Drew",
      "last_name": "Pyne",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Steve",
      "last_name": "Angeli",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Chris",
      "last_name": "Tyree",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Logan",
      "last_name": "Diggs",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Notre Dame",
      "team_name": "Fighting Irish",
      "first_name": "Audric",
      "last_name": "Estime",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Shocky",
      "last_name": "Jacques-Louis",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Bryce",
      "last_name": "Profitt",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Oran",
      "last_name": "Singleton Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Jasaiah",
      "last_name": "Gathings",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Tony",
      "last_name": "Grimes Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Alex",
      "last_name": "Adams",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Tristian",
      "last_name": "Brank",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Nik",
      "last_name": "Ognenovic",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Brycen",
      "last_name": "Yarmo",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "DJ",
      "last_name": "Irons",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Joey",
      "last_name": "Marousek",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Ryan",
      "last_name": "Jankowski",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Cam",
      "last_name": "Wiley",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Jonzell",
      "last_name": "Norrils",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Akron",
      "team_name": "Zips",
      "first_name": "Anthony",
      "last_name": "Williams Jr.",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "Yo'Heinz",
      "last_name": "Tyler",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "Jayshon",
      "last_name": "Jackson",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "Derin",
      "last_name": "McCulley",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "Ryan",
      "last_name": "Lezon",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "John",
      "last_name": "Paddock",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "Will",
      "last_name": "Jones",
      "position": "RB",
      "year": "GR"
    },
    {
      "team_city": "Ball State",
      "team_name": "Cardinals",
      "first_name": "Carson",
      "last_name": "Steele",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Tyrone",
      "last_name": "Broden",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Cavon",
      "last_name": "Croom",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Austin",
      "last_name": "Osborne",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Jhaylin",
      "last_name": "Embry",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Christian",
      "last_name": "Sims",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Griffin",
      "last_name": "Little",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Andrew",
      "last_name": "Bench",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Levi",
      "last_name": "Gazarek",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Matt",
      "last_name": "McDonald",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Tucker",
      "last_name": "Melton",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Terion",
      "last_name": "Stewart",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Bowling Green",
      "team_name": "Falcons",
      "first_name": "Jaison",
      "last_name": "Patterson",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Quian",
      "last_name": "Williams",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Jovany",
      "last_name": "Ruiz-Navarro",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Khamran",
      "last_name": "Laborn",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Jamari",
      "last_name": "Gassett",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Matt",
      "last_name": "Myers",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Casey",
      "last_name": "Case",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Buffalo",
      "team_name": "Bulls",
      "first_name": "Ron",
      "last_name": "Cook Jr.",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Alec",
      "last_name": "Ward",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Dallas",
      "last_name": "Dixon",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Joel",
      "last_name": "Wilson",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Daniel",
      "last_name": "Richardson",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Tyler",
      "last_name": "Pape",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Kobe",
      "last_name": "Lewis",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Central Michigan",
      "team_name": "Chippewas",
      "first_name": "Lew",
      "last_name": "Nichols III",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Tanner",
      "last_name": "Knue",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Zach",
      "last_name": "Westmoreland",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Dylan",
      "last_name": "Drummond",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Dennis",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Hassan",
      "last_name": "Beydoun",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "I'Shawn",
      "last_name": "Stewart",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Gunnar",
      "last_name": "Oakes",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Austin",
      "last_name": "Smith",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Darius",
      "last_name": "Boone Jr.",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Samson",
      "last_name": "Evans",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Eastern Michigan",
      "team_name": "Eagles",
      "first_name": "Bryson",
      "last_name": "Moss",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Dante",
      "last_name": "Cephas",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Devontez",
      "last_name": "Walker",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Ja'Shaun",
      "last_name": "Poke",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Luke",
      "last_name": "Floriea",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Raymond",
      "last_name": "James",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Kris",
      "last_name": "Leach",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Keenan",
      "last_name": "Orr",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Collin",
      "last_name": "Schlee",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Marquez",
      "last_name": "Cooper",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Xavier",
      "last_name": "Williams",
      "position": "RB",
      "year": "GR"
    },
    {
      "team_city": "Kent State",
      "team_name": "Golden Flashes",
      "first_name": "Bryan",
      "last_name": "Bradford",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Mac",
      "last_name": "Hippenhammer",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Nate",
      "last_name": "Muersch",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Jalen",
      "last_name": "Walker",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Kevin",
      "last_name": "Davis",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Devon",
      "last_name": "Dorsey",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Jack",
      "last_name": "Coldiron",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Brett",
      "last_name": "Gabbert",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Keyon",
      "last_name": "Mozee",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Miami (Ohio)",
      "team_name": "RedHawks",
      "first_name": "Jaylon",
      "last_name": "Bester",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Cole",
      "last_name": "Tucker",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Messiah",
      "last_name": "Travis",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Trayvon",
      "last_name": "Rudolph",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Fabian",
      "last_name": "McCray",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Mohamed",
      "last_name": "Toure",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Billy",
      "last_name": "Dozier",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Miles",
      "last_name": "Joiner",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Liam",
      "last_name": "Soraghan",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Tristen",
      "last_name": "Tewes",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Rocky",
      "last_name": "Lombardi",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Ethan",
      "last_name": "Hampton",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Harrison",
      "last_name": "Waylee",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Antario",
      "last_name": "Brown",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Mason",
      "last_name": "Blakemore",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Northern Illinois",
      "team_name": "Huskies",
      "first_name": "Brock",
      "last_name": "Lampe",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Ohio",
      "team_name": "Bobcats",
      "first_name": "James",
      "last_name": "Bostic",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Ohio",
      "team_name": "Bobcats",
      "first_name": "Tyler",
      "last_name": "Walton",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Ohio",
      "team_name": "Bobcats",
      "first_name": "Miles",
      "last_name": "Cross",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Ohio",
      "team_name": "Bobcats",
      "first_name": "Kurtis",
      "last_name": "Rourke",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Ohio",
      "team_name": "Bobcats",
      "first_name": "O'Shaan",
      "last_name": "Allison",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Jerjuan",
      "last_name": "Newton",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Devin",
      "last_name": "Maddox",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "DeMeer",
      "last_name": "Blankumsee",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Jamal",
      "last_name": "Turner",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Nick",
      "last_name": "Rosi",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Dequan",
      "last_name": "Finn",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Tucker",
      "last_name": "Gleason",
      "position": "QB",
      "year": "SO/TR"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Micah",
      "last_name": "Kelly",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Toledo",
      "team_name": "Rockets",
      "first_name": "Jacquez",
      "last_name": "Stuart",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Anthony",
      "last_name": "Sambucci",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Tyren",
      "last_name": "Mason",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Corey",
      "last_name": "Crooms",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Henry",
      "last_name": "Wilson Jr.",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Kaevion",
      "last_name": "Mack",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Austin",
      "last_name": "Hence",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Mitch",
      "last_name": "Bartol",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Jack",
      "last_name": "Salopek",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Stone",
      "last_name": "Hollenbach",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Mareyohn",
      "last_name": "Hrabowski",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "Sean",
      "last_name": "Tyler",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Western Michigan",
      "team_name": "Broncos",
      "first_name": "La'Darius",
      "last_name": "Jefferson",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "David",
      "last_name": "Cormier",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Jake",
      "last_name": "Spiewak",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Amari",
      "last_name": "Terry",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Micah",
      "last_name": "Davis",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Dane",
      "last_name": "Kinamon",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Ben",
      "last_name": "Jefferson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Kyle",
      "last_name": "Patterson",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Dalton",
      "last_name": "King",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Caden",
      "last_name": "Blum",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Haaziq",
      "last_name": "Daniels",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Warren",
      "last_name": "Bryan",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Zachary",
      "last_name": "Larrier",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "DeAndre",
      "last_name": "Hughes",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Jorden",
      "last_name": "Gidrey",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Brad",
      "last_name": "Roberts",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Omar",
      "last_name": "Fattah",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Air Force",
      "team_name": "Falcons",
      "first_name": "Emmanuel",
      "last_name": "Michel",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Billy",
      "last_name": "Bowens",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Eric",
      "last_name": "McAlister",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Shea",
      "last_name": "Whiting",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Stefan",
      "last_name": "Cobbs",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Austin",
      "last_name": "Bolt",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Kaden",
      "last_name": "Dudley",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Davis",
      "last_name": "Koetter",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Latrell",
      "last_name": "Caples",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Zamondre",
      "last_name": "Merriweather",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Riley",
      "last_name": "Smith",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Tyneil",
      "last_name": "Hopper",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Kurt",
      "last_name": "Rafdal",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Hank",
      "last_name": "Bachmeier",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Sam",
      "last_name": "Vidlak",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Taylen",
      "last_name": "Green",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "George",
      "last_name": "Holani",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Tyler",
      "last_name": "Crowe",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Boise State",
      "team_name": "Broncos",
      "first_name": "Taequan",
      "last_name": "Tyler",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Tory",
      "last_name": "Horton",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Justice",
      "last_name": "McCoy",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Ty",
      "last_name": "McCullouch",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "E.J.",
      "last_name": "Scott",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Melquan",
      "last_name": "Stovall",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Dante",
      "last_name": "Wright",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Thomas",
      "last_name": "Pannunzio",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Tanner",
      "last_name": "Arkin",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Gary",
      "last_name": "Williams",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Damir",
      "last_name": "Abdullah",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Clay",
      "last_name": "Millen",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Giles",
      "last_name": "Pooler",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Brayden",
      "last_name": "Fowler-Nicolosi",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "A'Jon",
      "last_name": "Vivens",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "Avery",
      "last_name": "Morrow",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Colorado State",
      "team_name": "Rams",
      "first_name": "David",
      "last_name": "Bailey",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Ty",
      "last_name": "Jones",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Josh",
      "last_name": "Kelly",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Zane",
      "last_name": "Pope",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Jalen",
      "last_name": "Cropper",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Erik",
      "last_name": "Brooks",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Raymond",
      "last_name": "Pauwels Jr.",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Jake",
      "last_name": "Haener",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Logan",
      "last_name": "Fife",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Fresno State",
      "team_name": "Bulldogs",
      "first_name": "Jordan",
      "last_name": "Mims",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Jonah",
      "last_name": "Panoke",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Zion",
      "last_name": "Bowens",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Koali",
      "last_name": "Nishigaya",
      "position": "WR/RB",
      "year": "RS SO"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Caleb",
      "last_name": "Phillips",
      "position": "TE",
      "year": "GR/TR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Steven",
      "last_name": "Fiso",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Kamuela",
      "last_name": "Borden",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Brayden",
      "last_name": "Schager",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Dedrick",
      "last_name": "Parson",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Hawaii",
      "team_name": "Rainbow Warriors",
      "first_name": "Calvin",
      "last_name": "Turner Jr.",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "B.J.",
      "last_name": "Casteel",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Victor",
      "last_name": "Snow",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Tyrese",
      "last_name": "Mack",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Dazure",
      "last_name": "Paggett",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Jamaal",
      "last_name": "Bell",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Marquis",
      "last_name": "Ashley",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Cooper",
      "last_name": "Shults",
      "position": "TE",
      "year": "SO/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Carlton",
      "last_name": "Brown III",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Nate",
      "last_name": "Cox",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Shane",
      "last_name": "Illingworth",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Toa",
      "last_name": "Taua",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Nevada",
      "team_name": "Wolf Pack",
      "first_name": "Devonte",
      "last_name": "Lee",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Jace",
      "last_name": "Taylor",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Andrew",
      "last_name": "Erickson",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Zarak",
      "last_name": "Scruggs Jr.",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Keyonta",
      "last_name": "Lanier",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Elijah",
      "last_name": "Queen",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Luke",
      "last_name": "Wysong",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Austin",
      "last_name": "Erickson",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Trace",
      "last_name": "Bruckler",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Connor",
      "last_name": "Witthoft",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Isaiah",
      "last_name": "Chavez",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Connor",
      "last_name": "Genal",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Nathaniel",
      "last_name": "Jones",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Peyton",
      "last_name": "Dixon",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "New Mexico",
      "team_name": "Lobos",
      "first_name": "Bobby",
      "last_name": "Wooden",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Tyrell",
      "last_name": "Shavers",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Brionne",
      "last_name": "Penny",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Ronald",
      "last_name": "Gilliam",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Jesse",
      "last_name": "Matthews",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Mekhi",
      "last_name": "Shaw",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Phillippe",
      "last_name": "Wesley II",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "TJ",
      "last_name": "Sullivan",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Darius",
      "last_name": "De Los Reyes",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Josh",
      "last_name": "Nicholson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Mark",
      "last_name": "Redman",
      "position": "TE",
      "year": "JR/TR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Aaron",
      "last_name": "Greene",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "JP",
      "last_name": "Murphy",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Jay",
      "last_name": "Rudolph",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Gus",
      "last_name": "McGee",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Cameron",
      "last_name": "Harpole",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Braxton",
      "last_name": "Burmeister",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Will",
      "last_name": "Haskell",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Kyle",
      "last_name": "Crum",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Chance",
      "last_name": "Bell",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Jordan",
      "last_name": "Byrd",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "San Diego State",
      "team_name": "Aztecs",
      "first_name": "Jaylon",
      "last_name": "Armstead",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Isaiah",
      "last_name": "Hamilton",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Charles",
      "last_name": "Ross",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Jermaine",
      "last_name": "Braddock",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Malikhi",
      "last_name": "Miller",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Elijah",
      "last_name": "Cooks",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Justin",
      "last_name": "Lockhart",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Dominick",
      "last_name": "Mazotti",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Sam",
      "last_name": "Olson",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Jackson",
      "last_name": "Canaan",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Chevan",
      "last_name": "Cordeiro",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Nick",
      "last_name": "Nash",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Kairee",
      "last_name": "Robinson",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Shamar",
      "last_name": "Garrett",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "San Jose State",
      "team_name": "Spartans",
      "first_name": "Kenyon",
      "last_name": "Sims",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Kilinahe",
      "last_name": "Mendiola-Jensen",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Marcus",
      "last_name": "Phillips Jr.",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Zyell",
      "last_name": "Griffin",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Kyle",
      "last_name": "Williams",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Jordan",
      "last_name": "Jakes",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Kaleo",
      "last_name": "Ballungay",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Shaun",
      "last_name": "Grayson",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Harrison",
      "last_name": "Bailey",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Cameron",
      "last_name": "Friel",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Chad",
      "last_name": "Magyar",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Courtney",
      "last_name": "Reese",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "UNLV",
      "team_name": "Rebels",
      "first_name": "Jayvaun",
      "last_name": "Wilson",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Justin",
      "last_name": "McGriff",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Jamie",
      "last_name": "Nance",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Xavier",
      "last_name": "Williams",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Brian",
      "last_name": "Cobbs",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Otto",
      "last_name": "Tia",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Ryder",
      "last_name": "MacGillivray",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Kyle",
      "last_name": "Van Leeuwen",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Franky",
      "last_name": "Jacobsen",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Garrett",
      "last_name": "Walchli",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "NyNy",
      "last_name": "Davis",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Terrell",
      "last_name": "Vaughn",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Taylor",
      "last_name": "Larsen",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Josh",
      "last_name": "Sterzer",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Parker",
      "last_name": "Buchanan",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Cade",
      "last_name": "Jensen",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Logan",
      "last_name": "Bonner",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Cooper",
      "last_name": "Legas",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Levi",
      "last_name": "Williams",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Calvin",
      "last_name": "Tyler Jr.",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "John",
      "last_name": "Gentry",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Utah State",
      "team_name": "Aggies",
      "first_name": "Pailate",
      "last_name": "Makakona",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Gunner",
      "last_name": "Gentry",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Wyatt",
      "last_name": "Wieland",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Ryan",
      "last_name": "Marquez",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Joshua",
      "last_name": "Cobbs",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Caleb",
      "last_name": "Cooley",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Alex",
      "last_name": "Brown",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Treyton",
      "last_name": "Welch",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Colin",
      "last_name": "O'Brien",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Jackson",
      "last_name": "Marcotte",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Andrew",
      "last_name": "Peasley",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Hank",
      "last_name": "Gibbs",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Gavin",
      "last_name": "Beerup",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Titus",
      "last_name": "Swen",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Dawaiian",
      "last_name": "McNeely",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "D.Q.",
      "last_name": "James",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Parker",
      "last_name": "Christensen",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Wyoming",
      "team_name": "Cowboys",
      "first_name": "Caleb",
      "last_name": "Driskill",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Dorian",
      "last_name": "Singer",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Kevin",
      "last_name": "Green Jr.",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Tetairoa",
      "last_name": "McMillan",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Ma'jon",
      "last_name": "Wright",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "AJ",
      "last_name": "Jones",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Jacob",
      "last_name": "Cowing",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Anthony",
      "last_name": "Simpson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Alex",
      "last_name": "Lines",
      "position": "TE",
      "year": "SO/TR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Tanner",
      "last_name": "McLachlan",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Keyan",
      "last_name": "Burnett",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Roberto",
      "last_name": "Miranda",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Jayden",
      "last_name": "de Laura",
      "position": "QB",
      "year": "SO/TR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Jordan",
      "last_name": "McCloud",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Noah",
      "last_name": "Fifita",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Michael",
      "last_name": "Wiley",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Jonah",
      "last_name": "Coleman",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Rayshon",
      "last_name": "Luke",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Arizona",
      "team_name": "Wildcats",
      "first_name": "Issaiah",
      "last_name": "Johnson",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Andre",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Chad",
      "last_name": "Johnson Jr.",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Bryan",
      "last_name": "Thompson",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Elijhah",
      "last_name": "Badger",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Cam",
      "last_name": "Johnson",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Giovanni",
      "last_name": "Sanders",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Jalin",
      "last_name": "Conyers",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Bryce",
      "last_name": "Pierre",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Messiah",
      "last_name": "Swinson",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Jacob",
      "last_name": "Newell",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Emory",
      "last_name": "Jones",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Paul",
      "last_name": "Tyson",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Trenton",
      "last_name": "Bourguet",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Xazavian",
      "last_name": "Valladay",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Daniyel",
      "last_name": "Ngata",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Tevin",
      "last_name": "White",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Case",
      "last_name": "Hatch",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Merlin",
      "last_name": "Robertson",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Arizona State",
      "team_name": "Sun Devils",
      "first_name": "Connor",
      "last_name": "Soelle",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Jeremiah",
      "last_name": "Hunter",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Monroe",
      "last_name": "Young",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "J.Michael",
      "last_name": "Sturdivant",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Justin",
      "last_name": "Baker",
      "position": "WR",
      "year": "Richard JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Aidan",
      "last_name": "Lee",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Mavin",
      "last_name": "Anderson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Mason",
      "last_name": "Starling",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Tommy",
      "last_name": "Christakos",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Keleki",
      "last_name": "Latu",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Jermaine",
      "last_name": "Terry II",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Nick",
      "last_name": "Alftin",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Jack",
      "last_name": "Plummer",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Kai",
      "last_name": "Millner",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Zach",
      "last_name": "Johnson",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Damien",
      "last_name": "Moore",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "DeCarlos",
      "last_name": "Brooks",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Jaydn",
      "last_name": "Ott",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Beaux",
      "last_name": "Tagaloa",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Andy",
      "last_name": "Alfieri",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "California",
      "team_name": "Golden Bears",
      "first_name": "Champion",
      "last_name": "Johnson",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "R.J.",
      "last_name": "Sneed II",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Daniel",
      "last_name": "Arias",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Maurice",
      "last_name": "Bell",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Montana",
      "last_name": "Lemonious-Craig",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Ty",
      "last_name": "Robinson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Jordyn",
      "last_name": "Tyson",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Chase",
      "last_name": "Penry",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Jaylon",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Brady",
      "last_name": "Russell",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Caleb",
      "last_name": "Fauria",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Austin",
      "last_name": "Smith",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "J.T.",
      "last_name": "Shrout",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Brendon",
      "last_name": "Lewis",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Maddox",
      "last_name": "Kopp",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Ramon",
      "last_name": "Jefferson",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Alex",
      "last_name": "Fontenot",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Colorado",
      "team_name": "Buffaloes",
      "first_name": "Deion",
      "last_name": "Smith",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Troy",
      "last_name": "Franklin",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Isaah",
      "last_name": "Crocker",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Isaiah",
      "last_name": "Brevard",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Dont'e",
      "last_name": "Thornton",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Chase",
      "last_name": "Cota",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Josh",
      "last_name": "Delgado",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Seven",
      "last_name": "McGee",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Kris",
      "last_name": "Hutson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Justius",
      "last_name": "Lowe",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Cam",
      "last_name": "McCormick",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Spencer",
      "last_name": "Webb",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Moliki",
      "last_name": "Matavao",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Bo",
      "last_name": "Nix",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Ty",
      "last_name": "Thompson",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Jay",
      "last_name": "Butterfield",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Byron",
      "last_name": "Cardwell",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Sean",
      "last_name": "Dollars",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Oregon",
      "team_name": "Ducks",
      "first_name": "Noah",
      "last_name": "Whittington",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Tre'Shaun",
      "last_name": "Harrison",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "John",
      "last_name": "Dunmore",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Makiya",
      "last_name": "Tongue",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Tyjon",
      "last_name": "Lindsey",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Jesiah",
      "last_name": "Irish",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Anthony",
      "last_name": "Gould",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Silas",
      "last_name": "Bolden",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Luke",
      "last_name": "Musgrave",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Jake",
      "last_name": "Overman",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Bryce",
      "last_name": "Caufield",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Chance",
      "last_name": "Nolan",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Tristan",
      "last_name": "Gebbia",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Ben",
      "last_name": "Gulbranson",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Damien",
      "last_name": "Martinez",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Deshaun",
      "last_name": "Fenwick",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Oregon State",
      "team_name": "Beavers",
      "first_name": "Trey",
      "last_name": "Lowe",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Michael",
      "last_name": "Wilson",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Bryce",
      "last_name": "Farrell",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Jayson",
      "last_name": "Raines",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Brycen",
      "last_name": "Tremayne",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "John",
      "last_name": "Humphreys",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Elijah",
      "last_name": "Higgins",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Silas",
      "last_name": "Starr",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Benjamin",
      "last_name": "Yurosek",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Sam",
      "last_name": "Roush",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Bradley",
      "last_name": "Archer",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Tanner",
      "last_name": "McKee",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Ari",
      "last_name": "Patu",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "E.J.",
      "last_name": "Smith",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Casey",
      "last_name": "Filkins",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Stanford",
      "team_name": "Cardinal",
      "first_name": "Jay",
      "last_name": "Symonds",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Jake",
      "last_name": "Bobo",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Jadyn",
      "last_name": "Marshall",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Matt",
      "last_name": "Sykes",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Kam",
      "last_name": "Brown",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Titus",
      "last_name": "Mokiao-Atimalala",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "DJ",
      "last_name": "Justice",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Kazmeir",
      "last_name": "Allen",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Logan",
      "last_name": "Loya",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Josiah",
      "last_name": "Norwood",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Michael",
      "last_name": "Ezeike",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Mike",
      "last_name": "Martinez",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Carsen",
      "last_name": "Ryan",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Dorian",
      "last_name": "Thompson-Robinson",
      "position": "QB",
      "year": "SR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Ethan",
      "last_name": "Garbers",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Chase",
      "last_name": "Artopoeus",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Zach",
      "last_name": "Charbonnet",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Keegan",
      "last_name": "Jones",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "UCLA",
      "team_name": "Bruins",
      "first_name": "Christian",
      "last_name": "Grubb",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Terrell",
      "last_name": "Bynum",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Kyle",
      "last_name": "Ford",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Kyron",
      "last_name": "Hudson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Tahj",
      "last_name": "Washington",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Mario",
      "last_name": "Williams",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Brenden",
      "last_name": "Rice",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Gary",
      "last_name": "Bryant Jr.",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "John",
      "last_name": "Jackson III",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "CJ",
      "last_name": "Williams",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Malcolm",
      "last_name": "Epps",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Jude",
      "last_name": "Wolfe",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Lake",
      "last_name": "McRee",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Caleb",
      "last_name": "Williams",
      "position": "QB",
      "year": "SO/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Miller",
      "last_name": "Moss",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Travis",
      "last_name": "Dye",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Darwin",
      "last_name": "Barlow",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "USC",
      "team_name": "Trojans",
      "first_name": "Austin",
      "last_name": "Jones",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Devaughn",
      "last_name": "Vele",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Solomon",
      "last_name": "Enis",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Money",
      "last_name": "Parks",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Dalton",
      "last_name": "Kincaid",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Brant",
      "last_name": "Kuithe",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Thomas",
      "last_name": "Yassmin",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Cameron",
      "last_name": "Rising",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Ja'Quinden",
      "last_name": "Jackson",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Bryson",
      "last_name": "Barnes",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Tavion",
      "last_name": "Thomas",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Micah",
      "last_name": "Bernard",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Utah",
      "team_name": "Utes",
      "first_name": "Jaylon",
      "last_name": "Glover",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Ja'Lynn",
      "last_name": "Polk",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Giles",
      "last_name": "Jackson",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Jabez",
      "last_name": "Tinae",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Rome",
      "last_name": "Odunze",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Lonyatta",
      "last_name": "Alexander Jr.",
      "position": "WR",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Denzel",
      "last_name": "Boston",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Jalen",
      "last_name": "McMillan",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Taj",
      "last_name": "Davis",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Devin",
      "last_name": "Culp",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Jack",
      "last_name": "Westover",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Quentin",
      "last_name": "Moore",
      "position": "TE",
      "year": "JR/TR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Michael",
      "last_name": "Penix Jr.",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Dylan",
      "last_name": "Morris",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Sam",
      "last_name": "Huard",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Aaron",
      "last_name": "Dumas",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Cameron",
      "last_name": "Davis",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Washington",
      "team_name": "Huskies",
      "first_name": "Richard",
      "last_name": "Newton",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "De'Zhaun",
      "last_name": "Stribling",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Mitchell",
      "last_name": "Quinn",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Donovan",
      "last_name": "Ollie",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "CJ",
      "last_name": "Moore",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Tsion",
      "last_name": "Nunnally",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Lincoln",
      "last_name": "Victor",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Orion",
      "last_name": "Peters",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Renard",
      "last_name": "Bell",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Andre",
      "last_name": "Dollar",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Billy",
      "last_name": "Riviere",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Cameron",
      "last_name": "Ward",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Victor",
      "last_name": "Gabalis",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Xavier",
      "last_name": "Ward",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Nakia",
      "last_name": "Watson",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Jouvensly",
      "last_name": "Bazil",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Washington State",
      "team_name": "Cougars",
      "first_name": "Djouvensky",
      "last_name": "Schlenbaker",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Jermaine",
      "last_name": "Burton",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Christian",
      "last_name": "Leary",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Aaron",
      "last_name": "Anderson",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Ja'Corey",
      "last_name": "Brooks",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Traeshon",
      "last_name": "Holden",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Thaiu",
      "last_name": "Jones-Bell",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "JoJo",
      "last_name": "Earle",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Tyler",
      "last_name": "Harrell",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Kendrick",
      "last_name": "Law",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Cameron",
      "last_name": "Latu",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Robbie",
      "last_name": "Ouzts",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Amari",
      "last_name": "Niblack",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Bryce",
      "last_name": "Young",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Jalen",
      "last_name": "Milroe",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Ty",
      "last_name": "Simpson",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Jahmyr",
      "last_name": "Gibbs",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Jase",
      "last_name": "McClellan",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Trey",
      "last_name": "Sanders",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Brian",
      "last_name": "Branch",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Malachi",
      "last_name": "Moore",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Alabama",
      "team_name": "Crimson Tide",
      "first_name": "Jake",
      "last_name": "Pope",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Warren",
      "last_name": "Thompson",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Bryce",
      "last_name": "Stephens",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Quincey",
      "last_name": "McAdoo",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Ketron",
      "last_name": "Jackson Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Isaiah",
      "last_name": "Sategna",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Jaedon",
      "last_name": "Wilson",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Jadon",
      "last_name": "Haselwood",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Jaquayln",
      "last_name": "Crawford",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Hudson",
      "last_name": "Henry",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Trey",
      "last_name": "Knox",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Erin",
      "last_name": "Outley",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "KJ",
      "last_name": "Jefferson",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Malik",
      "last_name": "Hornsby",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Raheim",
      "last_name": "Sanders",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "Dominique",
      "last_name": "Johnson",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Arkansas",
      "team_name": "Razorbacks",
      "first_name": "AJ",
      "last_name": "Green",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Shedrick",
      "last_name": "Jackson",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Ze'Vian",
      "last_name": "Capers",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Landen",
      "last_name": "King",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Malcolm",
      "last_name": "Johnson Jr.",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Jay",
      "last_name": "Fair",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Tommy",
      "last_name": "Nesmith",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Ja'Varrius",
      "last_name": "Johnson",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Tar'Varish",
      "last_name": "Dawson Jr.",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Jackson",
      "last_name": "Billings",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Landen",
      "last_name": "King",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Luke",
      "last_name": "Deal",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "John",
      "last_name": "Shenker",
      "position": "TE",
      "year": "Samuel SR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Tyler",
      "last_name": "Fromm",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Brandon",
      "last_name": "Frazier",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "T.J.",
      "last_name": "Finley",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Zach",
      "last_name": "Calzada",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Robby",
      "last_name": "Ashford",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Tank",
      "last_name": "Bigsby",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Jarquez",
      "last_name": "Hunter",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Auburn",
      "team_name": "Tigers",
      "first_name": "Sean",
      "last_name": "Jackson",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Justin",
      "last_name": "Shorter",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Ja'Quavion",
      "last_name": "Fraziars",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Marcus",
      "last_name": "Burke",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Xzavier",
      "last_name": "Henderson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Ja'Markis",
      "last_name": "Weston",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Fenley",
      "last_name": "Graham Jr.",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Trent",
      "last_name": "Whittemore",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Daejon",
      "last_name": "Reynolds",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Kahleil",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Keon",
      "last_name": "Zipperer",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Dante",
      "last_name": "Zanders",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Nick",
      "last_name": "Elksnis",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Anthony",
      "last_name": "Richardson",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Jack",
      "last_name": "Miller III",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Jalen",
      "last_name": "Kitna",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Montrell",
      "last_name": "Johnson",
      "position": "RB",
      "year": "SO/TR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Nay'Quan",
      "last_name": "Wright",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Florida",
      "team_name": "Gators",
      "first_name": "Demarkcus",
      "last_name": "Bowman",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Adonai",
      "last_name": "Mitchell",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Marcus",
      "last_name": "Rosemy-Jacksaint",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Ladd",
      "last_name": "McConkey",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Arian",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Jackson",
      "last_name": "Meeks",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Kearis",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Dominick",
      "last_name": "Blaylock",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Brock",
      "last_name": "Bowers",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Arik",
      "last_name": "Gilbert",
      "position": "TE",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Oscar",
      "last_name": "Delp",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Darnell",
      "last_name": "Washington",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Brett",
      "last_name": "Seither",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Ryland",
      "last_name": "Goede",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Stetson",
      "last_name": "Bennett",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Carson",
      "last_name": "Beck",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Brock",
      "last_name": "Vandagriff",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Kenny",
      "last_name": "McIntosh",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Kendall",
      "last_name": "Milton",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Daijun",
      "last_name": "Edwards",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Tykee",
      "last_name": "Smith",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Georgia",
      "team_name": "Bulldogs",
      "first_name": "Javon",
      "last_name": "Bullard",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Javon",
      "last_name": "Baker",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Chris",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Dane",
      "last_name": "Key",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "DeMarcus",
      "last_name": "Harris",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Clevan",
      "last_name": "Thomas Jr.",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Dekel",
      "last_name": "Crowdus",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Tayvion",
      "last_name": "Robinson",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Rahsaan",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Chauncey",
      "last_name": "Magwood",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Brenden",
      "last_name": "Bates",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Jordan",
      "last_name": "Dingle",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Josh",
      "last_name": "Kattus",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Keaton",
      "last_name": "Upshaw",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Izayah",
      "last_name": "Cummings",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Will",
      "last_name": "Levis",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Beau",
      "last_name": "Allen",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Deuce",
      "last_name": "Hogan",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Chris",
      "last_name": "Rodriguez Jr.",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "JuTahn",
      "last_name": "McClain",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "La'Vell",
      "last_name": "Wright",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Kentucky",
      "team_name": "Wildcats",
      "first_name": "Justice",
      "last_name": "Dingle",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Kayshon",
      "last_name": "Boutte",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Jaray",
      "last_name": "Jenkins",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Kyren",
      "last_name": "Lacy",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Brian",
      "last_name": "Thomas Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Chris",
      "last_name": "Hilton Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Malik",
      "last_name": "Nabers",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Jack",
      "last_name": "Bech",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Jack",
      "last_name": "Mashburn",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Kole",
      "last_name": "Taylor",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Nick",
      "last_name": "Storz",
      "position": "TE",
      "year": "GR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Jayden",
      "last_name": "Daniels",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Myles",
      "last_name": "Brennan",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Garrett",
      "last_name": "Nussmeier",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "John",
      "last_name": "Emery Jr.",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Tre",
      "last_name": "Bradford",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "LSU",
      "team_name": "Tigers",
      "first_name": "Armoni",
      "last_name": "Goodwin",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Jonathan",
      "last_name": "Mingo",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Dannis",
      "last_name": "Jackson",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Jalen",
      "last_name": "Knox",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Malik",
      "last_name": "Heath",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Bralon",
      "last_name": "Brown",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Jordan",
      "last_name": "Watkins",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Jeremiah",
      "last_name": "Dillon",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Dayton",
      "last_name": "Wade",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Michael",
      "last_name": "Trigg",
      "position": "TE",
      "year": "SO/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Casey",
      "last_name": "Kelly",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Jaxson",
      "last_name": "Dart",
      "position": "QB",
      "year": "SO/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Luke",
      "last_name": "Altmyer",
      "position": "QB",
      "year": "SO"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Zach",
      "last_name": "Evans",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Ulysses",
      "last_name": "Bentley IV",
      "position": "RB",
      "year": "JR/TR"
    },
    {
      "team_city": "Mississippi",
      "team_name": "Rebels",
      "first_name": "Quinshon",
      "last_name": "Judkins",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Rara",
      "last_name": "Thomas",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Lideatrick",
      "last_name": "Griffin",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Justin",
      "last_name": "Robinson",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Antonio",
      "last_name": "Harmon",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Caleb",
      "last_name": "Ducking",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Jordan",
      "last_name": "Mosley",
      "position": "WR",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Jaden",
      "last_name": "Walley",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Scoobie",
      "last_name": "Ford",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Jamire",
      "last_name": "Calvin",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Austin",
      "last_name": "Williams",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Rufus",
      "last_name": "Harvey",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "William",
      "last_name": "Hardrick",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Will",
      "last_name": "Rogers",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Sawyer",
      "last_name": "Robertson",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Chance",
      "last_name": "Lovertich",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Jo'quavious",
      "last_name": "Marks",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Dillon",
      "last_name": "Johnson",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Mississippi State",
      "team_name": "Bulldogs",
      "first_name": "Ke'Travion",
      "last_name": "Hargrove",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Luther",
      "last_name": "Burden III",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Chance",
      "last_name": "Luper",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Ja'Marion",
      "last_name": "Wayne",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Tauskie",
      "last_name": "Dove",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Mekhi",
      "last_name": "Miller",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Dominic",
      "last_name": "Lovett",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Barrett",
      "last_name": "Banister",
      "position": "WR",
      "year": "GR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Mookie",
      "last_name": "Cooper",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Tyler",
      "last_name": "Stephens",
      "position": "TE",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Kibet",
      "last_name": "Chepyator",
      "position": "TE",
      "year": "GR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Ryan",
      "last_name": "Hoerstkamp",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Brady",
      "last_name": "Cook",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Tyler",
      "last_name": "Macon",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Sam",
      "last_name": "Horn",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Nathaniel",
      "last_name": "Peat",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Cody",
      "last_name": "Schrader",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Elijah",
      "last_name": "Young",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Tyler",
      "last_name": "Jones",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Missouri",
      "team_name": "Tigers",
      "first_name": "Daylan",
      "last_name": "Carnell",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Josh",
      "last_name": "Vann",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Xavier",
      "last_name": "Legette",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Landon",
      "last_name": "Samson",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Antwane",
      "last_name": "Wells Jr.",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Corey",
      "last_name": "Rucker",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "O'Mega",
      "last_name": "Blake",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Dakereon",
      "last_name": "Joyner",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Ahmarean",
      "last_name": "Brown",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Trey",
      "last_name": "Adkins",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Jaheim",
      "last_name": "Bell",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Traevon",
      "last_name": "Kenion",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Austin",
      "last_name": "Stogner",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Chad",
      "last_name": "Terrell",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Spencer",
      "last_name": "Rattler",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Luke",
      "last_name": "Doty",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Colten",
      "last_name": "Gauthier",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "MarShawn",
      "last_name": "Lloyd",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Christian",
      "last_name": "Beal-Smith",
      "position": "RB",
      "year": "GR/TR"
    },
    {
      "team_city": "South Carolina",
      "team_name": "Gamecocks",
      "first_name": "Juju",
      "last_name": "McDowell",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Cedric",
      "last_name": "Tillman",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Jimmy",
      "last_name": "Holiday",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Chas",
      "last_name": "Nimrod",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Bru",
      "last_name": "McCoy",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Ramel",
      "last_name": "Keyton",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Kaleb",
      "last_name": "Webb",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Jalin",
      "last_name": "Hyatt",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Jimmy",
      "last_name": "Calloway",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Marquarius",
      "last_name": "White",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Princeton",
      "last_name": "Fant",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Jacob",
      "last_name": "Warren",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Hunter",
      "last_name": "Salmon",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Hendon",
      "last_name": "Hooker",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Joe",
      "last_name": "Milton III",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Tayven",
      "last_name": "Jackson",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Jabari",
      "last_name": "Small",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Jaylen",
      "last_name": "Wright",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Justin",
      "last_name": "Williams-Thomas",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Brandon",
      "last_name": "Turnage",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Doneiko",
      "last_name": "Slaughter",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Tennessee",
      "team_name": "Volunteers",
      "first_name": "Wesley",
      "last_name": "Walker",
      "position": "RB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Jalen",
      "last_name": "Preston",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Evan",
      "last_name": "Stewart",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Devin",
      "last_name": "Price",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Chase",
      "last_name": "Lane",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Moose",
      "last_name": "Muhammad III",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Chris",
      "last_name": "Marshall",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Ainias",
      "last_name": "Smith",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Yulkeith",
      "last_name": "Brown",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Max",
      "last_name": "Wright",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Blake",
      "last_name": "Smith",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Jake",
      "last_name": "Johnson",
      "position": "TE",
      "year": "FR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Haynes",
      "last_name": "King",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Max",
      "last_name": "Johnson",
      "position": "QB",
      "year": "JR/TR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Conner",
      "last_name": "Weigman",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Devon",
      "last_name": "Achane",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "Amari",
      "last_name": "Daniels",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Texas A&M",
      "team_name": "Aggies",
      "first_name": "LJ",
      "last_name": "Johnson Jr.",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Will",
      "last_name": "Sheppard",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Quincy",
      "last_name": "Skinner Jr.",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Logan",
      "last_name": "Kyle",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Daveon",
      "last_name": "Walker",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Ezra",
      "last_name": "McAllister",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Devin",
      "last_name": "Boddie Jr.",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Jayden",
      "last_name": "McGowan",
      "position": "WR",
      "year": "FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Ben",
      "last_name": "Bresnahan",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Gavin",
      "last_name": "Schoenwald",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Joel",
      "last_name": "DeCoursey",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Ken",
      "last_name": "Seals",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Mike",
      "last_name": "Wright",
      "position": "QB",
      "year": "JR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "AJ",
      "last_name": "Swann",
      "position": "QB",
      "year": "FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Re'Mahn",
      "last_name": "Davis",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Rocko",
      "last_name": "Griffin",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Patrick",
      "last_name": "Smith",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Elijah",
      "last_name": "McAllister",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Darren",
      "last_name": "Agu",
      "position": "RB",
      "year": "FR"
    },
    {
      "team_city": "Vanderbilt",
      "team_name": "Commodores",
      "first_name": "Miles",
      "last_name": "Capers",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Christian",
      "last_name": "Wells",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Christan",
      "last_name": "Horn",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Dashaun",
      "last_name": "Davis",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Henry",
      "last_name": "Pearson",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Miller",
      "last_name": "Gibbs",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Chase",
      "last_name": "Brice",
      "position": "QB",
      "year": "GR/TR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Nate",
      "last_name": "Noel",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Camerun",
      "last_name": "Peoples",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Appalachian State",
      "team_name": "Mountaineers",
      "first_name": "Daetrich",
      "last_name": "Harrington",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Jeff",
      "last_name": "Foreman",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Adam",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Reagan",
      "last_name": "Ealy",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Te'Vailance",
      "last_name": "Hunt",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Seydou",
      "last_name": "Traore",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Reed",
      "last_name": "Tyler",
      "position": "TE",
      "year": "SR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "James",
      "last_name": "Blackman",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Wyatt",
      "last_name": "Begeal",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "Arkansas State",
      "team_name": "Red Wolves",
      "first_name": "Lincoln",
      "last_name": "Pare",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Tyson",
      "last_name": "Mobley",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Deon",
      "last_name": "Fountain",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Sam",
      "last_name": "Pinckney",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Tyler",
      "last_name": "Roberts",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Jared",
      "last_name": "Brown",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Aaron",
      "last_name": "Bedgood",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Xavier",
      "last_name": "Gravette",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "TJ",
      "last_name": "Ivy Jr.",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Patrick",
      "last_name": "McSweeney",
      "position": "TE",
      "year": "RS SR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Grayson",
      "last_name": "McCall",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Bryce",
      "last_name": "Carpenter",
      "position": "QB",
      "year": "RS SR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Jarrett",
      "last_name": "Guest",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Braydon",
      "last_name": "Bennett",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "Reese",
      "last_name": "White",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Coastal Carolina",
      "team_name": "Chanticleers",
      "first_name": "CJ",
      "last_name": "Beasley",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Amare",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Jjay",
      "last_name": "Mcafee",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Emil",
      "last_name": "Smith",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Derwin",
      "last_name": "Burgess Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Darius",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Khaleb",
      "last_name": "Hood",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Sam",
      "last_name": "Kenerson",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "JT",
      "last_name": "Galloway",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Beau",
      "last_name": "Johnson",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Sean",
      "last_name": "Pelkisson",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Kyle",
      "last_name": "Vantrease",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Connor",
      "last_name": "Cigelske",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Richie",
      "last_name": "Lankford",
      "position": "QB",
      "year": "SO/TR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Jalen",
      "last_name": "White",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "Gerald",
      "last_name": "Green",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia Southern",
      "team_name": "Eagles",
      "first_name": "J.D.",
      "last_name": "King",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Ja'Cyais",
      "last_name": "Credle",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Jamari",
      "last_name": "Thrash",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Terrance",
      "last_name": "Dixon",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Robert",
      "last_name": "Lewis",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Aubry",
      "last_name": "Payne",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Kris",
      "last_name": "Byrd",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Ahmon",
      "last_name": "Green",
      "position": "TE",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Darren",
      "last_name": "Grainger",
      "position": "QB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Mikele",
      "last_name": "Colasurdo",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Tucker",
      "last_name": "Gregg",
      "position": "RB",
      "year": "SR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Jamyest",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Georgia State",
      "team_name": "Panthers",
      "first_name": "Marcus",
      "last_name": "Carroll",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Peter",
      "last_name": "LeBlanc",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Errol",
      "last_name": "Rogers Jr.",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Kaleb",
      "last_name": "Carter",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Michael",
      "last_name": "Jefferson",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Dontae",
      "last_name": "Fleming",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "John",
      "last_name": "Stephens Jr.",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Jacob",
      "last_name": "Bernard",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Dalen",
      "last_name": "Cambre",
      "position": "WR",
      "year": "RS SO"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Neal",
      "last_name": "Johnson",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Pearse",
      "last_name": "Migl",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Johnny",
      "last_name": "Lumpkin",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Chandler",
      "last_name": "Fields",
      "position": "QB",
      "year": "RS SO"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Ben",
      "last_name": "Wooldridge",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Lance",
      "last_name": "Legendre",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Chris",
      "last_name": "Smith",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Terrence",
      "last_name": "Williams",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Kendrell",
      "last_name": "Williams",
      "position": "RB",
      "year": "RS FR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Ja'len",
      "last_name": "Johnson",
      "position": "RB",
      "year": "RS SR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Brandon",
      "last_name": "Bishop",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Louisiana",
      "team_name": "Ragin' Cajuns",
      "first_name": "Patrick",
      "last_name": "Mensah",
      "position": "RB",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Zach",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Fred",
      "last_name": "Lloyd Jr.",
      "position": "WR",
      "year": "GR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Dariyan",
      "last_name": "Wiley",
      "position": "WR",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Jevin",
      "last_name": "Frett",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Jordan",
      "last_name": "Carroll",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Justin",
      "last_name": "Kimber",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Boogie",
      "last_name": "Knight",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Malik",
      "last_name": "Jackson",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Will",
      "last_name": "Derrick",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Alred",
      "last_name": "Luke",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Coby",
      "last_name": "Cavil",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Zach",
      "last_name": "Rasmussen",
      "position": "TE",
      "year": "SR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Austin",
      "last_name": "Yankowy",
      "position": "TE",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Rylan",
      "last_name": "Green",
      "position": "TE",
      "year": "RS FR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Chandler",
      "last_name": "Rogers",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Jiya",
      "last_name": "Wright",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Garrett",
      "last_name": "Hable",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Andrew",
      "last_name": "Henry",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Isaiah",
      "last_name": "Phillips",
      "position": "RB",
      "year": "JR"
    },
    {
      "team_city": "Louisiana-Monroe",
      "team_name": "Warhawks",
      "first_name": "Charlie",
      "last_name": "Norman",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Devin",
      "last_name": "Voisin",
      "position": "WR",
      "year": "JR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Jalen",
      "last_name": "Wayne",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Caullin",
      "last_name": "Lacy",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Jay'juan",
      "last_name": "Townsend",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Brandon",
      "last_name": "Crum",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Jacob",
      "last_name": "Hopper",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Lincoln",
      "last_name": "Sefcik",
      "position": "TE",
      "year": "JR/TR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Desmond",
      "last_name": "Trotter",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Eli",
      "last_name": "Gainey",
      "position": "QB",
      "year": "RS FR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Terrion",
      "last_name": "Avery",
      "position": "RB",
      "year": "RS SR/TR"
    },
    {
      "team_city": "South Alabama",
      "team_name": "Jaguars",
      "first_name": "Bryan",
      "last_name": "Hill",
      "position": "RB",
      "year": "SR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Marcell",
      "last_name": "Barbee",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Julian",
      "last_name": "Ortega-Jones",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Javen",
      "last_name": "Banks",
      "position": "WR",
      "year": "SR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Waydale",
      "last_name": "Jones",
      "position": "WR",
      "year": "RS SR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Ashtyn",
      "last_name": "Hawkins",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Rontavius",
      "last_name": "Groves",
      "position": "WR",
      "year": "SR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Donnovan",
      "last_name": "Moorer",
      "position": "WR",
      "year": "SO/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Drue",
      "last_name": "Jackson",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Chandler",
      "last_name": "Speights",
      "position": "WR",
      "year": "RS SR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Jackson",
      "last_name": "Lanam",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Micah",
      "last_name": "Hilts",
      "position": "TE",
      "year": "JR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Layne",
      "last_name": "Hatcher",
      "position": "QB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Dillon",
      "last_name": "Markiewicz",
      "position": "QB",
      "year": "RS FR/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Ty",
      "last_name": "Evans",
      "position": "QB",
      "year": "RS SO/TR"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Calvin",
      "last_name": "Hill",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Texas State",
      "team_name": "Bobcats",
      "first_name": "Jahmyl",
      "last_name": "Jeter",
      "position": "RB",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Deshon",
      "last_name": "Stoudemire",
      "position": "WR",
      "year": "JR/TR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Demontrez",
      "last_name": "Brown",
      "position": "WR",
      "year": "RS JR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Marcus",
      "last_name": "Rogers",
      "position": "WR",
      "year": "RS JR/TR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Jabre",
      "last_name": "Barber",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Peyton",
      "last_name": "Higgins",
      "position": "WR",
      "year": "RS FR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Tez",
      "last_name": "Johnson",
      "position": "WR",
      "year": "SO"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Deyunkrea",
      "last_name": "Lewis",
      "position": "TE",
      "year": "SO"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "AJ",
      "last_name": "Lewis",
      "position": "TE",
      "year": "RS JR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Gunnar",
      "last_name": "Watson",
      "position": "QB",
      "year": "RS JR"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Kimani",
      "last_name": "Vidal",
      "position": "RB",
      "year": "SO"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "Jamontez",
      "last_name": "Woods",
      "position": "RB",
      "year": "RS SO"
    },
    {
      "team_city": "Troy",
      "team_name": "Trojans",
      "first_name": "DK",
      "last_name": "Billingsley",
      "position": "RB",
      "year": "RS SR"
    }
  ]
}
'''
