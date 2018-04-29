"""Creating a dictionary of initial data to load to the system as part of setup and
initialization. This dict will include a list of courses and sessions with its respective data
"""

data = {}

# a list of subjects
data['subjects'] = {
    "flight":[
            {
                "name": "Intro to Flight",
                "description": "This is a course aimed at absolute beginners who are learn how to fly.  Basic concepts, like flapping your arms wildly to create lift, are touched on.  At the end of the session, participants will have an understanding of what it means to fly, as compared with walking or swimming."
            },
            {
                "name": "Navigation",
                "description":"Topics include vectors, directions, yaw, and all that good stuff."
            },
            {
                "name": "Instrument-only Landing",
                "description": "In this class, we spraypaint over all the the windows in the cockpit of Cessna and force the student to navigate by instruments alone.  It's a real sink-or-swim kind of situation."
            },
            {
                "name": "Nightime Landing on Aircraft Carriers",
                "description": "In this class, pilots are encouraged to land their Cessna on an aircraft carrier at night.  Pilots who manage this feat are awarded a coupon for a free personal pan pizza at Pizza Hut, which we feel is a useful way to reinforce student learning."
            },
            {
                "name": "Helicopters",
                "description": "Basically like flying a plane, expect there's a lot more spinning involved.  Pilots learn the basics of helicopters by spinning around until they get dizzy, then try to pilot a surplus Apache attack helicopter we purchased from the Army-Navy surplus store on Route 36."
            },
            {
                "name":"Water Landings",
                "description":"Live out your Sully Sullenberger fantasy by crash-landing a Cessna into Lake Michigan.  Definitely bring a bathing suit for this one!"
            }
    ]

}

# a list of locations
data['locations'] = [
    {
        "name": "Hanger 18",
        "max_capacity": 4,
        "address_1": "321 Airport Access Road",
        "city": "Milwaulkee",
        "state": "WI",
        "zip_code": "56312",
        "country": "United States"
    },
    {
        "name": "Hanger 10",
        "max_capacity": 7,
        "address_1": "321 Airport Access Road",
        "city": "Milwaulkee",
        "state": "WI",
        "zip_code": "56312",
        "country": "United States"
    },
    {
        "name": "Airstrip 1",
        "max_capacity": 20,
        "address_1": "321 Airport Access Road",
        "city": "Milwaulkee",
        "state": "WI",
        "zip_code": "56312",
        "country": "United States"
    }
]

# a list of instructors
data['instructors'] = [
    {
        "username":"dcooper",
        "password":"12345",
        "email":"dcooper@classmo.com",
        "profile":{
            "first_name":"DB",
            "last_name":"Cooper",
            "phone_number":"",
            "address_1":"",
            "address_2":"",
            "city":"",
            "state":"",
            "zip_code":"",
            "country":""
        }
    },
    {
        "username":"jjetplane",
        "password":"12345",
        "email":"jjetplane@classmo.com",
        "profile":{
            "first_name":"JJ",
            "last_name":"Jetplane",
            "phone_number":"",
            "address_1":"",
            "address_2":"",
            "city":"",
            "state":"",
            "zip_code":"",
            "country":""
        }
    },
    {
        "username":"wwright",
        "password":"12345",
        "email":"wwright@classmo.com",
        "profile":{
            "first_name":"Wilbur",
            "last_name":"Wright",
            "phone_number":"",
            "address_1":"",
            "address_2":"",
            "city":"",
            "state":"",
            "zip_code":"",
            "country":""
        }
    },
]

data['sessions'] = [
    {
        "name":"Morning",
        "instructor":"dcooper"
    },
    {
        "name":"Afternoon",
        "instructor":"jjetplane"
    },
    {
        "name":"Evening",
        "instructor":"wwright"
    }
]
