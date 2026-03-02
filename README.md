# Ecommerce App 

This project is a functional e-commerce platform that simulates a complete online shopping experience. It was built with a strong focus on usability, responsiveness, and state management, allowing users to browse products, manage a shopping cart, and view item details dynamically.

| Path | Description | 
| :--- | :--- | 
| `/product` | Product listing and item details | 
| `/order` | Checkout summary and order finalization | 
| `/webhook` | API endpoint for payment notifications | 
| `/success` | Confirmation page for approved payments | 
| `/failure` | Notification page for declined or failed payments | 
| `/pending` | Information for payments awaiting processing | 

## 💡 Features

- **Dynamic Catalog:** Browse products with real-time data.
- **Payment Integration:** Handling transaction flows via feedback URLs.
- **Webhook Support:** Real-time order status updates from payment gateways.

## 🛠️ Technical Stack

This project leverages a modern full-stack architecture for performance and scalability:

* **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python-based high-performance web framework).
* **Frontend:** HTML5, CSS3, and JavaScript (Vanilla JS or framework-specific).
* **Payment Integration:** [Mercado Pago SDK](https://www.mercadopago.com.br/developers/) (Secure checkout and payment processing).
* **Image Management:** [Cloudinary](https://cloudinary.com/) (Cloud-based image hosting and optimization).
* **Database:** [Aiven](https://aiven.io/) (Managed PostgreSQL or MySQL for reliable data storage).
* **API Communication:** RESTful architecture with JSON exchange.

## 🔐 Environment Variables

To run this project, you will need to create a `.env` file in your root directory and add the following variables. These keys are essential for database connection, payment processing, and cloud storage.

| Variable | Description | Source |
| :--- | :--- | :--- |
| `DB_URI` | Connection string for the database | **Aiven** Console |
| `MP_ACCESS_TOKEN` | Your private production or test access token | **Mercado Pago** Developers |
| `MP_WEBHOOK_SIGNATURE` | Secret key to validate incoming webhook notifications | **Mercado Pago** Dashboard |
| `REMOTE_STORAGE_NAME` | Cloudinary Cloud Name | **Cloudinary** Dashboard |
| `REMOTE_STORAGE_IDENTITY` | Cloudinary API Key | **Cloudinary** Dashboard |
| `REMOTE_STORAGE_KEY` | Cloudinary API Secret | **Cloudinary** Dashboard |
| `TN_URL` | The base URL of your deployed application | Production/Localhost |
| `TEST_EMAIL` | Email address used for testing payment flows | Sandbox Account |

> [!CAUTION]
> **Deployment Requirement:** For the Mercado Pago integration and Webhook notifications to function, this project **must be deployed and exposed on a live production server** with a valid SSL (HTTPS).
> 
> * **Why?** Mercado Pago's notification system requires a stable, publicly accessible endpoint. 
> * **Tunneling Issue:** Using tunneling services (like **ngrok** or **localtunnel**) is **not supported** or often fails to maintain the handshake required for the Mercado Pago Webhook flow. The system will only consistently receive payment updates when hosted in a properly exposed environment.

> [!WARNING]
> Keep your `.env` file out of version control. Ensure it is listed in your `.gitignore`.
