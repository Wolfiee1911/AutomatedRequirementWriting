# AutomatedRequirementWriting



**Dynamo** is an AI-powered system designed to analyze textual and graphic inputs, extract key functional and non-functional requirements, and organize them into a standardized format. Built for the **Barclays Hack and Hire Hackathon**, this project leverages advanced natural language processing (NLP) and optical character recognition (OCR) to streamline the requirement engineering process for software development teams.

---


## Project Overview

Dynamo is a web-based application that automates the process of requirement gathering and documentation. It supports multiple input types (text, images, PDFs, Word documents, Excel sheets, and web pages), extracts functional and non-functional requirements using AI, and generates standardized requirement documents and user stories for Jira backlog updates. The system is designed to handle multiple concurrent users, supports English dialects, and includes version-controlled inventory management for requirement documents.

The frontend features a modern, aesthetic design with the Discord color palette, a card-based layout, and the "Team Dynamo" logo for branding.

---

## Features

- **Multi-Input Support:** Accepts direct text input and uploads of various document types (minutes of meetings, emails, Word, Excel, PDFs, web pages, and images).
- **Graphic Input Analysis:** Extracts text from images using OCR (Tesseract).
- **Requirement Extraction:** Analyzes inputs to extract functional and non-functional requirements using a pre-trained GPT-2 model.
- **Public Domain Knowledge:** Applies knowledge from public domain sources (e.g., finance-specific rules from `finance_rules.csv`).
- **Real-Time Refinement:** Poses dynamic questions based on user input to refine requirements.
- **Standardized Output:**
  - Generates a 2-3 page Software Requirements Specification (SRS) document in Word format.
  - Exports user stories to Excel for Jira backlog updates.
- **Version Control:** Maintains an inventory of requirement documents with version control.
- **Multi-User Support:** Handles multiple concurrent users with session management.
- **Dialect Support:** Supports American and British English dialects.
- **Modern UI:** Features a sleek, card-based layout with the Discord color palette and "Team Dynamo" branding.

---

## Design Considerations

- **Language Support:** The system supports users of the English language, with options for American and British dialects to handle terminology differences (e.g., "color" vs. "colour").
- **Bias Mitigation:** Designed to work with different English dialects, ensuring inclusivity and reducing bias in requirement generation.
- **Version-Controlled Inventory Management:** Maintains a versioned inventory of requirement documents, allowing users to access previous versions.
- **Standard Requirement Document:** Generates a consistent 2-3 page SRS document with sections for Introduction, Functional Requirements, Non-Functional Requirements, Assumptions and Constraints, and Summary.

---

## Installation

### Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Tesseract OCR**: Required for image processing (see setup instructions below).
- **Virtual Environment**: Recommended to manage dependencies.
- **Git**: For cloning the repository.

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/AutomatedRequirementWriting.git
   cd AutomatedRequirementWriting
