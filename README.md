# Vendor Management System

## Table of Contents

- [Introduction](#introduction)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
  - [Vendor Endpoints](#vendor-endpoints)
  - [Purchase Order Endpoints](#purchase-order-endpoints)
  - [Vendor Performance Endpoint](#vendor-performance-endpoint)
- [Running the Test Suite](#running-the-test-suite)

## Introduction

The Vendor Management System is a Django-based application for managing vendors and purchase orders. It includes endpoints for creating, updating, retrieving, and deleting vendors and purchase orders, as well as retrieving vendor performance metrics.

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL (for production)

### Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2. **Create and Activate a Virtual Environment**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install Django djangorestframework djangorestframework-simplejwt
    ```

4. **Apply Migrations**

    ```sh
    python manage.py migrate
    ```

5. **Create a Superuser**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the Development Server**

    ```sh
    python manage.py runserver
    ```

## API Endpoints

### Vendor Endpoints

1. **POST /api/vendors/**: Create a new vendor.

    **Request Body:**

    ```json
    {
        "name": "Vendor Name",
        "contact_details": "Contact Details",
        "address": "Vendor Address",
        "vendor_code": "V001"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "name": "Vendor Name",
        "contact_details": "Contact Details",
        "address": "Vendor Address",
        "vendor_code": "V001",
        "on_time_delivery_rate": 0,
        "quality_rating_avg": 0,
        "average_response_time": 0,
        "fulfillment_rate": 0
    }
    ```

2. **GET /api/vendors/**: List all vendors.

    **Response:**

    ```json
    [
        {
            "id": 1,
            "name": "Vendor Name",
            "contact_details": "Contact Details",
            "address": "Vendor Address",
            "vendor_code": "V001",
            "on_time_delivery_rate": 0,
            "quality_rating_avg": 0,
            "average_response_time": 0,
            "fulfillment_rate": 0
        },
        ...
    ]
    ```

3. **GET /api/vendors/{vendor_id}/**: Retrieve a specific vendor's details.

    **Response:**

    ```json
    {
        "id": 1,
        "name": "Vendor Name",
        "contact_details": "Contact Details",
        "address": "Vendor Address",
        "vendor_code": "V001",
        "on_time_delivery_rate": 0,
        "quality_rating_avg": 0,
        "average_response_time": 0,
        "fulfillment_rate": 0
    }
    ```

4. **PUT /api/vendors/{vendor_id}/**: Update a vendor's details.

    **Request Body:**

    ```json
    {
        "name": "Updated Vendor Name",
        "contact_details": "Updated Contact Details",
        "address": "Updated Vendor Address",
        "vendor_code": "V001"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "name": "Updated Vendor Name",
        "contact_details": "Updated Contact Details",
        "address": "Updated Vendor Address",
        "vendor_code": "V001",
        "on_time_delivery_rate": 0,
        "quality_rating_avg": 0,
        "average_response_time": 0,
        "fulfillment_rate": 0
    }
    ```

5. **DELETE /api/vendors/{vendor_id}/**: Delete a vendor.

    **Response:**

    ```json
    {
        "message": "Vendor deleted successfully"
    }
    ```

### Purchase Order Endpoints

6. **POST /api/purchase_orders/**: Create a purchase order.

    **Request Body:**

    ```json
    {
        "po_number": "PO001",
        "vendor": 1,
        "order_date": "2023-01-01T00:00:00Z",
        "delivery_date": "2023-01-07T00:00:00Z",
        "items": [{"item": "item1", "quantity": 10}],
        "quantity": 10,
        "status": "pending",
        "issue_date": "2023-01-01T00:00:00Z"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "po_number": "PO001",
        "vendor": 1,
        "order_date": "2023-01-01T00:00:00Z",
        "delivery_date": "2023-01-07T00:00:00Z",
        "items": [{"item": "item1", "quantity": 10}],
        "quantity": 10,
        "status": "pending",
        "issue_date": "2023-01-01T00:00:00Z",
        "acknowledgment_date": null
    }
    ```

7. **GET /api/purchase_orders/**: List all purchase orders with an option to filter by vendor.

    **Response:**

    ```json
    [
        {
            "id": 1,
            "po_number": "PO001",
            "vendor": 1,
            "order_date": "2023-01-01T00:00:00Z",
            "delivery_date": "2023-01-07T00:00:00Z",
            "items": [{"item": "item1", "quantity": 10}],
            "quantity": 10,
            "status": "pending",
            "issue_date": "2023-01-01T00:00:00Z",
            "acknowledgment_date": null
        },
        ...
    ]
    ```

8. **GET /api/purchase_orders/{po_id}/**: Retrieve details of a specific purchase order.

    **Response:**

    ```json
    {
        "id": 1,
        "po_number": "PO001",
        "vendor": 1,
        "order_date": "2023-01-01T00:00:00Z",
        "delivery_date": "2023-01-07T00:00:00Z",
        "items": [{"item": "item1", "quantity": 10}],
        "quantity": 10,
        "status": "pending",
        "issue_date": "2023-01-01T00:00:00Z",
        "acknowledgment_date": null
    }
    ```

9. **PUT /api/purchase_orders/{po_id}/**: Update a purchase order.

    **Request Body:**

    ```json
    {
        "po_number": "PO001",
        "vendor": 1,
        "order_date": "2023-01-01T00:00:00Z",
        "delivery_date": "2023-01-07T00:00:00Z",
        "items": [{"item": "item1", "quantity": 10}],
        "quantity": 10,
        "status": "completed",
        "issue_date": "2023-01-01T00:00:00Z",
        "acknowledgment_date": "2023-01-02T00:00:00Z"
    }
    ```

    **Response:**

    ```json
    {
        "id": 1,
        "po_number": "PO001",
        "vendor": 1,
        "order_date": "2023-01-01T00:00:00Z",
        "delivery_date": "2023-01-07T00:00:00Z",
        "items": [{"item": "item1", "quantity": 10}],
        "quantity": 10,
        "status": "completed",
        "issue_date": "2023-01-01T00:00:00Z",
        "acknowledgment_date": "2023-01-02T00:00:00Z"
    }
    ```

10. **DELETE /api/purchase_orders/{po_id}/**: Delete a purchase order.

    **Response:**

    ```json
    {
        "message": "Purchase order deleted successfully"
    }
    ```

### Vendor Performance Endpoint

11. **GET /api/vendors/{vendor_id}/performance**: Retrieve a vendor's performance metrics.

    **Response:**

    ```json
    {
        "on_time_delivery_rate": 0.9,
        "quality_rating_avg": 4.5,
        "average_response_time": 24,
        "fulfillment_rate": 0.8
    }
    ```

## Running the Test Suite

1. **Run Tests**

    ```sh
    python manage.py test
    ```

This will run all the test cases and ensure the functionality and reliability of the endpoints.

---

By following the above instructions, you should be able to set up the project, understand the API endpoints, and run the test suite effectively. If you encounter any issues, please refer to the Django documentation or reach out for support.
