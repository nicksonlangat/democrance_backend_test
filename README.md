
### AUTHENTICATION OF USERS/CUSTOMERS
In the spirit of separation of concerns, a `Customer` and a `User` are two different entities each playing a specific role in the system.
The `User` model is responsible for handling authentication and authorization while the `Customer` model stores and handles business-specific information and roles eg Policy creation and assignment.
At the end of the day, a customer is a user in the system so there exists a `OneToOne` relationship in the `Customer` model. A user can only belong to one customer and vice-versa in the system.
Each time a new customer is created, an associated user is created as well via a `signal`.
