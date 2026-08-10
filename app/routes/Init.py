from app.models.user import User
from app.models.projects import Project
from app.models.component import Component

user = User(
    name="Samantha Galaviz Archila",
    email="sgalaviz0819@gmail.com",
    phone="323-805-7622",
    bio=(
        "Hello! Welcome to my portfolio. I love all things related to ArcGIS, "
        "animal habitats, and protecting the planet's ecosystems. This portfolio "
        "features some of my work and experiences."
    ),
    about=[
        (
            "My name is Samantha Galaviz, and I am a graduate of the University of "
            "California, Riverside, where I earned a bachelor’s degree in Biology. "
            "Through my education, experience working as a naturalist, and volunteer "
            "work at an animal shelter, I have developed a strong interest in wildlife, "
            "conservation, and environmental safety. These experiences have strengthened "
            "my commitment to protecting animals and the environments they depend on."
        ),
        (
            "My goal is to become a GIS Analyst or GIS Technician, where I can combine "
            "my background in biology with technology, mapping, and data analysis to "
            "address real world environmental challenges. I am especially interested "
            "in conservation, environmental risk analysis, and using geographic "
            "information systems to better understand and protect natural resources."
        ),
        (
            "Ultimately, I want my work to make a meaningful impact. By combining "
            "science, technology, and my passion for wildlife, I hope to help organizations "
            "make informed decisions that create safer and healthier environments for "
            "both people and animals."
        ),
    ],
)

images = []

for i in range(10):
    images.append(
        Component(
            name=f"Project {i + 1}",
            url="/static/images/otter_sprite.png",
            desc=f"Project {i + 1}",
        )
    )