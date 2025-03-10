# Google Maps Geocode API

This repository is for the maps services assignment.
It allows user to enter the source and destination address and the user can see the geometric distance between the two points. Also the address gets formatted to the precise location as well.

---

## **Features**

- **PostgresSQL Integration**: Queries postgres table for already entered locations to save on external API calls
- **Flow**: Enter source and destination locations and press 'Go'. You get the geometric distance between the two locations.

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/shimin8/channel-factory.git
   cd channel-factory
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the project root:
   ```plaintext
   GMAPS_API_KEY=<your-google-maps-api-key>
   GMAPS_GEOCODE_URL=https://maps.googleapis.com/maps/api/
   POSTGRES_PROJECT=mapsproject
   POSTGRES_USER=user1
   POSTGRES_PASSWORD=password1
   ```

4. To run the project, open 2 terminal tabs to run the backend and frontend service:
   ```bash
   ctrl+shift+T
   ```
   To run the backend service (assuming python is installed):
   ```bash
   cd backend
   python -m venv env
   source backend/env/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

   To run the frontend service:
      To install npm, nodejs, cURL and nvm
      ```bash
      cd frontend
      sudo apt install nodejs npm -y
      sudo apt install curl -y
      curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
      source ~/.bashrc
      ```

      To install the 
      ```bash
      npm install
      nvm install v18.20.7
      nvm use 18.20.7
      npm run dev
      ```

---

## **Usage**

- The UI prompts user to enter the source (the starting location) and the destination (the destination location). When the 'Go' button is pressed (after entering both the source and destination), the Distance field is populated with the geometric distance between the two locations.
- Also, the addresses entered by the user are replaced by the formatted addresses that represent the actual and complete addresses as seen on google maps
- The page also contains the Reset button, in case you want to start afresh.

### **Endpoints**

#### **POST calc-geometric-distance/**
this endpoint takes two locations in the req body and returns the geometric distance between the two

- **Request Body**:
  ```json
  {
    "source": "delhi",
    "destination": "agra"
  }
  ```

- **Response**:
  ```json
  {
    "status": 200,
    "src": "New Delhi, Delhi, India",
    "dest": "Agra, Uttar Pradesh, India",
    "distance": 178.27
  }
  ```

#### **POST fetch-location/**
this endpoint takes a single location and returns the formatted/actual address of the location

- **Request Body**:
  ```json
  {
    "location": "gurugram, cyberpark"
  }
  ```

- **Response**:
  ```json
  {
    "status": 200,
    "data": {
        "formattedAddress": "BLC-143, Golf Course Rd, DLF Phase 5, Sector 54, Gurugram, Haryana 122002, India",
        "coordinates": {
            "lat": 28.4350259,
            "lng": 77.10593899999999
        }
    }
  }
  ```
---

## **Code Structure**

   ```bash
       project/
    │── backend/
    │   ├── manage.py
    │   ├── requirements.txt
    │   ├── config/
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── wsgi.py
    │   │   ├── asgi.py
    │   ├── apps/
    │   │   ├── main/
    │   │   │   ├── models.py
    │   │   │   ├── views.py
    │   │   │   ├── services.py
    │   │   ├── wsgi.py
    │   ├── env/
    │
    │── frontend/
    │   ├── node_modules/
    │   ├── public/
    │   ├── src/
    │   │   ├── components/
    │   │   │   ├── DistanceService.tsx
    │   │   ├── main/
    │   │   ├── pages/
    │   │   ├── services/
    │   ├── package.json
    │   ├── vite.config.js
    │
    │── .env
    │── .gitignore
    │── README.md

   ```
---
