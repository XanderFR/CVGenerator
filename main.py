from tkinter import *
from tkinter import messagebox

import pyqrcode
from fpdf import FPDF


class PDFCV(FPDF):
    def header(self):
        self.image("mywebsite.png", 10, 8, 33, title="Portfolio Site")

    def footer(self):
        pass

    def generateCV(self, name, email, phoneNumber, address, skills, workExperience, education, aboutMe):
        # Set up the page
        self.add_page()
        self.ln(20)

        # Personal information
        self.set_font("Helvetica", "B", 26)

        self.cell(0, 10, name,
                  new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "B", 12)

        self.cell(0, 10, "Contact Information",
                  new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_font("Helvetica", "", 10)

        self.cell(0, 5, "Email: {}".format(email),
                  new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 5, "Phone: {}".format(phoneNumber),
                  new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 5, "Address: {}".format(address),
                  new_x="LMARGIN", new_y="NEXT")

        # Skills
        self.ln(10)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Skills", new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_font("Helvetica", "", 10)
        for skill in skills:
            self.cell(0, 5, "- {}".format(skill),
                      new_x="LMARGIN", new_y="NEXT")

        # Work experience
        self.ln(10)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Work Experience",
                  new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_font("Helvetica", "", 10)
        for experience in workExperience:
            self.cell(0, 5, "{}: {}".format(
                experience['title'], experience['description']), new_x="LMARGIN", new_y="NEXT")

        # Education
        self.ln(10)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "Education", new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_font("Helvetica", "", 10)
        for educationItem in education:
            self.cell(0, 5, "{}: {}".format(
                educationItem['degree'], educationItem['university']), new_x="LMARGIN", new_y="NEXT")

        # About Me
        self.ln(10)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, "About Me", new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, aboutMe)

        # Output PDF
        self.output("CV.pdf")


def generateCVPDF():
    name = nameEntry.get()
    email = emailEntry.get()
    phoneNumber = phoneEntry.get()
    address = addressEntry.get()
    website = websiteEntry.get()
    skills = skillsEntry.get("1.0", END).strip().split('\n')  # Removes whitespace and newline characters
    workExperience = []
    education = []

    workExperienceLines = experienceEntry.get("1.0", END).strip().split('\n')
    educationLines = educationEntry.get("1.0", END).strip().split('\n')
    aboutMe = aboutMeEntry.get("1.0", END)

    for line in workExperienceLines:
        title, description = line.split(':')
        workExperience.append({'title': title.strip(), 'description': description.strip()})

    for line in educationLines:
        degree, university = line.split(':')
        education.append({'degree': degree.strip(), 'university': university.strip()})

    # Create QR CODE
    qrCode = pyqrcode.create(website)
    qrCode.png("mywebsite.png", scale=6)

    if not name or not email or not phoneNumber or not address or not skills or not workExperience or not education or not aboutMe:
        messagebox.showerror("Error", "Please fill in all the details")
        return

    cv = PDFCV()
    cv.generateCV(name, email, phoneNumber, address, skills, workExperience, education, aboutMe)
    messagebox.showinfo("Success", "PDF CV generated successfully.")

window = Tk()
window.title("CV Generator")

nameLabel = Label(window, text="Name: ")
nameLabel.pack()
nameEntry = Entry(window, width=40)
nameEntry.pack()

emailLabel = Label(window, text="Email: ")
emailLabel.pack()
emailEntry = Entry(window, width=40)
emailEntry.pack()

phoneLabel = Label(window, text="Phone: ")
phoneLabel.pack()
phoneEntry = Entry(window, width=40)
phoneEntry.pack()

addressLabel = Label(window, text="Address: ")
addressLabel.pack()
addressEntry = Entry(window, width=40)
addressEntry.pack()

websiteLabel = Label(window, text="Website: ")
websiteLabel.pack()
websiteEntry = Entry(window, width=40)
websiteEntry.pack()

skillsLabel = Label(window, text="Skills (Enter one skill per line)")
skillsLabel.pack()
skillsEntry = Text(window, height=5)
skillsEntry.pack()

educationLabel = Label(window, text="Education (One per line in format 'Degree':'University')")
educationLabel.pack()
educationEntry = Text(window, height=5)
educationEntry.pack()

experienceLabel = Label(window, text="Experience (One per line in format 'Job Title':'Description')")
experienceLabel.pack()
experienceEntry = Text(window, height=5)
experienceEntry.pack()

aboutMeLabel = Label(window, text="About Me")
aboutMeLabel.pack()
aboutMeEntry = Text(window, height=5)
aboutMeEntry.pack()

generateButton = Button(window, text="Generate CV", command=generateCVPDF)
generateButton.pack()

window.mainloop()
