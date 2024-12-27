# Social Media Application Using FastAPI

This project is a social media application built using **FastAPI**, providing robust APIs for user interaction and post management. The application includes features like user authentication, post creation, commenting, liking, and following/unfollowing users. Additionally, it integrates with **AWS S3** for scalable image storage.

## Project Description

The application enables users to:
- Register and authenticate securely using JWT.
- Create, update, delete, and retrieve posts.
- Add comments to posts and interact through likes/unlikes.
- Follow/unfollow other users to build connections.
- Manage detailed user profiles, including profile pictures and bio updates.

---

## Version-Wise Functionalities

### Version 1
- **Implemented:** User authentication with JWT.
- **Features:** Basic CRUD operations for posts.
- **Database:** Integrated database for managing users and posts.

### Version 2
- **Added:** Commenting system for posts.
- **Enhanced:** Post update and deletion functionalities.
- **Validation:** API validation and error handling for seamless user experience.

### Version 3
- **Advanced Features:**
  - Like/unlike functionality for posts.
  - Follow/unfollow system for users.
  - Detailed user profiles with followers, following, and posts.
- **Scalable Image Storage:** Integrated AWS S3 for profile and post image storage.

---

## Technologies Used

- **Framework:** FastAPI
- **Database:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Cloud Storage:** AWS S3
- **Language:** Python
- **Dependency Management:** Pydantic for validation

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Virtual Environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/niyazasghar/Social-Media-Post-FastAPI.git
   cd Social-Media-Post-FastAPI
