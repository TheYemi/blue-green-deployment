How to Run

1. Clone the project

    - git clone <repo-url>
    - cd blue-green-deployment

2. Create .env file

    - BLUE_IMAGE=<blue_image_url>
    - GREEN_IMAGE=<green_image_url>
    - ACTIVE_POOL=blue
    - RELEASE_ID_BLUE=blue-v1
    - RELEASE_ID_GREEN=green-v1

3. Start all services

    - docker-compose up -d
     
4. Check version (Blue active)

    - curl -i http://localhost:8080/version

5. Simulate Blue failure

    - curl -X POST http://localhost:8081/chaos/start?mode=error

6. Verify switch to Green

    - curl -i http://localhost:8080/version

7. Stop chaos

    - curl -X POST http://localhost:8081/chaos/stop

8. Stop container
    
    - docker-compose down
