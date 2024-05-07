# Django Vendor Management System

## Introduction
This is a Vendor Management System built using Django and Django REST Framework. It allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Features
- **Vendor Profile Management:**
  - Create, retrieve, update, and delete vendor profiles.
- **Purchase Order Tracking:**
  - Create, retrieve, update, and delete purchase orders.
- **Vendor Performance Evaluation:**
  - Calculate performance metrics such as on-time delivery rate, quality rating average, response time, and fulfillment rate.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/Django-Vendor-Management-System.git
**
  *** API Endpoints***
**Vendor Endpoints:**
List/Create Vendor: http://127.0.0.1:8000/api/vendors/
Retrieve/Update/Delete Vendor: http://127.0.0.1:8000/api/vendors/{vendor_id}/
Vendor Performance: http://127.0.0.1:8000/api/vendors/{vendor_id}/performance/
Purchase Order Endpoints:
List/Create Purchase Order: http://127.0.0.1:8000/api/purchase_orders/
Retrieve/Update/Delete Purchase Order: http://127.0.0.1:8000/api/purchase_orders/{po_id}/

**Documentation**
For detailed documentation on each API endpoint, please refer to the API Documentation.
