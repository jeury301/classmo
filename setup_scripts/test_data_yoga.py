"""Creating a dictionary of initial data to load to the system as part of setup and
initialization. This dict will include a list of courses and sessions with its respective data
"""

data = {}

# a list of subjects
data['subjects'] = {
    "yoga":[
            {
                "name": "Yoga for Beginners",
                "description": "This is a course aimed at absolute beginners who are eager to explore the practice of yoga.  Basic poses, like the warrior post and tree pose, are explored in a welcoming and nuturing environment."
            },
            {
                "name": "Hatha Yoga",
                "description":"A physical-based approach to yoga, this class is aimed at intermediate and advanced yoga practioners."
            },
            {
                "name": "Iyengar Yoga",
                "description": "Explore your body with the detailed and precise movements of our Iyenga Yoga class.  This two-hour session is aimed at advanced yoga practitioners."
            },
            {
                "name": "Kundalini yoga",
                "description": "This class is all about experiencing both the spiritual and physical sides of yoga.  Get in touch with your inner self in a big way."
            },
            {
                "name": "Vinyasa yoga",
                "description": "Feel the transformative power of the eight-limbed path."
            },
            {
                "name":"Bikram yoga",
                "description":"If sweating profusely is enjoyable for you, you will adore this class. Yoga in 105 degree heat - it's undeniably delightful."
            }
    ]

}

# a list of locations
data['locations'] = [
    {
        "name": "Lotus Room",
        "max_capacity":10,
        "address_1": "777 Levon Helm Way",
        "city": "Woodstock",
        "state": "NY",
        "zip_code": "11211",
        "country": "United States"
    },
    {
        "name": "Tadasana Chamber",
        "max_capacity":6,
        "address_1": "777 Levon Helm Way",
        "city": "Woodstock",
        "state": "NY",
        "zip_code": "11211",
        "country": "United States"
    },
    {
        "name": "Vajrasana Courtyard",
        "max_capacity":20,
        "address_1": "777 Levon Helm Way",
        "city": "Woodstock",
        "state": "NY",
        "zip_code": "11211",
        "country": "United States"
    }
]

# a list of instructors
data['instructors'] = [
    {
        "username":"hlee",
        "password":"12345",
        "email":"hlee@classmo.com",
        "profile":{
            "first_name":"Hyori",
            "last_name":"Lee",
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
        "username":"yberra",
        "password":"12345",
        "email":"yberra@classmo.com",
        "profile":{
            "first_name":"Yogi",
            "last_name":"Berra",
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
        "username":"myogi",
        "password":"12345",
        "email":"myogi@classmo.com",
        "profile":{
            "first_name":"Maharishi",
            "last_name":"Yogi",
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
        "instructor":"llay"
    },
    {
        "name":"Afternoon",
        "instructor":"gryan"
    },
    {
        "name":"Evening",
        "instructor":"asohn"
    }
]
