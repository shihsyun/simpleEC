# simpleEC
use DRF to provide EC function, include register, order, ship, feedback.

User Story as below
1. User can register a customer.
2. User can Apply a seller.
3. Seller can manange product and stock.
4. Customer can place orders when product stock is greater than zero.
5. Seller need to shipping when receive the orders.
6. Customer can give feedback when transaction end.

Architecture
1. Use DRF for main frame.
2. Use Celery to do async task, like approve application etc.
3. Use k8s+GCP to do production env.
