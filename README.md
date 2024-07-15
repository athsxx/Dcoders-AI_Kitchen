# AI Kitchen for India

## Overview
AI Kitchen for India is an innovative application designed to revolutionize the cooking experience. By leveraging advanced machine learning and computer vision techniques, this application assists users in identifying fruits and vegetables, generating recipes, and providing real-time kitchen assistance. The project showcases the future of tech-enabled culinary practices, integrating object detection, natural language processing (NLP), and user-friendly interfaces to create a seamless and intuitive cooking companion.

## Key Features

### Object Detection
- **Dataset**: Utilizes custom made dataset to detect various fruits,vegetables,spices,cereals and utensils found in Indian Kitchen.
- **Models**: Employs  and MobileNetV2 for classification and recognition.
- **Implementation**: Detects and classifies various  fruits,vegetables,spices,cereals and utensils using  MobileNetV2 for fine-grained classification.
- **Data Augmentation**: Uses TensorFlow’s `ImageDataGenerator` for rescaling, augmentation, and generating training and validation datasets.

### Recipe Reader
- **Natural Language Processing (NLP)**:Process the instructions,ingredients and utensils and display them based on user input
### Frontend
- **Technologies**: HTML, CSS, JavaScript.
- **Design**: Implements user-friendly design principles using Figma for prototyping and layout design.

### Backend
- **Framework**: Flask.
- **API Integration**: Provides APIs for object detection, classification, and recipe generation.

## Technology Stack
- **Frontend**: HTML, CSS, JavaScript, Figma for design.
- **Backend**: Flask, TensorFlow/Keras for machine learning models.
- **Models**: YOLO for object detection, MobileNetV2 for classification.
- **Data Handling**: TensorFlow’s `ImageDataGenerator` for data augmentation.

## Usage
The application provides a camera interface for users to scan their kitchen ingredients. Upon detection, the app lists the identified items and suggests recipes that can be made from them. Users can interact with the app through a web interface, with real-time processing handled by the backend.

## Conclusion
AI Kitchen for India exemplifies the potential of AI to enhance everyday activities, such as cooking. By merging advanced machine learning techniques with user-friendly web technologies, the application not only simplifies the cooking process but also encourages creativity in the kitchen. The project stands as a testament to how technology can empower individuals, making cooking more accessible and enjoyable for everyone. As we continue to refine and expand its features, AI Kitchen for India aims to become an indispensable tool for modern cooking, ultimately transforming how we interact with food in our daily lives.
## Setup and Installation

### Prerequisites
- Python 3.6+
- pip (Python package installer)
- Kaggle API

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AI-Kitchen-for-India.git
   cd AI-Kitchen-for-India
### Set Up Kaggle API
1. Go to your Kaggle account and generate the API token (`kaggle.json`).
2. Place the `kaggle.json` file in the `~/.kaggle/` directory (Mac/Linux) or `C:\Users\<YourUsername>\.kaggle\` (Windows).

### Download the Dataset

###NLP: Used for generating recipes based on user inputs-###
1. _NLP.py_ includes a normal recipe
2. _NLP-voice_ includes voice output 


Figma: Used for designing the user interface and overall user experience.

**Figma Design**

The user interface and experience of AI Kitchen for India were meticulously designed using Figma. You can view the design prototype here:
https://www.figma.com/design/1rznz84plJ6s4bU7ihmBLm/Intel-Project?node-id=0-1&t=EEgjEXuOmTZCxzoZ-1









