# 🚗 Travel Together — Carpooling Platform

**Travel Together** is a full-stack carpooling web application built with Python and Django. It connects drivers and passengers traveling between cities, allowing them to share rides, split costs, and travel comfortably together.

---

## 🌍 Overview

Inspired by platforms like BlaBlaCar and Uber Pool, Travel Together brings intercity carpooling to India. Drivers post their trips between cities, set a price per seat, and approve passengers. Passengers search for rides on their route, send a join request, and once approved — chat with the driver and confirm their journey.

---

## ✨ Features

### 👤 Passenger Features
- Register and login securely
- Complete profile with photo and identity document (Aadhar/PAN)
- Search rides by origin city, destination city, and date
- View full ride details — driver info, vehicle, price, seats, pickup/drop points
- Request a seat with a personal message
- Cancel a request anytime
- Chat with driver after approval
- View all upcoming and past trips

### 🚗 Driver Features
- Register as a driver by submitting documents
- Upload driving license, car RC, and insurance
- Add vehicle information (model, number, color)
- Create rides with route, departure time, seat count, and price
- Define pickup and drop points for the journey
- Approve or reject passenger requests
- Manage all passengers from a driver dashboard
- Chat with approved passengers

### 🛡️ Admin Features
- Full Django admin panel
- Verify or reject driver profiles
- Verify user identity documents
- View all rides, requests, and messages
- Monitor platform activity

---

## 🗄️ Database Models

| Model | Purpose |
|---|---|
| `UserProfile` | Extended user info — phone, city, identity document, verification status |
| `DriverProfile` | Driver-specific data — license, car details, RC, insurance, verification |
| `Ride` | A posted trip with route, timing, seats, and price |
| `RideRequest` | A passenger's request to join a ride — pending/approved/rejected |
| `RideMessage` | Chat messages between driver and approved passengers |
| `Notification` | In-app alerts for requests, approvals, and messages |

---

## 🔐 Verification Flow

```
Driver submits documents
          │
          ▼
    [ Pending Review ]
          │
     ┌────┴────┐
     ▼         ▼
  Verified   Rejected
     │
     ▼
Can post rides
```

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Django 4.2 |
| Database | SQLite (default) / MySQL 8.0 |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Typography | Google Fonts — Sora, Inter |
| Icons | Font Awesome 6 |
| Image Handling | Pillow |
| Authentication | Django Built-in Auth System |

---

## ⚙️ Setup (Windows)

```cmd
cd travel_together_carpooling
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py makemigrations drivers
python manage.py makemigrations rides
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## 🔑 Key URLs

| URL | Description |
|---|---|
| `/` | Home / Landing page with search |
| `/accounts/register/` | Register new account |
| `/accounts/login/` | Login |
| `/dashboard/` | User dashboard |
| `/rides/` | Search all rides |
| `/rides/create/` | Post a new ride |
| `/rides/my/` | Your rides as driver/passenger |
| `/drivers/become/` | Register as driver |
| `/drivers/dashboard/` | Driver management panel |
| `/admin/` | Django admin panel |

---

## 🚀 Future Scope

- **Real-time chat** using Django Channels and WebSockets
- **Google Maps** route visualization
- **Online Payment** integration (Razorpay/UPI)
- **Ratings & Reviews** for drivers and passengers
- **Mobile App** using React Native
- **Live Tracking** during the ride
- **Email/SMS Notifications** for ride updates

---

## 👨‍💻 Authors

**Rutvika** & **Krish**
Government Polytechnic Palanpur
Diploma in Information Technology — Semester 6 Final Year Project

---

<div align="center">
  <strong>Travel Together — Share the Journey, Split the Cost.</strong>
</div>
