"""Creating a dictionary of initial data to load to the system as part of setup and
initialization. This dict will include a list of courses and sessions with its respective data
"""

data = {}

# a list of subjects
data['subjects'] = {
    "cs":[
            {
                "name": "CS 115 Tutoring",
                "description": "Intro. to CS I in C++: Fundamentals of computer science are introduced, with emphasis on programming methodology and problem solving. Topics include basic concepts of computer systems, software engineering, algorithm design, programming languages and data abstraction, with applications. The high level language C++ is fully discussed and serves as the vehicle to illustrate many of the concepts. CIS majors should enroll in CS 113."
            },
            {
                "name": "CS 252 Tutoring",
                "description":"Computer Organization and Architecture: An introduction to the organization and architecture of computer systems, including the standard Von Neumann model and more recent architectural concepts. Among the topics covered are numeric data representation, assembly language organization, memory addressing, memory systems, both real and virtual, coding and compression, input/output structures treated as programmed, interrupt, and direct memory access, and functional organization of the CPU and the computer system."
            },
            {
                "name": "CS 280 Tutoring",
                "description": "Programming Language Concepts: Conceptual study of programming language syntax, semantics and implementation. Course covers language definition structure, data types and structures, control structures and data flow, run-time consideration, and interpretative languages."
            },
            {
                "name": "CS 288 Tutoring",
                "description":"Intensive Programming in Linux: The course covers Linux programming with Apache Web and MySql database using Php/Python and C as primary languages. It consists of four stages: basic tools such as Bash and C programming; searching trees and matrix computing, end-to-end applications such as one that constantly presents top 100 stocks; and extending the applications to run on multiple machines. The course provides students with hands-on experience for programming relatively large applications."
            },
            {
                "name": "CS 332 Tutoring",
                "description":"Principles of Operating Systems: Organization of operating systems covering structure, process management and scheduling; interaction of concurrent processes; interrupts; I/O, device handling; memory and virtual memory management and file management."
            },
            {
                "name":"CS 431 Tutoring",
                "description":"Database system architecture; data modeling using the entity-relationship model; storage of databases; the hierarchical, network and relational data models; formal and commercial query languages; functional dependencies and normalization for relational database design; relation decomposition; concurrency control and transactions management. Student projects involve the use of a DBMS package."
            },
            {
                "name":"CS 490 Tutoring",
                "description":"Guided Design in Software Engineering: This course focuses on the methodology for developing software systems. Methods and techniques for functional requirements analysis and specifications, design, coding, testing and proving, integration and maintenance are discussed."
            },
            {
                "name":"CS 491 Tutoring",
                "description":"Senior Project: An opportunity for the student to integrate the knowledge and skills gained in previous computer science work into a team-based project. The project involves investigation of current literature as well as computer implementation of either a part of a large program or the whole of a small system."
            }
    ]

}

# a list of locations
data['locations'] = [
    {
        "name": "Central King Building | Room 220",
        "max_capacity":10,
        "address_1": "Newark Campus",
        "city": "Newark",
        "state": "NJ",
        "zip_code": "07105",
        "country": "United States"
    },
    {
        "name": "Tiernan Hall | Room 112",
        "max_capacity":30,
        "address_1": "Newark Campus",
        "city": "Newark",
        "state": "NJ",
        "zip_code": "07105",
        "country": "United States"
    },
    {
        "name":"Kupfrian Hall | Room 206",
        "max_capacity":20,
        "address_1": "Newark Campus",
        "city": "Newark",
        "state": "NJ",
        "zip_code": "07105",
        "country": "United States"
    }
]

# a list of instructors
data['instructors'] = [
    {
        "username":"gryan",
        "password":"12345",
        "email":"gryan@classmo.com",
        "profile":{
            "first_name":"Gerard",
            "last_name":"Ryan",
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
        "username":"llay",
        "password":"12345",
        "email":"llay@classmo.com",
        "profile":{
            "first_name":"Larry",
            "last_name":"Lay",
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
        "username":"asohn",
        "password":"12345",
        "email":"asohn@classmo.com",
        "profile":{
            "first_name":"Andrew",
            "last_name":"Sohn",
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
        "name":"101",
        "instructor":"llay"
    },
    {
        "name":"201",
        "instructor":"gryan"
    },
    {
        "name":"301",
        "instructor":"asohn"
    }
]
